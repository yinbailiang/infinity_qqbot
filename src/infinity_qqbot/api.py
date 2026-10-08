"""QQ 机器人 OpenAPI 客户端。

使用 ``aiohttp`` 进行网络传输，并强制使用 ``certifi`` 提供的 CA 证书包
（``ssl.create_default_context(cafile=certifi.where())``），保证虚拟环境 /
容器等受限环境下 TLS 校验始终可用。

``QQBotAPI`` 覆盖 QQ 机器人开放平台 v2 的全部接口，主要分为：

- 凭证：``fetch_access_token`` / ``get_access_token``（自动缓存与提前刷新）；
- 网关：``get_gateway`` / ``get_gateway_bot``；
- 单聊：发送 / 流式发送 / 撤回 / 富媒体上传（URL 与分片）；
- 群聊：发送 / 撤回 / 富媒体上传 / 群信息 / 群成员 / 入群申请 / 黑名单 / 禁言；
- 互动：``respond_interaction``；菜单与指令面板；
- 频道：子频道管理、消息、私信、成员、身份组、禁言、公告、权限、表情表态、精华消息、日程。

所有方法均为 ``async``，返回已解析的 Pydantic 模型（或 ``None``），
失败时抛出 :class:`QQBotAPIError`。
"""

from __future__ import annotations

import asyncio
import json
import logging
import ssl
import time
from collections.abc import Sequence
from enum import Enum
from typing import Any, cast

import aiohttp
import certifi
from event_bus.templates import ServiceError
from pydantic import BaseModel

from .models import (
    DMS,
    AccessTokenResponse,
    Announce,
    ApiPermissionDemand,
    ApiPermissionList,
    BotInfo,
    Channel,
    FileUploadResponse,
    Gateway,
    GatewayBot,
    GroupBotState,
    GroupInfo,
    GroupMember,
    GroupMemberPage,
    Guild,
    GuildMember,
    InputNotify,
    JoinRequestPage,
    Keyboard,
    MediaInfo,
    Menu,
    MenuResponse,
    MenuVersion,
    Message,
    MessageMarkdown,
    MessageReference,
    MessageResponse,
    Panel,
    PanelCreated,
    PanelInfo,
    PanelList,
    ReactionUsers,
    RecommendChannel,
    RestrictChatSetting,
    Role,
    Schedule,
    SetMemberMuteState,
    StreamMessageResponse,
    UploadPrepareResponse,
)

logger = logging.getLogger(__name__)

__all__ = [
    'QQBOT_API_BASE',
    'QQBotAPI',
    'QQBotAPIError',
]

#: 统一请求地址
QQBOT_API_BASE = 'https://api.bot.qq.com'

#: 获取 access_token 的路径
QQBOT_TOKEN_PATH = '/app/getAppAccessToken'

#: 默认 User-Agent
_USER_AGENT = 'infinity-qqbot/0.1.0'


class QQBotAPIError(ServiceError):
    """OpenAPI 调用失败（继承 ``ServiceError``）。

    作为处理器内抛出的异常时，``ServiceHandler`` 会自动把它转换为
    ``success=False`` 的 RPC 响应（``error_code`` / ``error_msg`` 跨总线保留）。

    Attributes:
        code: 平台错误码（``err_code`` / ``code``），网络层错误时为 ``None``。
        message: 平台错误信息（仅用于人工排查，勿用于逻辑判断）。
        trace_id: 平台链路追踪 ID。
        status: HTTP 状态码。
        payload: 原始响应体。
    """

    def __init__(
        self,
        code: int | None,
        message: str,
        *,
        trace_id: str | None = None,
        status: int | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.trace_id = trace_id
        self.status = status
        self.payload = payload

    def __str__(self) -> str:
        """包含错误码的可读信息（作为处理器异常时跨总线成为 ``error_msg``）。"""
        return f'[{self.code}] {self.message}' if self.code is not None else self.message


def to_jsonable(value: Any) -> Any:
    """把任意值转换为可 JSON 序列化的结构（Pydantic 模型 / 枚举 / 容器）。"""
    if value is None:
        return None
    if isinstance(value, BaseModel):
        return value.model_dump(mode='json', exclude_none=True)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        mapping = cast(dict[str, Any], value)
        return {k: to_jsonable(v) for k, v in mapping.items() if v is not None}
    if isinstance(value, (list, tuple)):
        sequence = cast(list[Any] | tuple[Any, ...], value)
        return [to_jsonable(v) for v in sequence]
    return value


def _parse_json(text: str) -> Any:
    """解析 JSON 文本；空文本或解析失败返回 ``None``。"""
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _as_body(data: Any) -> dict[str, Any] | None:
    """把任意响应数据统一为 ``dict[str, Any]``（非字典返回 ``None``）。"""
    if isinstance(data, dict):
        return cast(dict[str, Any], data)
    return None


def _compact(**fields: Any) -> dict[str, Any]:
    """构造请求体：丢弃 ``None`` 字段并递归 JSON 化。"""
    body = {key: to_jsonable(value) for key, value in fields.items() if value is not None}
    return body


class QQBotAPI:
    """QQ 机器人 OpenAPI 客户端（aiohttp + certifi）。"""

    def __init__(
        self,
        app_id: str,
        client_secret: str,
        *,
        base_url: str = QQBOT_API_BASE,
        token_url: str | None = None,
        timeout: float = 30.0,
        session: aiohttp.ClientSession | None = None,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        """初始化客户端。

        Args:
            app_id: 机器人 AppID。
            client_secret: 机器人 AppSecret。
            base_url: 统一请求地址，默认 ``https://api.bot.qq.com``。
            token_url: 凭证接口完整地址，默认 ``{base_url}/app/getAppAccessToken``。
            timeout: 单请求超时（秒）。
            session: 复用的 ``aiohttp.ClientSession``；不传则内部创建（并负责关闭）。
            ssl_context: 自定义 SSL 上下文；默认使用 certifi 证书包构建。
        """
        self.app_id = app_id
        self.client_secret = client_secret
        self._base_url = base_url.rstrip('/')
        self._token_url = token_url or f'{self._base_url}{QQBOT_TOKEN_PATH}'
        self._timeout = timeout
        self._session = session
        self._owns_session = session is None
        self._ssl_context = ssl_context or ssl.create_default_context(cafile=certifi.where())
        self._access_token: str | None = None
        self._token_expire_at: float = 0.0
        self._token_lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # 会话与生命周期
    # ------------------------------------------------------------------

    @property
    def ssl_context(self) -> ssl.SSLContext:
        """当前使用的 SSL 上下文（certifi 证书）。"""
        return self._ssl_context

    async def ensure_session(self) -> aiohttp.ClientSession:
        """返回底层 ``aiohttp.ClientSession``（必要时惰性创建）。"""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(ssl=self._ssl_context)
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self._timeout),
                headers={
                    'User-Agent': _USER_AGENT,
                    'Accept': 'application/json',
                },
            )
            self._owns_session = True
        return self._session

    async def close(self) -> None:
        """关闭内部创建的会话（外部注入的会话不会被关闭）。"""
        if self._session is not None and self._owns_session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> 'QQBotAPI':
        await self.ensure_session()
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # 底层请求
    # ------------------------------------------------------------------

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        headers: dict[str, str] | None = None,
        auth: bool = True,
        base_url: str | None = None,
    ) -> Any:
        """发送请求并解析响应；失败时抛出 :class:`QQBotAPIError`。"""
        session = await self.ensure_session()
        request_headers = dict(headers or {})
        if auth:
            request_headers['Authorization'] = f'QQBot {await self.get_access_token()}'
        url = f'{base_url or self._base_url}{path}'
        async with session.request(method, url, params=params, json=json_body, headers=request_headers) as resp:
            status = resp.status
            trace_id = resp.headers.get('X-Tps-trace-ID')
            if status == 204:
                return None
            text = await resp.text()
            data: Any = _parse_json(text)
            body = _as_body(data)
            if 200 <= status < 300:
                if body is not None:
                    code = body.get('err_code')
                    if isinstance(code, int) and code != 0:
                        raise QQBotAPIError(
                            code,
                            str(body.get('message', '')),
                            trace_id=body.get('trace_id') or trace_id,
                            status=status,
                            payload=data,
                        )
                return data
            if body is not None:
                code = body.get('err_code')
                message = str(body.get('message', text))
                trace_id = body.get('trace_id') or trace_id
            else:
                code = None
                message = text or f'HTTP {status}'
            raise QQBotAPIError(code, message, trace_id=trace_id, status=status, payload=data)

    # ------------------------------------------------------------------
    # 凭证
    # ------------------------------------------------------------------

    async def fetch_access_token(self) -> AccessTokenResponse:
        """请求平台签发新的 access_token（不读取缓存）。"""
        session = await self.ensure_session()
        async with session.post(
            self._token_url,
            json={'appId': self.app_id, 'clientSecret': self.client_secret},
        ) as resp:
            text = await resp.text()
            data: Any = _parse_json(text)
            body = _as_body(data)
            if body is None or 'access_token' not in body:
                if body is not None:
                    code = body.get('code')
                    message = str(body.get('message', text))
                else:
                    code = None
                    message = text or f'HTTP {resp.status}'
                raise QQBotAPIError(code, message, status=resp.status, payload=data)
            return AccessTokenResponse.model_validate(data)

    async def get_access_token(self, *, force: bool = False) -> str:
        """获取 access_token（带缓存）。

        默认在过期前 60 秒自动刷新（与官方建议一致）；``force=True`` 强制刷新。
        """
        async with self._token_lock:
            now = time.monotonic()
            if self._access_token is not None and not force and now < self._token_expire_at:
                return self._access_token
            resp = await self.fetch_access_token()
            self._access_token = resp.access_token
            # 提前 60 秒视为过期，避免边界期间请求失败
            self._token_expire_at = now + max(resp.expires_in - 60, 30)
            logger.debug('QQBot access_token 已刷新，有效期 %s 秒', resp.expires_in)
            return self._access_token

    # ------------------------------------------------------------------
    # 网关
    # ------------------------------------------------------------------

    async def get_gateway(self) -> Gateway:
        """获取通用 WSS 接入点（``GET /gateway``）。"""
        data = await self._request('GET', '/gateway')
        return Gateway.model_validate(data)

    async def get_gateway_bot(self) -> GatewayBot:
        """获取带分片的 WSS 接入点与连接限制（``GET /gateway/bot``）。"""
        data = await self._request('GET', '/gateway/bot')
        return GatewayBot.model_validate(data)

    # ------------------------------------------------------------------
    # 机器人
    # ------------------------------------------------------------------

    async def get_me(self) -> BotInfo:
        """获取机器人详情（``GET /users/@me``）。"""
        data = await self._request('GET', '/users/@me')
        return BotInfo.model_validate(data)

    async def get_my_guilds(
        self,
        *,
        before: str | None = None,
        after: str | None = None,
        limit: int | None = None,
    ) -> list[Guild]:
        """获取机器人频道列表（``GET /users/@me/guilds``）。"""
        data = await self._request(
            'GET', '/users/@me/guilds', params={'before': before, 'after': after, 'limit': limit}
        )
        items: list[Any] = data or []
        return [Guild.model_validate(item) for item in items]

    async def generate_url_link(self, **payload: Any) -> dict[str, Any]:
        """生成分享链接（``POST /v2/generate_url_link``，字段随平台更新，透传）。"""
        data = await self._request('POST', '/v2/generate_url_link', json_body=_compact(**payload))
        return data or {}

    # ------------------------------------------------------------------
    # 单聊消息
    # ------------------------------------------------------------------

    def _qq_message_body(
        self,
        *,
        content: str | None = None,
        msg_type: int | None = None,
        markdown: MessageMarkdown | dict[str, Any] | None = None,
        keyboard: Keyboard | dict[str, Any] | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        msg_seq: int | None = None,
        media: MediaInfo | dict[str, Any] | None = None,
        message_reference: MessageReference | dict[str, Any] | None = None,
        is_wakeup: bool | None = None,
        input_notify: InputNotify | dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return _compact(
            content=content,
            msg_type=msg_type,
            markdown=markdown,
            keyboard=keyboard,
            msg_id=msg_id,
            event_id=event_id,
            msg_seq=msg_seq,
            media=media,
            message_reference=message_reference,
            is_wakeup=is_wakeup,
            input_notify=input_notify,
        )

    async def send_c2c_message(
        self,
        user_openid: str,
        *,
        content: str | None = None,
        msg_type: int | None = None,
        markdown: MessageMarkdown | dict[str, Any] | None = None,
        keyboard: Keyboard | dict[str, Any] | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        msg_seq: int | None = None,
        media: MediaInfo | dict[str, Any] | None = None,
        message_reference: MessageReference | dict[str, Any] | None = None,
        is_wakeup: bool | None = None,
        input_notify: InputNotify | dict[str, Any] | None = None,
    ) -> MessageResponse:
        """发送单聊消息（``POST /v2/users/{user_openid}/messages``）。"""
        data = await self._request(
            'POST',
            f'/v2/users/{user_openid}/messages',
            json_body=self._qq_message_body(
                content=content,
                msg_type=msg_type,
                markdown=markdown,
                keyboard=keyboard,
                msg_id=msg_id,
                event_id=event_id,
                msg_seq=msg_seq,
                media=media,
                message_reference=message_reference,
                is_wakeup=is_wakeup,
                input_notify=input_notify,
            ),
        )
        return MessageResponse.model_validate(data)

    async def send_c2c_stream_message(
        self,
        user_openid: str,
        *,
        input_state: int,
        index: int,
        content_raw: str | None = None,
        input_mode: str | None = None,
        content_type: str | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        stream_msg_id: str | None = None,
        msg_seq: int | None = None,
        is_wakeup: bool | None = None,
    ) -> StreamMessageResponse:
        """流式发送单聊消息（``POST /v2/users/{user_openid}/stream_messages``）。

        首片使用 ``index=0`` 且不传 ``stream_msg_id``，响应 ``id`` 即后续分片
        需要携带的 ``stream_msg_id``；``input_state``：``1`` 生成中、``10`` 结束。
        """
        data = await self._request(
            'POST',
            f'/v2/users/{user_openid}/stream_messages',
            json_body=_compact(
                input_mode=input_mode,
                input_state=input_state,
                index=index,
                content_type=content_type,
                content_raw=content_raw,
                msg_id=msg_id,
                event_id=event_id,
                stream_msg_id=stream_msg_id,
                msg_seq=msg_seq,
                is_wakeup=is_wakeup,
            ),
        )
        return StreamMessageResponse.model_validate(data)

    async def recall_c2c_message(self, user_openid: str, message_id: str) -> None:
        """撤回单聊消息（``DELETE /v2/users/{user_openid}/messages/{message_id}``）。"""
        await self._request('DELETE', f'/v2/users/{user_openid}/messages/{message_id}')

    async def upload_c2c_file(
        self,
        user_openid: str,
        *,
        file_type: int,
        url: str | None = None,
        file_name: str | None = None,
        srv_send_msg: bool | None = None,
        upload_id: str | None = None,
    ) -> FileUploadResponse:
        """单聊富媒体上传（``POST /v2/users/{user_openid}/files``）。

        - URL 上传：传入 ``url``；
        - 分片合并：完成分片后传入 ``upload_id``；
        - ``srv_send_msg=True`` 时上传即发送（返回中包含消息 ``id``）。
        """
        data = await self._request(
            'POST',
            f'/v2/users/{user_openid}/files',
            json_body=_compact(
                file_type=file_type,
                url=url,
                file_name=file_name,
                srv_send_msg=srv_send_msg,
                upload_id=upload_id,
            ),
        )
        return FileUploadResponse.model_validate(data)

    async def c2c_upload_prepare(
        self,
        user_openid: str,
        *,
        file_type: int,
        file_size: int | str,
        file_name: str,
        md5: str,
        sha1: str,
        md5_10m: str,
    ) -> UploadPrepareResponse:
        """单聊富媒体预上传（``POST /v2/users/{user_openid}/upload_prepare``）。

        返回 ``upload_id``、分片预签名 URL 与上传配置；随后逐片 ``HTTP PUT``
        到 ``presigned_url`` 并调用 :meth:`c2c_upload_part_finish`。
        """
        data = await self._request(
            'POST',
            f'/v2/users/{user_openid}/upload_prepare',
            json_body=_compact(
                file_type=file_type,
                file_size=str(file_size),
                file_name=file_name,
                md5=md5,
                sha1=sha1,
                md5_10m=md5_10m,
            ),
        )
        return UploadPrepareResponse.model_validate(data)

    async def c2c_upload_part_finish(self, user_openid: str, **payload: Any) -> None:
        """单聊分片上传完成（``POST /v2/users/{user_openid}/upload_part_finish``）。

        请求体字段随平台更新（如 ``upload_id`` / ``index``），直接透传。
        """
        await self._request('POST', f'/v2/users/{user_openid}/upload_part_finish', json_body=_compact(**payload))

    # ------------------------------------------------------------------
    # 群聊消息
    # ------------------------------------------------------------------

    async def send_group_message(
        self,
        group_openid: str,
        *,
        content: str | None = None,
        msg_type: int | None = None,
        markdown: MessageMarkdown | dict[str, Any] | None = None,
        keyboard: Keyboard | dict[str, Any] | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        msg_seq: int | None = None,
        media: MediaInfo | dict[str, Any] | None = None,
        message_reference: MessageReference | dict[str, Any] | None = None,
        is_wakeup: bool | None = None,
        input_notify: InputNotify | dict[str, Any] | None = None,
    ) -> MessageResponse:
        """发送群聊消息（``POST /v2/groups/{group_openid}/messages``）。"""
        data = await self._request(
            'POST',
            f'/v2/groups/{group_openid}/messages',
            json_body=self._qq_message_body(
                content=content,
                msg_type=msg_type,
                markdown=markdown,
                keyboard=keyboard,
                msg_id=msg_id,
                event_id=event_id,
                msg_seq=msg_seq,
                media=media,
                message_reference=message_reference,
                is_wakeup=is_wakeup,
                input_notify=input_notify,
            ),
        )
        return MessageResponse.model_validate(data)

    async def recall_group_message(self, group_openid: str, message_id: str) -> None:
        """撤回群聊消息（``DELETE /v2/groups/{group_openid}/messages/{message_id}``）。"""
        await self._request('DELETE', f'/v2/groups/{group_openid}/messages/{message_id}')

    async def upload_group_file(
        self,
        group_openid: str,
        *,
        file_type: int,
        url: str | None = None,
        file_name: str | None = None,
        srv_send_msg: bool | None = None,
        upload_id: str | None = None,
    ) -> FileUploadResponse:
        """群聊富媒体上传（``POST /v2/groups/{group_openid}/files``）。"""
        data = await self._request(
            'POST',
            f'/v2/groups/{group_openid}/files',
            json_body=_compact(
                file_type=file_type,
                url=url,
                file_name=file_name,
                srv_send_msg=srv_send_msg,
                upload_id=upload_id,
            ),
        )
        return FileUploadResponse.model_validate(data)

    async def group_upload_prepare(
        self,
        group_openid: str,
        *,
        file_type: int,
        file_size: int | str,
        file_name: str,
        md5: str,
        sha1: str,
        md5_10m: str,
    ) -> UploadPrepareResponse:
        """群聊富媒体预上传（``POST /v2/groups/{group_openid}/upload_prepare``）。"""
        data = await self._request(
            'POST',
            f'/v2/groups/{group_openid}/upload_prepare',
            json_body=_compact(
                file_type=file_type,
                file_size=str(file_size),
                file_name=file_name,
                md5=md5,
                sha1=sha1,
                md5_10m=md5_10m,
            ),
        )
        return UploadPrepareResponse.model_validate(data)

    async def group_upload_part_finish(self, group_openid: str, **payload: Any) -> None:
        """群聊分片上传完成（``POST /v2/groups/{group_openid}/upload_part_finish``，字段透传）。"""
        await self._request('POST', f'/v2/groups/{group_openid}/upload_part_finish', json_body=_compact(**payload))

    # ------------------------------------------------------------------
    # 群信息 / 群成员 / 入群申请 / 黑名单 / 禁言
    # ------------------------------------------------------------------

    async def get_group_info(self, group_openid: str) -> GroupInfo:
        """获取群基本信息（``GET /v2/groups/{group_openid}/info``）。"""
        data = await self._request('GET', f'/v2/groups/{group_openid}/info')
        return GroupInfo.model_validate(data)

    async def get_group_bot_state(self, group_openid: str) -> GroupBotState:
        """获取机器人群内状态（``GET /v2/groups/{group_openid}/bot_state``）。"""
        data = await self._request('GET', f'/v2/groups/{group_openid}/bot_state')
        return GroupBotState.model_validate(data or {})

    async def get_group_members(self, group_openid: str, *, cursor: str | None = None) -> GroupMemberPage:
        """获取群成员列表，每次最多 30 条（``GET /v2/groups/{group_openid}/members``）。"""
        data = await self._request('GET', f'/v2/groups/{group_openid}/members', params={'cursor': cursor})
        return GroupMemberPage.model_validate(data or {})

    async def get_group_member(self, group_openid: str, member_openid: str) -> GroupMember:
        """获取群成员信息（``GET /v2/groups/{group_openid}/members/{member_openid}``）。"""
        data = await self._request('GET', f'/v2/groups/{group_openid}/members/{member_openid}')
        return GroupMember.model_validate(data)

    async def batch_remove_group_members(self, group_openid: str, members: list[str], **extra: Any) -> None:
        """群成员批量移除（``POST /v2/groups/{group_openid}/batch_remove_members``）。

        Args:
            members: 待移除成员 OpenID 列表。
            **extra: 平台新增字段透传。
        """
        await self._request(
            'POST',
            f'/v2/groups/{group_openid}/batch_remove_members',
            json_body=_compact(members=members, **extra),
        )

    async def get_join_request_list(
        self,
        group_openid: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> JoinRequestPage:
        """拉取入群申请列表（``GET /v2/groups/{group_openid}/join_request_list``）。"""
        data = await self._request(
            'GET',
            f'/v2/groups/{group_openid}/join_request_list',
            params={'cursor': cursor, 'limit': limit},
        )
        return JoinRequestPage.model_validate(data or {})

    async def approval_join_request(
        self,
        group_openid: str,
        member_openid: str,
        *,
        join_request_id: str | None = None,
        approve: bool | None = None,
        reason: str | None = None,
        **extra: Any,
    ) -> None:
        """入群申请审批（``POST /v2/groups/{group_openid}/approval_join_request/{member_openid}``）。

        Args:
            join_request_id: 申请 ID（来自入群申请列表 / 事件）。
            approve: 是否同意。
            reason: 审批理由。
            **extra: 平台新增字段透传。
        """
        await self._request(
            'POST',
            f'/v2/groups/{group_openid}/approval_join_request/{member_openid}',
            json_body=_compact(join_request_id=join_request_id, approve=approve, reason=reason, **extra),
        )

    async def get_join_approval_strategies(self, **params: Any) -> dict[str, Any]:
        """查询入群自动审批策略列表（``GET /v2/groups/join_approval_strategy``，字段透传）。"""
        data = await self._request('GET', '/v2/groups/join_approval_strategy', params=_compact(**params) or None)
        return data or {}

    async def create_join_approval_strategy(self, **payload: Any) -> dict[str, Any]:
        """创建入群自动审批策略（``POST /v2/groups/join_approval_strategy``，字段透传）。"""
        data = await self._request('POST', '/v2/groups/join_approval_strategy', json_body=_compact(**payload))
        return data or {}

    async def update_join_approval_strategy(self, strategy_id: str, **payload: Any) -> dict[str, Any]:
        """修改入群自动审批策略（``PATCH /v2/groups/join_approval_strategy/{strategy_id}``，字段透传）。"""
        data = await self._request(
            'PATCH', f'/v2/groups/join_approval_strategy/{strategy_id}', json_body=_compact(**payload)
        )
        return data or {}

    async def delete_join_approval_strategy(self, strategy_id: str) -> None:
        """删除入群自动审批策略（``DELETE /v2/groups/join_approval_strategy/{strategy_id}``）。"""
        await self._request('DELETE', f'/v2/groups/join_approval_strategy/{strategy_id}')

    async def execute_join_approval_strategy(self, strategy_id: str, **payload: Any) -> dict[str, Any]:
        """执行入群自动审批策略（``POST .../{strategy_id}/execute``，字段透传）。"""
        data = await self._request(
            'POST', f'/v2/groups/join_approval_strategy/{strategy_id}/execute', json_body=_compact(**payload)
        )
        return data or {}

    async def update_join_approval_whitelist(self, strategy_id: str, **payload: Any) -> dict[str, Any]:
        """修改入群自动审批策略白名单（``POST .../{strategy_id}/whitelist_users``，字段透传）。"""
        data = await self._request(
            'POST',
            f'/v2/groups/join_approval_strategy/{strategy_id}/whitelist_users',
            json_body=_compact(**payload),
        )
        return data or {}

    async def get_group_blacklist(self, group_openid: str, **params: Any) -> dict[str, Any]:
        """群黑名单查询（``GET /v2/groups/{group_openid}/member_blacklist``，字段透传）。"""
        data = await self._request(
            'GET', f'/v2/groups/{group_openid}/member_blacklist', params=_compact(**params) or None
        )
        return data or {}

    async def operate_group_blacklist(self, group_openid: str, **payload: Any) -> dict[str, Any]:
        """群黑名单操作（``POST /v2/groups/{group_openid}/member_blacklist``，字段透传）。"""
        data = await self._request('POST', f'/v2/groups/{group_openid}/member_blacklist', json_body=_compact(**payload))
        return data or {}

    async def get_group_restrict_chat_setting(self, group_openid: str) -> RestrictChatSetting:
        """查询群禁言状态（``GET /v2/groups/{group_openid}/restrict_chat_setting``）。"""
        data = await self._request('GET', f'/v2/groups/{group_openid}/restrict_chat_setting')
        return RestrictChatSetting.model_validate(data or {})

    async def set_group_member_mute(
        self, group_openid: str, members: Sequence[SetMemberMuteState | dict[str, Any]]
    ) -> None:
        """设置群成员禁言（``POST /v2/groups/{group_openid}/restrict_chat_setting``）。

        单次设置不能超过 20 个成员；``op=del`` 传空 ``mute_expire_at`` 表示立即解除。
        """
        await self._request(
            'POST',
            f'/v2/groups/{group_openid}/restrict_chat_setting',
            json_body=_compact(members=members),
        )

    # ------------------------------------------------------------------
    # 互动
    # ------------------------------------------------------------------

    async def respond_interaction(self, interaction_id: str, *, code: int = 0, **extra: Any) -> None:
        """互动事件响应（``PUT /interactions/{interaction_id}``）。

        Args:
            interaction_id: ``INTERACTION_CREATE`` 事件的 ``d.id``（不带前缀）。
            code: 0 成功 / 1 操作失败 / 2 操作频繁 / 3 重复操作 / 4 没有权限 / 5 仅管理员。
        """
        await self._request('PUT', f'/interactions/{interaction_id}', json_body=_compact(code=code, **extra))

    # ------------------------------------------------------------------
    # 自定义菜单 / 指令面板
    # ------------------------------------------------------------------

    async def get_menu(self) -> MenuResponse:
        """查询全局自定义菜单（``GET /v2/menu``）。"""
        data = await self._request('GET', '/v2/menu')
        return MenuResponse.model_validate(data or {})

    async def put_menu(self, menu: Menu | dict[str, Any]) -> MenuVersion:
        """修改全局自定义菜单（``PUT /v2/menu``，传入即覆盖）。"""
        data = await self._request('PUT', '/v2/menu', json_body=_compact(menu=menu))
        return MenuVersion.model_validate(data or {})

    async def list_panels(self, **params: Any) -> PanelList:
        """查询指令面板列表（``GET /v2/panels``，查询参数透传）。"""
        data = await self._request('GET', '/v2/panels', params=_compact(**params) or None)
        return PanelList.model_validate(data or {})

    async def create_panel(
        self,
        *,
        scope: str,
        panel: Panel | dict[str, Any],
        target_type: str | None = None,
        user_openids: list[str] | None = None,
        group_openids: list[str] | None = None,
    ) -> PanelCreated:
        """创建指令面板（``POST /v2/panels``）。

        Args:
            scope: ``c2c`` / ``group`` / ``channel`` / ``dm``。
            panel: 面板配置。
            target_type: ``all`` 或 ``specific``（channel/dm 仅支持 all）。
            user_openids: specific 时的用户列表（c2c，最多 20）。
            group_openids: specific 时的群列表（group，最多 20）。
        """
        data = await self._request(
            'POST',
            '/v2/panels',
            json_body=_compact(
                scope=scope,
                panel=panel,
                target_type=target_type,
                user_openids=user_openids,
                group_openids=group_openids,
            ),
        )
        return PanelCreated.model_validate(data or {})

    async def get_panel(self, panel_id: str) -> PanelInfo:
        """查询指令面板详情（``GET /v2/panels/{panel_id}``）。"""
        data = await self._request('GET', f'/v2/panels/{panel_id}')
        return PanelInfo.model_validate(data or {})

    async def update_panel(self, panel_id: str, **payload: Any) -> None:
        """修改指令面板（``PUT /v2/panels/{panel_id}``，字段透传）。"""
        await self._request('PUT', f'/v2/panels/{panel_id}', json_body=_compact(**payload))

    async def delete_panel(self, panel_id: str) -> None:
        """删除指令面板（``DELETE /v2/panels/{panel_id}``）。"""
        await self._request('DELETE', f'/v2/panels/{panel_id}')

    async def update_panel_target(self, panel_id: str, **payload: Any) -> None:
        """修改指令面板关联对象（``PUT /v2/panels/{panel_id}/target``，字段透传）。"""
        await self._request('PUT', f'/v2/panels/{panel_id}/target', json_body=_compact(**payload))

    # ------------------------------------------------------------------
    # 频道管理
    # ------------------------------------------------------------------

    async def get_guild(self, guild_id: str) -> Guild:
        """获取频道详情（``GET /guilds/{guild_id}``）。"""
        data = await self._request('GET', f'/guilds/{guild_id}')
        return Guild.model_validate(data)

    async def get_guild_channels(self, guild_id: str) -> list[Channel]:
        """获取子频道列表（``GET /guilds/{guild_id}/channels``）。"""
        data = await self._request('GET', f'/guilds/{guild_id}/channels')
        items: list[Any] = data or []
        return [Channel.model_validate(item) for item in items]

    async def create_guild_channel(
        self,
        guild_id: str,
        *,
        name: str,
        type: int,
        position: int | None = None,
        parent_id: str | None = None,
        sub_type: int | None = None,
        private_type: int | None = None,
        private_user_limit: int | None = None,
        **extra: Any,
    ) -> Channel:
        """创建子频道（``POST /guilds/{guild_id}/channels``）。

        Args:
            type: 0 文字 / 2 语音 / 4 分组。
            **extra: 平台新增字段透传。
        """
        data = await self._request(
            'POST',
            f'/guilds/{guild_id}/channels',
            json_body=_compact(
                name=name,
                type=type,
                position=position,
                parent_id=parent_id,
                sub_type=sub_type,
                private_type=private_type,
                private_user_limit=private_user_limit,
                **extra,
            ),
        )
        return Channel.model_validate(data)

    async def get_channel(self, channel_id: str) -> Channel:
        """获取子频道详情（``GET /channels/{channel_id}``）。"""
        data = await self._request('GET', f'/channels/{channel_id}')
        return Channel.model_validate(data)

    async def update_channel(self, channel_id: str, **payload: Any) -> Channel:
        """修改子频道（``PATCH /channels/{channel_id}``，字段透传）。"""
        data = await self._request('PATCH', f'/channels/{channel_id}', json_body=_compact(**payload))
        return Channel.model_validate(data)

    async def delete_channel(self, channel_id: str) -> None:
        """删除子频道（``DELETE /channels/{channel_id}``）。"""
        await self._request('DELETE', f'/channels/{channel_id}')

    # ------------------------------------------------------------------
    # 频道消息 / 私信
    # ------------------------------------------------------------------

    def _channel_message_body(
        self,
        *,
        content: str | None = None,
        embed: dict[str, Any] | None = None,
        ark: dict[str, Any] | None = None,
        image: str | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        markdown: MessageMarkdown | dict[str, Any] | None = None,
        message_reference: MessageReference | dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return _compact(
            content=content,
            embed=embed,
            ark=ark,
            image=image,
            msg_id=msg_id,
            event_id=event_id,
            markdown=markdown,
            message_reference=message_reference,
        )

    async def send_channel_message(
        self,
        channel_id: str,
        *,
        content: str | None = None,
        embed: dict[str, Any] | None = None,
        ark: dict[str, Any] | None = None,
        image: str | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        markdown: MessageMarkdown | dict[str, Any] | None = None,
        message_reference: MessageReference | dict[str, Any] | None = None,
    ) -> Message:
        """发送子频道消息（``POST /channels/{channel_id}/messages``）。

        ``content`` / ``embed`` / ``ark`` / ``image`` / ``markdown`` 至少填一个。
        """
        data = await self._request(
            'POST',
            f'/channels/{channel_id}/messages',
            json_body=self._channel_message_body(
                content=content,
                embed=embed,
                ark=ark,
                image=image,
                msg_id=msg_id,
                event_id=event_id,
                markdown=markdown,
                message_reference=message_reference,
            ),
        )
        return Message.model_validate(data)

    async def get_channel_message(self, channel_id: str, message_id: str) -> Message:
        """获取子频道消息（``GET /channels/{channel_id}/messages/{message_id}``）。"""
        data = await self._request('GET', f'/channels/{channel_id}/messages/{message_id}')
        return Message.model_validate(data)

    async def recall_channel_message(self, channel_id: str, message_id: str, *, hidetip: bool = False) -> None:
        """撤回子频道消息（``DELETE /channels/{channel_id}/messages/{message_id}``）。"""
        await self._request('DELETE', f'/channels/{channel_id}/messages/{message_id}', params={'hidetip': hidetip})

    async def create_dm_session(self, recipient_id: str, source_guild_id: str) -> DMS:
        """创建频道私信会话（``POST /users/@me/dms``）。"""
        data = await self._request(
            'POST',
            '/users/@me/dms',
            json_body=_compact(recipient_id=recipient_id, source_guild_id=source_guild_id),
        )
        return DMS.model_validate(data)

    async def send_dm_message(
        self,
        guild_id: str,
        *,
        content: str | None = None,
        embed: dict[str, Any] | None = None,
        ark: dict[str, Any] | None = None,
        image: str | None = None,
        msg_id: str | None = None,
        event_id: str | None = None,
        markdown: MessageMarkdown | dict[str, Any] | None = None,
        message_reference: MessageReference | dict[str, Any] | None = None,
    ) -> Message:
        """发送频道私信（``POST /dms/{guild_id}/messages``，参数同子频道消息）。"""
        data = await self._request(
            'POST',
            f'/dms/{guild_id}/messages',
            json_body=self._channel_message_body(
                content=content,
                embed=embed,
                ark=ark,
                image=image,
                msg_id=msg_id,
                event_id=event_id,
                markdown=markdown,
                message_reference=message_reference,
            ),
        )
        return Message.model_validate(data)

    async def recall_dm_message(self, guild_id: str, message_id: str, *, hidetip: bool = False) -> None:
        """撤回频道私信（``DELETE /dms/{guild_id}/messages/{message_id}``）。"""
        await self._request('DELETE', f'/dms/{guild_id}/messages/{message_id}', params={'hidetip': hidetip})

    # ------------------------------------------------------------------
    # 频道成员 / 身份组
    # ------------------------------------------------------------------

    async def get_guild_members(
        self, guild_id: str, *, after: str | None = None, limit: int | None = None
    ) -> list[GuildMember]:
        """获取频道成员列表（``GET /guilds/{guild_id}/members``）。"""
        data = await self._request('GET', f'/guilds/{guild_id}/members', params={'after': after, 'limit': limit})
        items: list[Any] = data or []
        return [GuildMember.model_validate(item) for item in items]

    async def get_guild_member(self, guild_id: str, user_id: str) -> GuildMember:
        """获取频道成员详情（``GET /guilds/{guild_id}/members/{user_id}``）。"""
        data = await self._request('GET', f'/guilds/{guild_id}/members/{user_id}')
        return GuildMember.model_validate(data)

    async def remove_guild_member(
        self,
        guild_id: str,
        user_id: str,
        *,
        add_blacklist: bool | None = None,
        delete_history_msg_days: int | None = None,
    ) -> None:
        """移除频道成员（``DELETE /guilds/{guild_id}/members/{user_id}``）。"""
        await self._request(
            'DELETE',
            f'/guilds/{guild_id}/members/{user_id}',
            json_body=_compact(add_blacklist=add_blacklist, delete_history_msg_days=delete_history_msg_days),
        )

    async def get_guild_roles(self, guild_id: str, *, limit: int | None = None) -> list[Role]:
        """获取频道身份组列表（``GET /guilds/{guild_id}/roles``）。"""
        data = await self._request('GET', f'/guilds/{guild_id}/roles', params={'limit': limit})
        body = _as_body(data)
        if body is not None:
            roles: list[Any] = body.get('roles') or []
            return [Role.model_validate(item) for item in roles]
        items: list[Any] = data or []
        return [Role.model_validate(item) for item in items]

    async def create_guild_role(
        self,
        guild_id: str,
        *,
        name: str | None = None,
        color: int | None = None,
        hoist: int | None = None,
        mentionable: int | None = None,
        **extra: Any,
    ) -> Role:
        """创建频道身份组（``POST /guilds/{guild_id}/roles``）。"""
        data = await self._request(
            'POST',
            f'/guilds/{guild_id}/roles',
            json_body=_compact(name=name, color=color, hoist=hoist, mentionable=mentionable, **extra),
        )
        return Role.model_validate(data)

    async def update_guild_role(
        self,
        guild_id: str,
        role_id: str,
        *,
        name: str | None = None,
        color: int | None = None,
        hoist: int | None = None,
    ) -> Role:
        """修改频道身份组（``PATCH /guilds/{guild_id}/roles/{role_id}``）。"""
        data = await self._request(
            'PATCH',
            f'/guilds/{guild_id}/roles/{role_id}',
            json_body=_compact(name=name, color=color, hoist=hoist),
        )
        return Role.model_validate(data)

    async def delete_guild_role(self, guild_id: str, role_id: str) -> None:
        """删除频道身份组（``DELETE /guilds/{guild_id}/roles/{role_id}``）。"""
        await self._request('DELETE', f'/guilds/{guild_id}/roles/{role_id}')

    async def add_role_member(
        self, guild_id: str, user_id: str, role_id: str, *, channel_id: str | None = None
    ) -> None:
        """添加身份组成员（``PUT /guilds/{guild_id}/members/{user_id}/roles/{role_id}``）。"""
        await self._request(
            'PUT',
            f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
            json_body=_compact(channel_id=channel_id) or None,
        )

    async def remove_role_member(
        self, guild_id: str, user_id: str, role_id: str, *, channel_id: str | None = None
    ) -> None:
        """移除身份组成员（``DELETE /guilds/{guild_id}/members/{user_id}/roles/{role_id}``）。"""
        await self._request(
            'DELETE',
            f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
            json_body=_compact(channel_id=channel_id) or None,
        )

    # ------------------------------------------------------------------
    # 禁言 / 公告 / API 权限
    # ------------------------------------------------------------------

    async def mute_guild(
        self,
        guild_id: str,
        *,
        mute_seconds: str | None = None,
        mute_end_timestamp: str | None = None,
    ) -> None:
        """频道全员禁言（``PATCH /guilds/{guild_id}/mute``，两者只能填一个）。"""
        await self._request(
            'PATCH',
            f'/guilds/{guild_id}/mute',
            json_body=_compact(mute_seconds=mute_seconds, mute_end_timestamp=mute_end_timestamp),
        )

    async def mute_guild_member(
        self,
        guild_id: str,
        user_id: str,
        *,
        mute_seconds: str | None = None,
        mute_end_timestamp: str | None = None,
    ) -> None:
        """指定成员禁言（``PATCH /guilds/{guild_id}/members/{user_id}/mute``）。"""
        await self._request(
            'PATCH',
            f'/guilds/{guild_id}/members/{user_id}/mute',
            json_body=_compact(mute_seconds=mute_seconds, mute_end_timestamp=mute_end_timestamp),
        )

    async def create_guild_announce(
        self,
        guild_id: str,
        *,
        message_id: str | None = None,
        channel_id: str | None = None,
        announces_type: int | None = None,
        recommend_channels: Sequence[RecommendChannel | dict[str, Any]] | None = None,
    ) -> Announce:
        """创建频道公告（``POST /guilds/{guild_id}/announces``）。"""
        data = await self._request(
            'POST',
            f'/guilds/{guild_id}/announces',
            json_body=_compact(
                message_id=message_id,
                channel_id=channel_id,
                announces_type=announces_type,
                recommend_channels=recommend_channels,
            ),
        )
        return Announce.model_validate(data or {})

    async def delete_guild_announce(self, guild_id: str, message_id: str) -> None:
        """删除频道公告（``DELETE /guilds/{guild_id}/announces/{message_id}``）。"""
        await self._request('DELETE', f'/guilds/{guild_id}/announces/{message_id}')

    async def create_channel_announce(
        self,
        channel_id: str,
        *,
        message_id: str | None = None,
        announces_type: int | None = None,
    ) -> Announce:
        """创建子频道公告（``POST /channels/{channel_id}/announces``）。"""
        data = await self._request(
            'POST',
            f'/channels/{channel_id}/announces',
            json_body=_compact(message_id=message_id, announces_type=announces_type),
        )
        return Announce.model_validate(data or {})

    async def delete_channel_announce(self, channel_id: str, message_id: str) -> None:
        """删除子频道公告（``DELETE /channels/{channel_id}/announces/{message_id}``）。"""
        await self._request('DELETE', f'/channels/{channel_id}/announces/{message_id}')

    async def get_api_permission(self, guild_id: str) -> ApiPermissionList:
        """获取频道可用权限列表（``GET /guilds/{guild_id}/api_permission``）。"""
        data = await self._request('GET', f'/guilds/{guild_id}/api_permission')
        return ApiPermissionList.model_validate(data or {})

    async def create_api_permission_demand(
        self, guild_id: str, *, channel_id: str, api_identify: dict[str, Any], desc: str | None = None
    ) -> ApiPermissionDemand:
        """创建频道 API 接口权限授权链接（``POST /guilds/{guild_id}/api_permission/demand``）。

        Args:
            channel_id: 申请授权的子频道 ID。
            api_identify: 形如 ``{"path": "/channels/{channel_id}", "method": "GET"}``。
        """
        data = await self._request(
            'POST',
            f'/guilds/{guild_id}/api_permission/demand',
            json_body=_compact(channel_id=channel_id, api_identify=api_identify, desc=desc),
        )
        return ApiPermissionDemand.model_validate(data or {})

    # ------------------------------------------------------------------
    # 表情表态 / 精华消息 / 日程
    # ------------------------------------------------------------------

    async def add_reaction(self, channel_id: str, message_id: str, emoji_type: int | str, emoji_id: str) -> None:
        """添加表情表态（``PUT /channels/{channel_id}/messages/{message_id}/reactions/{type}/{id}``）。"""
        await self._request('PUT', f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji_type}/{emoji_id}')

    async def delete_reaction(self, channel_id: str, message_id: str, emoji_type: int | str, emoji_id: str) -> None:
        """删除表情表态（``DELETE .../reactions/{type}/{id}``）。"""
        await self._request('DELETE', f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji_type}/{emoji_id}')

    async def get_reactions(
        self, channel_id: str, message_id: str, emoji_type: int | str, emoji_id: str
    ) -> ReactionUsers:
        """获取表情表态用户列表（``GET .../reactions?type=&id=``）。"""
        data = await self._request(
            'GET',
            f'/channels/{channel_id}/messages/{message_id}/reactions',
            params={'type': emoji_type, 'id': emoji_id},
        )
        return ReactionUsers.model_validate(data or {})

    async def add_pin(self, channel_id: str, message_id: str) -> None:
        """添加精华消息（``PUT /channels/{channel_id}/pins/{message_id}``）。"""
        await self._request('PUT', f'/channels/{channel_id}/pins/{message_id}')

    async def delete_pin(self, channel_id: str, message_id: str) -> None:
        """删除精华消息（``DELETE /channels/{channel_id}/pins/{message_id}``）。"""
        await self._request('DELETE', f'/channels/{channel_id}/pins/{message_id}')

    async def get_pins(self, channel_id: str) -> list[Message]:
        """获取精华消息列表（``GET /channels/{channel_id}/pins``）。"""
        data = await self._request('GET', f'/channels/{channel_id}/pins')
        body = _as_body(data)
        source: Any = body.get('items') if body is not None else data
        items: list[Any] = source or []
        return [Message.model_validate(item) for item in items]

    async def get_schedules(self, channel_id: str, *, since: str | None = None) -> list[Schedule]:
        """获取日程列表（``GET /channels/{channel_id}/schedules``）。"""
        data = await self._request('GET', f'/channels/{channel_id}/schedules', params={'since': since})
        body = _as_body(data)
        source: Any = body.get('schedules') if body is not None else data
        items: list[Any] = source or []
        return [Schedule.model_validate(item) for item in items]

    async def create_schedule(self, channel_id: str, schedule: Schedule | dict[str, Any]) -> Schedule:
        """创建日程（``POST /channels/{channel_id}/schedules``）。"""
        data = await self._request('POST', f'/channels/{channel_id}/schedules', json_body=_compact(schedule=schedule))
        return Schedule.model_validate(data or {})

    async def get_schedule(self, channel_id: str, schedule_id: str) -> Schedule:
        """获取日程详情（``GET /channels/{channel_id}/schedules/{schedule_id}``）。"""
        data = await self._request('GET', f'/channels/{channel_id}/schedules/{schedule_id}')
        return Schedule.model_validate(data or {})

    async def update_schedule(self, channel_id: str, schedule_id: str, schedule: Schedule | dict[str, Any]) -> Schedule:
        """修改日程（``PATCH /channels/{channel_id}/schedules/{schedule_id}``）。"""
        data = await self._request(
            'PATCH', f'/channels/{channel_id}/schedules/{schedule_id}', json_body=_compact(schedule=schedule)
        )
        return Schedule.model_validate(data or {})

    async def delete_schedule(self, channel_id: str, schedule_id: str) -> None:
        """删除日程（``DELETE /channels/{channel_id}/schedules/{schedule_id}``）。"""
        await self._request('DELETE', f'/channels/{channel_id}/schedules/{schedule_id}')

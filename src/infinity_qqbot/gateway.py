"""QQ 机器人 WebSocket 网关客户端。

职责：

- 通过 :class:`~infinity_qqbot.api.QQBotAPI` 获取 WSS 接入点与 access_token；
- 完成 ``Hello → Identify/Resume → Heartbeat`` 连接维护流程；
- 断线后自动重连并优先 ``Resume`` 恢复会话（补发遗漏事件）；
- 把 ``Dispatch`` 事件解析为 :class:`QQBotEvent`，供引擎 / 总线消费。

不可恢复的关闭码（4001/4002/401x/4914/4915 等）会抛出
:class:`QQBotGatewayClosed`，上层应停止重试。
"""

from __future__ import annotations

import asyncio
import builtins
import contextlib
import json
import logging
import sys
from collections.abc import AsyncIterator
from typing import Any, cast

import aiohttp
from infinity_bus import EventDeclaration
from pydantic import BaseModel, Field

from .api import QQBotAPI
from .events import resolve_event
from .models import Intents, OpCode, User

logger = logging.getLogger(__name__)

__all__ = [
    'QQBotEvent',
    'QQBotGateway',
    'QQBotGatewayClosed',
    'QQBotGatewayError',
]

#: 不可恢复的网关关闭码（重连无意义）
FATAL_CLOSE_CODES = frozenset({4001, 4002, 4010, 4011, 4012, 4013, 4014, 4914, 4915})


class QQBotGatewayError(RuntimeError):
    """网关协议 / 连接层面的可重试错误。"""


class QQBotGatewayClosed(RuntimeError):
    """网关因不可恢复原因关闭（如无效 shard / intent、机器人下架或封禁）。"""

    def __init__(self, code: int | None, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f'[{code}] {message}' if code is not None else message)


class QQBotEvent(BaseModel):
    """网关下发的单个事件（Dispatch）。"""

    type: str = Field(description='QQ 平台事件类型，如 C2C_MESSAGE_CREATE')
    declaration: builtins.type[EventDeclaration] = Field(description='总线事件声明类（含总线事件名）')
    payload: BaseModel = Field(description='已按声明解析的事件负载')
    raw: dict[str, Any] = Field(default_factory=dict, description='原始 d 数据')
    event_id: str | None = Field(default=None, description='事件 ID')
    sequence: int | None = Field(default=None, description='事件序列号 s，用于 resume')


class QQBotGateway:
    """单分片 WebSocket 网关客户端（自动重连 + 会话恢复）。

    典型用法::

        gateway = QQBotGateway(api, intents=Intents.DEFAULT, shard=(0, 1))
        async for event in gateway.stream():
            ...
    """

    def __init__(
        self,
        api: QQBotAPI,
        *,
        intents: Intents | int = Intents.DEFAULT,
        shard: tuple[int, int] = (0, 1),
        properties: dict[str, str] | None = None,
        auto_reconnect: bool = True,
        reconnect_delay: float = 5.0,
        max_reconnect_delay: float = 60.0,
        receive_slack: float = 3.0,
    ) -> None:
        """初始化网关客户端。

        Args:
            api: OpenAPI 客户端（提供接入点与 access_token）。
            intents: 订阅的 Intents 位标记。
            shard: 分片 ``(id, num)``，无需分片时使用 ``(0, 1)``。
            properties: Identify 中的设备信息（无实际作用，可自定义）。
            auto_reconnect: 断线后是否自动重连。
            reconnect_delay: 初始重连等待秒数（指数退避）。
            max_reconnect_delay: 最大重连等待秒数。
            receive_slack: 接收超时系数：``心跳周期 × 系数`` 内无任何消息则判定连接失效。
        """
        self._api = api
        self._intents = int(intents)
        self._shard = (int(shard[0]), int(shard[1]))
        self._properties = properties or {
            '$os': sys.platform,
            '$browser': 'infinity_qqbot',
            '$device': 'infinity_qqbot',
        }
        self._auto_reconnect = auto_reconnect
        self._reconnect_delay = reconnect_delay
        self._max_reconnect_delay = max_reconnect_delay
        self._receive_slack = receive_slack

        self._session_id: str | None = None
        self._sequence: int | None = None
        self._bot: User | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._closed = False

    # ------------------------------------------------------------------
    # 属性
    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str | None:
        """当前会话 ID（用于 Resume）。"""
        return self._session_id

    @property
    def sequence(self) -> int | None:
        """已收到的最新事件序列号。"""
        return self._sequence

    @property
    def bot(self) -> User | None:
        """READY 中的机器人用户信息。"""
        return self._bot

    @property
    def shard(self) -> tuple[int, int]:
        """当前分片 ``(id, num)``。"""
        return self._shard

    # ------------------------------------------------------------------
    # 事件流
    # ------------------------------------------------------------------

    async def stream(self) -> AsyncIterator[QQBotEvent]:
        """连接网关并持续产出事件（自动重连，直到 :meth:`close`）。"""
        delay = self._reconnect_delay
        while not self._closed:
            try:
                async for event in self._run():
                    if self._closed:
                        break
                    delay = self._reconnect_delay
                    yield event
            except QQBotGatewayClosed:
                raise
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # 网络层错误统一重连
                logger.warning('QQBot 网关连接异常：%s', exc)
            if self._closed or not self._auto_reconnect:
                break
            logger.info(
                'QQBot 网关将在 %.1f 秒后重连（resume=%s）',
                delay,
                self._session_id is not None,
            )
            await asyncio.sleep(delay)
            delay = min(delay * 2, self._max_reconnect_delay)

    async def close(self) -> None:
        """关闭网关连接并终止事件流。"""
        self._closed = True
        ws = self._ws
        if ws is not None and not ws.closed:
            await ws.close()

    # ------------------------------------------------------------------
    # 连接维护
    # ------------------------------------------------------------------

    async def _run(self) -> AsyncIterator[QQBotEvent]:
        """建立一次完整连接并处理下行消息，直到连接结束。"""
        gateway = await self._api.get_gateway_bot()
        token = f'QQBot {await self._api.get_access_token()}'
        session = await self._api.ensure_session()
        ws = await session.ws_connect(
            gateway.url,
            ssl=self._api.ssl_context,
            heartbeat=None,
            max_msg_size=0,
        )
        self._ws = ws
        heartbeat_task: asyncio.Task[None] | None = None
        try:
            hello = await self._receive_payload(ws, timeout=30.0)
            if hello is None:
                raise QQBotGatewayError('网关在鉴权前关闭了连接')
            if hello.get('op') != OpCode.HELLO:
                raise QQBotGatewayError(f'网关首包不是 Hello：{hello!r}')
            hello_data: dict[str, Any] = cast(dict[str, Any], hello.get('d') or {})
            interval = float(hello_data.get('heartbeat_interval', 45000)) / 1000.0
            logger.debug('网关心跳周期：%.1f 秒', interval)

            # ---- 鉴权：优先 Resume，否则全新 Identify ----
            if self._session_id is not None and self._sequence is not None:
                await ws.send_json(
                    {
                        'op': int(OpCode.RESUME),
                        'd': {'token': token, 'session_id': self._session_id, 'seq': self._sequence},
                    }
                )
                logger.info('QQBot 网关尝试恢复会话 session_id=%s', self._session_id)
            else:
                await ws.send_json(
                    {
                        'op': int(OpCode.IDENTIFY),
                        'd': {
                            'token': token,
                            'intents': self._intents,
                            'shard': [self._shard[0], self._shard[1]],
                            'properties': self._properties,
                        },
                    }
                )
                logger.info('QQBot 网关已发送 Identify（intents=%s, shard=%s）', self._intents, self._shard)

            heartbeat_task = asyncio.create_task(self._heartbeat_loop(ws, interval), name='infinity_qqbot.heartbeat')
            timeout = max(interval * self._receive_slack, 30.0)

            while not self._closed:
                try:
                    payload = await self._receive_payload(ws, timeout=timeout)
                except TimeoutError:
                    logger.warning('QQBot 网关 %.0f 秒未收到任何消息（含心跳 ACK），主动重连', timeout)
                    break
                if payload is None:
                    logger.info('QQBot 网关连接关闭（code=%s）', ws.close_code)
                    break

                op = payload.get('op')
                if op == OpCode.DISPATCH:
                    s = payload.get('s')
                    if isinstance(s, int):
                        self._sequence = s
                    t = payload.get('t')
                    data = payload.get('d')
                    if t == 'READY' and isinstance(data, dict):
                        ready = cast(dict[str, Any], data)
                        session_id = ready.get('session_id')
                        if isinstance(session_id, str):
                            self._session_id = session_id
                        user = ready.get('user')
                        if isinstance(user, dict):
                            self._bot = User.model_validate(user)
                        logger.info('QQBot 网关就绪：bot=%s', self._bot.username if self._bot else None)
                    elif t == 'RESUMED':
                        logger.info('QQBot 网关会话已恢复')
                    decl, model = resolve_event(str(t), data)
                    yield QQBotEvent(
                        type=str(t),
                        declaration=decl,
                        payload=model,
                        raw=cast(dict[str, Any], data) if isinstance(data, dict) else {'raw_data': data},
                        event_id=payload.get('id'),
                        sequence=self._sequence,
                    )
                elif op == OpCode.HEARTBEAT_ACK:
                    continue
                elif op == OpCode.HEARTBEAT:
                    # 服务端要求立即心跳
                    await ws.send_json({'op': int(OpCode.HEARTBEAT), 'd': self._sequence})
                elif op == OpCode.RECONNECT:
                    logger.info('QQBot 网关通知重连')
                    break
                elif op == OpCode.INVALID_SESSION:
                    resumable = bool(payload.get('d'))
                    if not resumable:
                        # 会话不可恢复：清空会话状态，下次连接走 Identify
                        self._session_id = None
                        self._sequence = None
                    logger.warning('QQBot 网关会话失效（resumable=%s）', resumable)
                    await asyncio.sleep(1.0)
                    break
                elif op == OpCode.HELLO:
                    continue
                else:
                    logger.debug('忽略未知 op=%s 的网关消息', op)
        finally:
            if heartbeat_task is not None:
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task
            self._ws = None
            if not ws.closed:
                await ws.close()

        # 正常退出循环后检查是否因致命关闭码断开
        close_code = ws.close_code
        if close_code in FATAL_CLOSE_CODES and not self._closed:
            raise QQBotGatewayClosed(close_code, '网关以不可恢复的关闭码断开')

    async def _heartbeat_loop(self, ws: aiohttp.ClientWebSocketResponse, interval: float) -> None:
        """按周期发送 OpCode 1 心跳，``d`` 为已收到的最新序列号。"""
        try:
            while True:
                await ws.send_json({'op': int(OpCode.HEARTBEAT), 'd': self._sequence})
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # 发送失败交给接收侧超时处理
            logger.debug('QQBot 心跳发送失败：%s', exc)

    @staticmethod
    async def _receive_payload(ws: aiohttp.ClientWebSocketResponse, *, timeout: float) -> dict[str, Any] | None:
        """接收一条 JSON 消息；连接关闭时返回 ``None``，协议异常时抛错。"""
        msg = await asyncio.wait_for(ws.receive(), timeout=timeout)
        if msg.type == aiohttp.WSMsgType.TEXT:
            payload: Any = json.loads(msg.data)
            if not isinstance(payload, dict):
                raise QQBotGatewayError(f'网关消息不是 JSON 对象：{msg.data!r}')
            return cast(dict[str, Any], payload)
        if msg.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.CLOSING,
        ):
            return None
        if msg.type == aiohttp.WSMsgType.ERROR:
            raise QQBotGatewayError(f'网关连接异常：{ws.exception()!r}')
        raise QQBotGatewayError(f'收到不支持的网关消息类型：{msg.type!r}')

"""冒烟测试：不联网验证核心链路。

覆盖：

1. 模型分包导出、事件声明自动收集（ModuleEventRegister）与 RPC 显式事件生成；
2. access_token 缓存与强制刷新；
3. 强类型 RPC：生成的客户端 ``send_c2c_message`` → ``QQBotAPIHandler`` → ``QQBotAPI``
   （含平台错误码跨总线保留）；
4. 事件发布：``register_handlers``（ModuleHandlerRegister）→ 网关事件发布到总线；
5. 幂等去重：相同事件 ID 的重复推送只发布一次（IdempotencyRecorder）；
6. ``wait_for_event``（expect 模板）等待首个匹配事件。

运行::

    python tests/smoke.py
"""

from __future__ import annotations

import asyncio
import io
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from infinity_bus import Event, EventBus, EventDeclaration, EventHandler, EventHandlerRegistry, EventRegistry, Regex
from infinity_bus.templates import InMemoryIdempotencyRecorder
from pydantic import BaseModel

from infinity_qqbot import (
    ALL_EVENTS,
    AccessTokenResponse,
    C2CMessageCreateEvent,
    C2CMsgReceiveEvent,
    FriendAddEvent,
    FriendEventPayload,
    GroupAddRobotEvent,
    GroupAtMessageCreateEvent,
    GroupBotState,
    GroupDelRobotEvent,
    GroupInfo,
    GroupMemberAddEvent,
    GroupMemberEventPayload,
    GroupMemberRemoveEvent,
    GroupMsgReceiveEvent,
    GroupRobotEventPayload,
    JoinRequest,
    MediaImagePage,
    MessageCard,
    MessageCardContent,
    MessageResponse,
    MsgReceiveSwitchEventPayload,
    ParallelMessage,
    QQBotAPI,
    QQBotAPIError,
    QQBotAPIHandler,
    QQBotEvent,
    RestrictChatSetting,
    SendC2CMessageRequest,
    SendC2CMessageRequestEvent,
    SendC2CMessageResponseEvent,
    SendGroupMessageRequest,
    UnknownEvent,
    UnknownEventPayload,
    UserInfo,
    qqbot_events,
    register_handlers,
    resolve_event,
    send_c2c_message,
    wait_for_event,
)

# 输出被重定向的环境（如 Windows CI）默认使用非 UTF-8 编码（cp1252 等），
# 直接打印中文会抛 UnicodeEncodeError；统一强制 stdout/stderr 为 UTF-8。
for _stream in (sys.stdout, sys.stderr):
    if isinstance(_stream, io.TextIOWrapper) and _stream.encoding and 'utf' not in _stream.encoding.lower():
        _stream.reconfigure(encoding='utf-8', errors='replace')


def check_declarations() -> None:
    """模型分包、网关事件与 RPC 事件声明接线。"""
    assert C2CMessageCreateEvent.name == 'qqbot.event.c2c_message_create'
    assert C2CMessageCreateEvent.payload_type is C2CMessageCreateEvent.Payload

    decl, payload = resolve_event('C2C_MESSAGE_CREATE', {'id': 'm1', 'content': 'hi', 'user_openid': 'u1'})
    assert decl is C2CMessageCreateEvent, decl
    assert isinstance(payload, C2CMessageCreateEvent.Payload)
    assert payload.user_openid == 'u1' and payload.content == 'hi', payload

    decl2, payload2 = resolve_event('BRAND_NEW_EVENT', {'a': 1})
    assert decl2 is UnknownEvent
    assert isinstance(payload2, UnknownEventPayload)
    assert payload2.type == 'BRAND_NEW_EVENT' and payload2.data == {'a': 1}

    decl3, payload3 = resolve_event('RESUMED', '')
    assert getattr(decl3, 'type_name', None) == 'RESUMED' and getattr(payload3, 'raw_data', '') == '', payload3

    # ModuleEventRegister 自动收集：QQ 网关事件是其子集
    assert set(ALL_EVENTS) <= set(qqbot_events.events)
    assert len(ALL_EVENTS) >= 50, len(ALL_EVENTS)

    # 每个网关事件声明的 name 与 type_name 一致
    for decl in ALL_EVENTS:
        decl_type_name = getattr(decl, 'type_name', None)
        assert decl_type_name is None or decl.name == f'qqbot.event.{decl_type_name.lower()}', decl

    # RPC 事件为显式生成的声明（含嵌套 Payload 别名）
    assert SendC2CMessageRequestEvent.name == 'qqbot.api.send_c2c_message.request'
    assert SendC2CMessageResponseEvent.name == 'qqbot.api.send_c2c_message.response'
    assert SendC2CMessageRequestEvent.payload_type is SendC2CMessageRequest

    print('[ok] 模型分包、事件自动收集与 RPC 显式事件')


def check_management_event_payloads() -> None:
    """管理类事件（入群 / 成员 / 消息开关 / 好友）的整数时间戳（Unix 秒）解析。"""
    cases: list[tuple[str, type[EventDeclaration], int]] = [
        ('GROUP_ADD_ROBOT', GroupAddRobotEvent, 1791972342),
        ('GROUP_DEL_ROBOT', GroupDelRobotEvent, 1784570535),
        ('GROUP_MEMBER_ADD', GroupMemberAddEvent, 1784276757),
        ('GROUP_MEMBER_REMOVE', GroupMemberRemoveEvent, 1784276759),
        ('GROUP_MSG_RECEIVE', GroupMsgReceiveEvent, 1784276800),
        ('FRIEND_ADD', FriendAddEvent, 1784570523),
        ('C2C_MSG_RECEIVE', C2CMsgReceiveEvent, 1784570617),
    ]
    for type_name, decl, timestamp in cases:
        resolved, payload = resolve_event(type_name, {'timestamp': timestamp})
        assert resolved is decl, (type_name, resolved)
        assert isinstance(
            payload,
            (FriendEventPayload, GroupMemberEventPayload, GroupRobotEventPayload, MsgReceiveSwitchEventPayload),
        ), type_name
        assert payload.timestamp == timestamp, type_name
    print('[ok] 管理类事件整数时间戳（Unix 秒）解析')


def check_group_message_payload_fields() -> None:
    """群聊消息新增字段：member_nickname / group_id / parallel_message。"""
    legacy: dict[str, Any] = {
        'id': 'm-old',
        'author': {'id': 'member-1', 'username': '示例昵称', 'member_openid': 'member-1', 'member_role': 'owner'},
        'content': '你好～',
        'timestamp': '2026-10-16T23:47:16+08:00',
        'message_type': 0,
        'group_openid': 'group-1',
    }
    _, payload = resolve_event('GROUP_AT_MESSAGE_CREATE', legacy)
    assert isinstance(payload, GroupAtMessageCreateEvent.Payload)
    assert payload.author is not None and payload.author.member_nickname is None
    assert payload.group_id is None and payload.parallel_message is None

    plain: dict[str, Any] = {
        **legacy,
        'id': 'm-plain',
        'author': {
            'id': 'member-1',
            'username': '示例昵称',
            'avatar': None,
            'bot': False,
            'union_openid': '',
            'member_openid': 'member-1',
            'member_role': 'admin',
            'member_nickname': '示例昵称',
        },
        'timestamp': '2026-11-20T22:33:23+08:00',
        'message_scene': {'source': 'default', 'ext': ['msg_idx=idx-1', 'auth_token=token']},
        'group_id': 'group-1',
        'union_group_openid': 'union-group-1',
        'mentions': [
            {'id': 'member-2', 'username': '小明', 'member_openid': 'member-2', 'is_you': False, 'scope': 'single'}
        ],
    }
    _, payload = resolve_event('GROUP_AT_MESSAGE_CREATE', plain)
    assert isinstance(payload, GroupAtMessageCreateEvent.Payload)
    assert payload.author is not None
    assert payload.author.member_nickname == '示例昵称' and payload.author.member_role == 'admin'
    assert payload.group_id == payload.group_openid == 'group-1'
    assert payload.union_group_openid == 'union-group-1'
    assert payload.mentions[0].is_you is False and payload.mentions[0].scope == 'single'
    assert payload.parallel_message is None

    quoted: dict[str, Any] = {
        **plain,
        'id': 'm-quoted',
        'content': '我喜欢你',
        'timestamp': '2026-11-20T22:51:43+08:00',
        'message_type': 103,
        'message_scene': {'source': 'default', 'ext': ['ref_msg_idx=ref-1', 'msg_idx=idx-2', 'auth_token=token']},
        'msg_elements': [
            {
                'msg_idx': 'ref-1',
                'author': None,
                'message_type': 103,
                'content': '被引用的机器人回复内容',
                'attachments': [],
                'ark_data': None,
                'msg_elements': [],
            }
        ],
        'parallel_message': {'msg_nodes': [{'content': '@示例昵称 被引用的机器人回复内容', 'message_type': 0}]},
    }
    _, payload = resolve_event('GROUP_AT_MESSAGE_CREATE', quoted)
    assert isinstance(payload, GroupAtMessageCreateEvent.Payload)
    assert payload.message_type == 103 and payload.msg_elements[0].msg_idx == 'ref-1'
    parallel = payload.parallel_message
    assert isinstance(parallel, ParallelMessage)
    assert [node.content for node in parallel.msg_nodes] == ['@示例昵称 被引用的机器人回复内容']
    assert [node.message_type for node in parallel.msg_nodes] == [0]
    print('[ok] 群聊消息新增字段（member_nickname / group_id / parallel_message）')


def check_official_model_fields() -> None:
    """官方文档新增字段：群信息 / 群状态 / 禁言 / 入群申请 / 用户信息 / 素材 / 图文卡片。"""
    info = GroupInfo.model_validate(
        {
            'group_openid': 'group-1',
            'group_name': '读书分享会',
            'group_tags': ['阅读'],
            'group_member_num': 256,
            'union_group_openid': 'union-group-1',
        }
    )
    assert info.union_group_openid == 'union-group-1'

    state = GroupBotState.model_validate(
        {
            'member_openid': 'bot-1',
            'joined_at': '2026-08-01T12:00:00+08:00',
            'allow_proactive_msg': False,
            'recv_msg_setting': 'only_mention',
            'member_role': 'admin',
        }
    )
    assert state.recv_msg_setting == 'only_mention' and state.allow_proactive_msg is False

    setting = RestrictChatSetting.model_validate(
        {
            'global_rule': {
                'mode': 'schedule',
                'schedule_rules': [{'task_id': 'task-1', 'start_at': '2026-07-22T10:44:00+08:00', 'enabled': True}],
                'recurring_rules': [
                    {'task_id': 'task-2', 'weekdays': [1, 2], 'start_time': '13:00', 'end_time': '14:00'}
                ],
            },
            'members': [
                {'member_openid': 'member-2', 'username': 'T小不点', 'mute_expire_at': '2026-08-05T11:23:04+08:00'}
            ],
        }
    )
    assert setting.global_rule is not None and setting.global_rule.mode == 'schedule'
    assert setting.global_rule.schedule_rules[0].task_id == 'task-1'
    assert setting.global_rule.recurring_rules[0].weekdays == [1, 2]
    assert setting.members[0].member_openid == 'member-2'

    join = JoinRequest.model_validate(
        {
            'join_request_id': 'req-1',
            'member_openid': 'member-3',
            'username': '申请人',
            'apply_at': '2026-08-05T16:21:40+08:00',
            'apply_source': 'self_apply',
            'verify_info': {'method': 'verify_message', 'verify_message': '你好'},
            'auto_approved': {'strategy_id': 'st-1'},
        }
    )
    assert join.auto_approved is not None and join.auto_approved.strategy_id == 'st-1'
    assert join.verify_info is not None and join.verify_info.method == 'verify_message'

    user = UserInfo.model_validate(
        {'username': '笑😊心❤️', 'avatar': 'https://example.com/a.png', 'allow_proactive_msg': True}
    )
    assert user.allow_proactive_msg is True

    page = MediaImagePage.model_validate(
        {
            'images': [
                {
                    'image_id': 'image-1',
                    'url': 'qqbot-media://image/v1/token',
                    'file_name': 'kline.png',
                    'created_at': 1792051409,
                    'expires_at': 1792656210,
                }
            ],
            'next_cursor': '',
            'total': 1,
        }
    )
    assert page.total == 1 and page.images[0].url == 'qqbot-media://image/v1/token'

    card = MessageCard(
        type='tuwen',
        content=MessageCardContent(
            title='iPhone 17 Pro 正式发布',
            description='全新芯片 / 钛金属机身',
            url='https://news.qq.com/example',
            pic_url='https://inews.gtimg.com/example.jpg',
        ),
    )
    request = SendGroupMessageRequest(
        session_id='session-1', request_id='request-1', group_openid='group-1', msg_type=8, card=card
    )
    assert request.model_dump(exclude_none=True)['card']['content']['title'] == 'iPhone 17 Pro 正式发布'
    print('[ok] 官方文档新增字段与图文卡片模型')


async def check_new_api_methods() -> None:
    """用户信息与素材管理 API 路径与响应解析。"""
    api = QQBotAPI('appid', 'secret')
    calls: list[tuple[str, str, Any, Any]] = []

    async def fake_request(method: str, path: str, **kwargs: Any) -> Any:
        calls.append((method, path, kwargs.get('json_body'), kwargs.get('params')))
        if path == '/v2/users/u1/info':
            return {'username': '示例', 'avatar': 'https://example.com/a.png', 'allow_proactive_msg': True}
        if path == '/v2/media-images/prepare':
            return {'upload_id': 'u1', 'presigned_url': 'https://upload.example', 'expires_in': 3600}
        if path == '/v2/media-images/complete':
            return {
                'image_id': 'image-1',
                'url': 'qqbot-media://image/v1/token',
                'ttl': 7776000,
                'preview_url': 'https://preview.example',
            }
        if path == '/v2/media-images':
            return {
                'images': [{'image_id': 'image-1', 'url': 'qqbot-media://image/v1/token'}],
                'next_cursor': '',
                'total': 1,
            }
        return {}

    api._request = fake_request  # type: ignore[method-assign]

    user = await api.get_user_info('u1')
    assert user.username == '示例' and user.allow_proactive_msg is True
    prepared = await api.media_image_prepare(
        file_name='kline.png', file_size=40156, content_type='image/png', md5='md5', sha1='sha1'
    )
    assert prepared.upload_id == 'u1' and prepared.expires_in == 3600
    completed = await api.media_image_complete(upload_id='u1', md5='md5')
    assert completed.image_id == 'image-1' and completed.ttl == 7776000
    page = await api.get_media_images()
    assert page.total == 1 and page.images[0].image_id == 'image-1'
    await api.delete_media_image('image-1')
    await api.close()

    assert calls[0] == ('GET', '/v2/users/u1/info', None, None), calls[0]
    assert calls[1][:2] == ('POST', '/v2/media-images/prepare'), calls[1]
    assert calls[1][2]['content_type'] == 'image/png', calls[1]
    assert calls[2][:2] == ('POST', '/v2/media-images/complete'), calls[2]
    assert calls[3][:2] == ('GET', '/v2/media-images'), calls[3]
    assert calls[4][:2] == ('DELETE', '/v2/media-images/image-1/delete'), calls[4]
    print('[ok] 用户信息与素材管理接口')


async def check_token_cache() -> None:
    """access_token 缓存与强制刷新。"""
    api = QQBotAPI('appid', 'secret')
    calls: list[int] = []

    async def fake_fetch() -> AccessTokenResponse:
        calls.append(1)
        return AccessTokenResponse(access_token=f'token-{len(calls)}', expires_in=7200)

    api.fetch_access_token = fake_fetch  # type: ignore[method-assign]

    first = await api.get_access_token()
    second = await api.get_access_token()
    assert first == second == 'token-1' and len(calls) == 1, (first, second, calls)

    third = await api.get_access_token(force=True)
    assert third == 'token-2' and len(calls) == 2, (third, calls)

    await api.close()
    await api.close()  # 无会话时 close 应幂等
    print('[ok] access_token 缓存')


async def check_typed_rpc() -> None:
    """强类型 RPC 全链路（含平台错误码跨总线保留）。"""
    registry = EventRegistry()
    qqbot_events.register_all_events(registry)

    api = QQBotAPI('appid', 'secret')
    calls: list[tuple[str, str]] = []

    async def fake_request(method: str, path: str, **kwargs: Any) -> Any:
        calls.append((method, path))
        return {'id': 'reply-1', 'timestamp': '2026-10-09T12:00:00+08:00'}

    api._request = fake_request  # type: ignore[method-assign]

    handlers = EventHandlerRegistry()
    await handlers.register(QQBotAPIHandler(api))

    async with EventBus(registry, handlers) as bus:
        message = await send_c2c_message(
            bus.proxy('smoke'),
            user_openid='u1',
            content='hello',
            msg_id='m1',
        )
        assert isinstance(message, MessageResponse), message
        assert message.id == 'reply-1'
        assert calls == [('POST', '/v2/users/u1/messages')], calls

        async def failing_request(method: str, path: str, **kwargs: Any) -> Any:
            raise QQBotAPIError(40034005, '回复消息msg_id已过期')

        api._request = failing_request  # type: ignore[method-assign]
        try:
            await send_c2c_message(bus.proxy('smoke'), user_openid='u1', content='hi')
        except QQBotAPIError as exc:
            assert exc.code is None and '40034005' in str(exc), exc
        else:
            raise AssertionError('平台错误应抛出 QQBotAPIError')

    print('[ok] 强类型 RPC 与错误码跨总线')


class FakeEngine:
    """模拟 QQBot 引擎：事件通过内部队列按需推送。"""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[QQBotEvent] = asyncio.Queue()
        self.closed = False

    def push(self, event: QQBotEvent) -> None:
        """向事件流推送一条事件。"""
        self._queue.put_nowait(event)

    async def stream(self):
        while True:
            yield await self._queue.get()

    async def close(self) -> None:
        self.closed = True


def c2c_event(message_id: str, content: str, *, event_id: str, sequence: int) -> QQBotEvent:
    """构造一条 C2C_MESSAGE_CREATE 网关事件。"""
    return QQBotEvent(
        type='C2C_MESSAGE_CREATE',
        declaration=C2CMessageCreateEvent,
        payload=C2CMessageCreateEvent.Payload(id=message_id, content=content, user_openid='u1'),
        raw={'id': message_id},
        event_id=event_id,
        sequence=sequence,
    )


class Collector(EventHandler):
    """收集总线上发布的所有 qqbot 网关事件。"""

    def __init__(self) -> None:
        super().__init__(subscriptions=[Regex(r'qqbot\.event\..*')])
        self.names: list[str] = []
        self.payloads: list[Any] = []

    async def handle(self, payload: BaseModel | None, bus_proxy: EventBus.Proxy, raw_event: Event) -> None:
        self.names.append(raw_event.name)
        self.payloads.append(payload)


async def check_events() -> None:
    """批量注册、事件发布、幂等去重与 wait_for_event。"""
    registry = EventRegistry()
    qqbot_events.register_all_events(registry)

    api = QQBotAPI('appid', 'secret')  # 不会真正联网（注入 FakeEngine）
    engine = FakeEngine()
    collector = Collector()

    handlers = EventHandlerRegistry()
    await handlers.register(collector)
    await register_handlers(  # ModuleHandlerRegister 批量注册入站 + RPC 处理器
        handlers,
        api,
        engine=engine,  # type: ignore[arg-type]
        dedup_recorder=InMemoryIdempotencyRecorder(),
    )

    async with EventBus(registry, handlers) as bus:
        waiter = asyncio.create_task(wait_for_event(bus.proxy('smoke'), C2CMessageCreateEvent.name, timeout=2.0))
        await asyncio.sleep(0.1)  # 让等待者先完成注册

        # 相同 event_id 的重复推送应被幂等去重
        engine.push(c2c_event('m1', 'hi', event_id='evt-1', sequence=1))
        engine.push(c2c_event('m1', 'hi', event_id='evt-1', sequence=2))
        engine.push(c2c_event('m2', 'yo', event_id='evt-2', sequence=3))

        waited = await waiter
        assert isinstance(waited.data, C2CMessageCreateEvent.Payload)
        assert waited.data.content == 'hi'

        await asyncio.sleep(0.3)
        assert collector.names == ['qqbot.event.c2c_message_create'] * 2, collector.names
        assert [p.id for p in collector.payloads] == ['m1', 'm2'], collector.payloads

    await asyncio.sleep(0.1)
    print('[ok] 批量注册、事件发布、幂等去重与 wait_for_event')


async def main() -> None:
    check_declarations()
    check_management_event_payloads()
    check_group_message_payload_fields()
    check_official_model_fields()
    await check_new_api_methods()
    await check_token_cache()
    await check_typed_rpc()
    await check_events()
    print('\n全部冒烟测试通过 ✔')


if __name__ == '__main__':
    asyncio.run(main())

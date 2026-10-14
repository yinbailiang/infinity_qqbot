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
    GroupDelRobotEvent,
    GroupMemberAddEvent,
    GroupMemberEventPayload,
    GroupMemberRemoveEvent,
    GroupMsgReceiveEvent,
    GroupRobotEventPayload,
    MessageResponse,
    MsgReceiveSwitchEventPayload,
    QQBotAPI,
    QQBotAPIError,
    QQBotAPIHandler,
    QQBotEvent,
    SendC2CMessageRequest,
    SendC2CMessageRequestEvent,
    SendC2CMessageResponseEvent,
    UnknownEvent,
    UnknownEventPayload,
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
    await check_token_cache()
    await check_typed_rpc()
    await check_events()
    print('\n全部冒烟测试通过 ✔')


if __name__ == '__main__':
    asyncio.run(main())

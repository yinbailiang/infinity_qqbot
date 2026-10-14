"""事件总线集成：入站事件发布与处理器组装。

- :class:`QQBotEventHandler`：接受 :class:`~infinity_qqbot.api.QQBotAPI`，
  在总线激活时自动连接 QQ 网关，把每个事件发布为 ``qqbot.event.<type>``
  （如 ``qqbot.event.c2c_message_create``），停机 / 注销时自动断开；
  可选注入 ``IdempotencyRecorder``（幂等模板）按事件 ID 去重，防止 QQ 重复推送；
- :func:`register_handlers`：基于 ``ModuleHandlerRegister`` 批量注册
  :class:`QQBotEventHandler` 与强类型 RPC 处理器
  :class:`~infinity_qqbot.rpc.handlers.QQBotAPIHandler`（见 :mod:`infinity_qqbot.rpc`）；
- :func:`wait_for_event`：一次性等待匹配事件（底层使用 ``expect`` 模板）。

典型接线::

    from infinity_bus import EventBus, EventHandlerRegistry, EventRegistry

    from infinity_qqbot import qqbot_events, register_handlers, send_c2c_message

    registry = EventRegistry()
    qqbot_events.register_all_events(registry)   # 注册全部事件声明（网关事件 + RPC 事件）

    handlers = EventHandlerRegistry()
    await register_handlers(handlers, api)       # 入站发布 + 强类型 RPC 处理器

    async with EventBus(registry, handlers) as bus:
        message = await send_c2c_message(
            bus.proxy('app'),
            user_openid=openid,
            content='hello',
            msg_id=msg_id,
        )
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from infinity_bus import BusShuttingDown, Event, EventBus, EventHandler, EventHandlerRegistry, Regex
from infinity_bus.templates import IdempotencyRecorder, ModuleHandlerRegister, expect

from .api import QQBotAPI
from .engine import QQBot
from .events import UnknownEvent
from .gateway import QQBotEvent, QQBotGatewayClosed
from .models import Intents
from .rpc import QQBotAPIHandler

logger = logging.getLogger(__name__)

__all__ = [
    'QQBotEventHandler',
    'register_handlers',
    'wait_for_event',
]


class QQBotEventHandler(EventHandler):
    """QQBot 事件处理器：把网关事件自动发布到事件总线。

    在 ``on_activate`` 时启动后台事件泵连接网关，在 ``on_deactivate``
    时取消；事件按 ``qqbot.event.<type 小写>`` 发布，未建模事件走
    ``qqbot.event.unknown`` 兜底。
    """

    def __init__(
        self,
        api: QQBotAPI,
        *,
        intents: Intents | int = Intents.DEFAULT,
        shard: tuple[int, int] = (0, 1),
        properties: dict[str, str] | None = None,
        engine: QQBot | None = None,
        event_filter: Callable[[QQBotEvent], bool] | None = None,
        publish_unknown: bool = True,
        dedup_recorder: IdempotencyRecorder | None = None,
        dedup_consumer: str = 'infinity_qqbot.gateway',
    ) -> None:
        """初始化事件处理器。

        Args:
            api: OpenAPI 客户端（用于获取接入点与 access_token）。
            intents: 订阅的 Intents 位标记。
            shard: 分片 ``(id, num)``。
            properties: Identify 设备信息。
            engine: 自定义引擎（默认按参数创建 :class:`QQBot`，测试时可注入）。
            event_filter: 事件过滤器，返回 ``False`` 的事件不发布。
            publish_unknown: 未建模事件是否发布到 ``qqbot.event.unknown``。
            dedup_recorder: 幂等记录器（``IdempotencyRecorder``，如
                ``InMemoryIdempotencyRecorder`` / ``SqliteIdempotencyRecorder``）；
                传入后按事件 ID 去重，防止 QQ 重复推送（发布成功才记录）。
            dedup_consumer: 幂等去重的消费方标识。
        """
        super().__init__(subscriptions=None)
        self._api = api
        self._engine = engine or QQBot(api, intents=intents, shard=shard, properties=properties)
        self._event_filter = event_filter
        self._publish_unknown = publish_unknown
        self._dedup = dedup_recorder
        self._dedup_consumer = dedup_consumer
        self._task: asyncio.Task[None] | None = None

    # ------------------------------------------------------------------
    # 属性
    # ------------------------------------------------------------------

    @property
    def api(self) -> QQBotAPI:
        """底层 OpenAPI 客户端。"""
        return self._api

    @property
    def engine(self) -> QQBot:
        """底层 QQBot 引擎。"""
        return self._engine

    # ------------------------------------------------------------------
    # 生命周期：随总线激活 / 注销
    # ------------------------------------------------------------------

    async def on_activate(self, bus: EventBus) -> None:
        """被注册表激活时启动事件泵（自动连接网关）。"""
        await super().on_activate(bus)
        proxy = bus.proxy(f'{type(self).__name__}:gateway')
        self._task = asyncio.create_task(self._pump(proxy), name='infinity_qqbot.event_pump')

    async def on_deactivate(self, bus: EventBus) -> None:
        """被注销 / 总线停机时停止事件泵（等待其收敛后撤销订阅）。"""
        await self._stop_pump()
        await super().on_deactivate(bus)

    async def aclose(self) -> None:
        """显式关闭事件泵并断开网关连接（用于手动管理生命周期）。"""
        await self._stop_pump()
        await self._engine.close()

    async def handle(
        self,
        payload: Any,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> None:
        """事件处理器入口。

        本处理器是纯事件生产者（订阅为空），该方法不会被总线调用；
        保留实现仅为满足 :class:`~infinity_bus.EventHandler` 抽象协议。
        """

    # ------------------------------------------------------------------
    # 事件泵
    # ------------------------------------------------------------------

    async def _stop_pump(self) -> None:
        """取消事件泵并等待其收敛（避免停机后残留野任务）。"""
        task, self._task = self._task, None
        if task is not None and not task.done():
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

    async def _pump(self, proxy: EventBus.Proxy) -> None:
        """持续消费网关事件并发布到总线。"""
        try:
            async for event in self._engine.stream():
                if not self._accept(event):
                    continue
                declaration = event.declaration
                if declaration is UnknownEvent and not self._publish_unknown:
                    continue
                if await self._is_duplicate(event):
                    continue
                await proxy.publish(declaration.name, event.payload)
                await self._mark_processed(event)
        except asyncio.CancelledError:
            raise
        except QQBotGatewayClosed as exc:
            logger.error('QQBot 网关已关闭且不可恢复，事件泵停止：%s', exc)
        except BusShuttingDown:
            logger.debug('事件总线停机，QQBot 事件泵退出')
        except Exception:  # 后台任务兜底，避免静默死亡
            logger.exception('QQBot 事件泵异常退出')

    def _accept(self, event: QQBotEvent) -> bool:
        if self._event_filter is None:
            return True
        try:
            return bool(self._event_filter(event))
        except Exception:  # 过滤器异常不应拖垮事件泵
            logger.exception('event_filter 执行异常，默认丢弃事件 %s', event.type)
            return False

    async def _is_duplicate(self, event: QQBotEvent) -> bool:
        """按事件 ID 查重（未配置记录器或事件无 ID 时不去重）。"""
        if self._dedup is None or not event.event_id:
            return False
        duplicate = await self._dedup.is_processed(self._dedup_consumer, event.event_id)
        if duplicate:
            logger.debug('跳过重复推送的事件 %s（id=%s）', event.type, event.event_id)
        return duplicate

    async def _mark_processed(self, event: QQBotEvent) -> None:
        """发布成功后记录事件 ID（失败不记录，重投可重试）。"""
        if self._dedup is not None and event.event_id:
            await self._dedup.mark_processed(self._dedup_consumer, event.event_id)


async def register_handlers(
    handler_registry: EventHandlerRegistry,
    api: QQBotAPI,
    *,
    intents: Intents | int = Intents.DEFAULT,
    shard: tuple[int, int] = (0, 1),
    properties: dict[str, str] | None = None,
    engine: QQBot | None = None,
    event_filter: Callable[[QQBotEvent], bool] | None = None,
    publish_unknown: bool = True,
    dedup_recorder: IdempotencyRecorder | None = None,
) -> None:
    """把 :class:`QQBotEventHandler` 与 :class:`QQBotAPIHandler` 批量注册到处理器注册表。

    基于 ``infinity_bus.templates.ModuleHandlerRegister`` 模板实现（**异步**：自
    infinity_bus 6.0.0 起 ``register_all_handlers`` 为协程），参数与
    :class:`QQBotEventHandler` 一致。

    Args:
        handler_registry: 目标处理器注册表（可先注册业务处理器，再加本函数）。
        api: OpenAPI 客户端。
        intents: 订阅的 Intents 位标记。
        shard: 分片 ``(id, num)``。
        properties: Identify 设备信息。
        engine: 自定义引擎（测试 / 自定义连接时可注入）。
        event_filter: 事件过滤器。
        publish_unknown: 未建模事件是否发布到 ``qqbot.event.unknown``。
        dedup_recorder: 幂等记录器（按事件 ID 去重，防止 QQ 重复推送）。
    """
    module_handlers = ModuleHandlerRegister('infinity_qqbot')
    module_handlers.add_handler(
        QQBotEventHandler,
        lambda: {
            'api': api,
            'intents': intents,
            'shard': shard,
            'properties': properties,
            'engine': engine,
            'event_filter': event_filter,
            'publish_unknown': publish_unknown,
            'dedup_recorder': dedup_recorder,
        },
    )
    module_handlers.add_handler(QQBotAPIHandler, lambda: {'api': api})
    await module_handlers.register_all_handlers(handler_registry)


async def wait_for_event(
    bus_proxy: EventBus.Proxy,
    event_pattern: Regex | str | list[Regex | str],
    *,
    timeout: float | None = 60.0,
    filter_func: Callable[[Event], bool | Awaitable[bool]] | None = None,
) -> Event:
    """等待首个匹配的事件（基于 ``expect`` 模板的一次性监听）。

    Args:
        bus_proxy: 事件总线代理（如 ``bus.proxy('app')``）。
        event_pattern: 事件名 / ``Regex`` / 列表。
        timeout: 等待超时（秒），``None`` 表示无限等待。
        filter_func: 可选过滤器，返回 ``True`` 才视为匹配。

    Returns:
        匹配到的原始 :class:`~infinity_bus.Event`。

    示例（等待网关就绪）::

        await wait_for_event(bus.proxy('app'), ReadyEvent.name, timeout=30)
    """
    async with expect(bus_proxy, event_pattern, filter_func=filter_func) as future:
        if timeout is None:
            return await future
        return await asyncio.wait_for(future, timeout=timeout)

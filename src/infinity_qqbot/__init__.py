"""infinity_qqbot —— 基于 ``infinity_bus`` 的强类型 QQ 机器人引擎。

模块结构：

- :mod:`infinity_qqbot.models`：按域拆分的 Pydantic 数据模型
  （基础对象 / 消息 / 互动 / 群聊 / 菜单 / 响应 / 事件负载）；
- :mod:`infinity_qqbot.api`：``QQBotAPI`` —— aiohttp + certifi 的 OpenAPI 封装；
- :mod:`infinity_qqbot.gateway`：``QQBotGateway`` —— WebSocket 网关客户端；
- :mod:`infinity_qqbot.engine`：``QQBot`` —— API + 网关组成的引擎；
- :mod:`infinity_qqbot.events`：QQ 网关事件声明（嵌套 ``Payload`` 风格，定义即自动收集）；
- :mod:`infinity_qqbot.rpc`：强类型 RPC —— 每方法请求 / 响应模型、事件声明、客户端
  与 ``QQBotAPIHandler``（由 ``tools/gen_rpc.py`` 生成）；
- :mod:`infinity_qqbot.handlers`：``QQBotEventHandler`` 入站发布、``register_handlers`` 批量接线与工具。

快速开始::

    import asyncio

    from infinity_bus import EventBus, EventHandlerRegistry, EventRegistry

    from infinity_qqbot import (
        QQBotAPI,
        qqbot_events,
        register_handlers,
        send_c2c_message,
    )

    async def main():
        api = QQBotAPI('你的AppID', '你的AppSecret')

        registry = EventRegistry()
        qqbot_events.register_all_events(registry)   # 注册全部事件声明（网关事件 + RPC 事件）

        handlers = EventHandlerRegistry()
        register_handlers(handlers, api)              # 入站发布 + 强类型 RPC 处理器

        async with EventBus(registry, handlers) as bus:
            message = await send_c2c_message(
                bus.proxy('app'),
                user_openid='用户 openid',
                content='hello',
            )
            print(message.id)

    asyncio.run(main())
"""

from . import api as api
from . import engine as engine
from . import events as events
from . import gateway as gateway
from . import handlers as handlers
from . import models as models
from . import rpc as rpc
from .api import QQBOT_API_BASE as QQBOT_API_BASE
from .api import QQBotAPI as QQBotAPI
from .api import QQBotAPIError as QQBotAPIError
from .engine import QQBot as QQBot
from .events import *
from .events import ALL_EVENTS as ALL_EVENTS
from .events import EVENT_BY_TYPE as EVENT_BY_TYPE
from .events import qqbot_events as qqbot_events
from .events import resolve_event as resolve_event
from .gateway import QQBotEvent as QQBotEvent
from .gateway import QQBotGateway as QQBotGateway
from .gateway import QQBotGatewayClosed as QQBotGatewayClosed
from .gateway import QQBotGatewayError as QQBotGatewayError
from .handlers import QQBotEventHandler as QQBotEventHandler
from .handlers import register_handlers as register_handlers
from .handlers import wait_for_event as wait_for_event
from .models import *
from .rpc import *
from .rpc import QQBotAPIHandler as QQBotAPIHandler

# rpc 的星导出会带入其子模块名（channels / groups / handlers / ...），
# 这里恢复本包 ``handlers`` 子模块别名，避免被 ``rpc.handlers`` 覆盖

__version__ = '0.1.1'

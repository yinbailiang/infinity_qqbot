"""QQBot 引擎：把 OpenAPI 客户端与 WebSocket 网关组合为统一入口。

``QQBot`` 自身不依赖事件总线，可独立使用::

    async with QQBot(api, intents=Intents.DEFAULT) as bot:
        async for event in bot.stream():
            ...

``QQBotEventHandler`` 会以此引擎为事件源，把事件自动发布到总线。
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import Any

from .api import QQBotAPI
from .gateway import QQBotEvent, QQBotGateway
from .models import Intents, User

logger = logging.getLogger(__name__)

__all__ = ['QQBot']


class QQBot:
    """QQ 机器人引擎（API + 网关）。"""

    def __init__(
        self,
        api: QQBotAPI,
        *,
        intents: Intents | int = Intents.DEFAULT,
        shard: tuple[int, int] = (0, 1),
        properties: dict[str, str] | None = None,
        gateway: QQBotGateway | None = None,
    ) -> None:
        """初始化引擎。

        Args:
            api: OpenAPI 客户端。
            intents: 订阅的 Intents 位标记。
            shard: 分片 ``(id, num)``。
            properties: Identify 设备信息。
            gateway: 自定义网关实现（默认按参数创建 :class:`QQBotGateway`）。
        """
        self.api = api
        self.gateway = gateway or QQBotGateway(
            api,
            intents=intents,
            shard=shard,
            properties=properties,
        )
        self._closed = False

    # ------------------------------------------------------------------
    # 状态
    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str | None:
        """当前网关会话 ID（resume 用）。"""
        return self.gateway.session_id

    @property
    def sequence(self) -> int | None:
        """已收到的最新事件序列号。"""
        return self.gateway.sequence

    @property
    def bot(self) -> User | None:
        """READY 事件中的机器人用户信息。"""
        return self.gateway.bot

    @property
    def ready(self) -> bool:
        """是否已成功建立网关会话。"""
        return self.gateway.session_id is not None

    # ------------------------------------------------------------------
    # 事件流与生命周期
    # ------------------------------------------------------------------

    def stream(self) -> AsyncIterator[QQBotEvent]:
        """返回网关事件流（自动重连，直到 :meth:`close`）。"""
        return self.gateway.stream()

    async def close(self) -> None:
        """关闭引擎（断开网关连接）。"""
        self._closed = True
        await self.gateway.close()

    async def __aenter__(self) -> QQBot:
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.close()

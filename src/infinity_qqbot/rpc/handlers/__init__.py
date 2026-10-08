"""强类型 RPC 处理器（按类别 mixin 组装）。"""

from __future__ import annotations

from event_bus.templates import ServiceHandler

from ...api import QQBotAPI
from .channels import ChannelHandlersMixin
from .groups import GroupHandlersMixin
from .interactions import InteractionHandlersMixin
from .messages import MessageHandlersMixin

__all__ = ['QQBotAPIHandler']


class QQBotAPIHandler(
    MessageHandlersMixin,
    GroupHandlersMixin,
    ChannelHandlersMixin,
    InteractionHandlersMixin,
    ServiceHandler,
):
    """把 ``QQBotAPI`` 暴露为强类型总线 RPC。

    每个处理器方法由 ``@process(请求事件, 响应事件)`` 登记（事件与模型由
    ``tools/gen_rpc.py`` 生成，事件名形如 ``qqbot.api.<method>.request`` /
    ``qqbot.api.<method>.response``），内部以显式关键字调用 :class:`QQBotAPI`
    （Pyright 静态校验字段与签名），平台异常由 ``ServiceHandler`` 自动转为
    ``success=False`` 响应。
    """

    def __init__(self, api: QQBotAPI) -> None:
        """包装一个 OpenAPI 客户端。"""
        self._api = api
        super().__init__()

    @property
    def api(self) -> QQBotAPI:
        """被包装的 OpenAPI 客户端。"""
        return self._api

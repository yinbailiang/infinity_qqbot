"""自动生成：interactions RPC 处理器（显式关键字调用 ``QQBotAPI``）。

请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

from typing import Any

from infinity_bus import Event, EventBus
from infinity_bus.templates import ServiceHandler, process

from ...api import QQBotAPI
from ..interactions import (
    CreatePanelRequest,
    CreatePanelRequestEvent,
    CreatePanelResponseEvent,
    DeletePanelRequest,
    DeletePanelRequestEvent,
    DeletePanelResponseEvent,
    GenerateUrlLinkRequest,
    GenerateUrlLinkRequestEvent,
    GenerateUrlLinkResponseEvent,
    GetMenuRequest,
    GetMenuRequestEvent,
    GetMenuResponseEvent,
    GetMeRequest,
    GetMeRequestEvent,
    GetMeResponseEvent,
    GetMyGuildsRequest,
    GetMyGuildsRequestEvent,
    GetMyGuildsResponseEvent,
    GetPanelRequest,
    GetPanelRequestEvent,
    GetPanelResponseEvent,
    ListPanelsRequest,
    ListPanelsRequestEvent,
    ListPanelsResponseEvent,
    PutMenuRequest,
    PutMenuRequestEvent,
    PutMenuResponseEvent,
    RespondInteractionRequest,
    RespondInteractionRequestEvent,
    RespondInteractionResponseEvent,
    UpdatePanelRequest,
    UpdatePanelRequestEvent,
    UpdatePanelResponseEvent,
    UpdatePanelTargetRequest,
    UpdatePanelTargetRequestEvent,
    UpdatePanelTargetResponseEvent,
)

__all__ = ['InteractionHandlersMixin']


class InteractionHandlersMixin(ServiceHandler):
    """interactions RPC 处理器 mixin。"""

    _api: QQBotAPI

    @process(GetMeRequestEvent, GetMeResponseEvent)
    async def get_me(
        self,
        payload: GetMeRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取机器人详情。"""
        result = await self._api.get_me()
        return {'result': result}

    @process(GetMyGuildsRequestEvent, GetMyGuildsResponseEvent)
    async def get_my_guilds(
        self,
        payload: GetMyGuildsRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取机器人频道列表。"""
        result = await self._api.get_my_guilds(
            before=payload.before,
            after=payload.after,
            limit=payload.limit,
        )
        return {'result': result}

    @process(GenerateUrlLinkRequestEvent, GenerateUrlLinkResponseEvent)
    async def generate_url_link(
        self,
        payload: GenerateUrlLinkRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """生成分享链接。"""
        result = await self._api.generate_url_link(
            callback_data=payload.callback_data,
        )
        return {'result': result}

    @process(RespondInteractionRequestEvent, RespondInteractionResponseEvent)
    async def respond_interaction(
        self,
        payload: RespondInteractionRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """互动事件响应。"""
        await self._api.respond_interaction(
            interaction_id=payload.interaction_id,
            code=payload.code,
            **(payload.model_extra or {}),
        )
        return {'result': None}

    @process(GetMenuRequestEvent, GetMenuResponseEvent)
    async def get_menu(
        self,
        payload: GetMenuRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """查询全局自定义菜单。"""
        result = await self._api.get_menu()
        return {'result': result}

    @process(PutMenuRequestEvent, PutMenuResponseEvent)
    async def put_menu(
        self,
        payload: PutMenuRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改全局自定义菜单。"""
        result = await self._api.put_menu(
            menu=payload.menu,
        )
        return {'result': result}

    @process(ListPanelsRequestEvent, ListPanelsResponseEvent)
    async def list_panels(
        self,
        payload: ListPanelsRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """查询指令面板列表。"""
        result = await self._api.list_panels(
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(CreatePanelRequestEvent, CreatePanelResponseEvent)
    async def create_panel(
        self,
        payload: CreatePanelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建指令面板。"""
        result = await self._api.create_panel(
            scope=payload.scope,
            panel=payload.panel,
            target_type=payload.target_type,
            user_openids=payload.user_openids,
            group_openids=payload.group_openids,
        )
        return {'result': result}

    @process(GetPanelRequestEvent, GetPanelResponseEvent)
    async def get_panel(
        self,
        payload: GetPanelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """查询指令面板详情。"""
        result = await self._api.get_panel(
            panel_id=payload.panel_id,
        )
        return {'result': result}

    @process(UpdatePanelRequestEvent, UpdatePanelResponseEvent)
    async def update_panel(
        self,
        payload: UpdatePanelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改指令面板。"""
        await self._api.update_panel(
            panel_id=payload.panel_id,
            **(payload.model_extra or {}),
        )
        return {'result': None}

    @process(DeletePanelRequestEvent, DeletePanelResponseEvent)
    async def delete_panel(
        self,
        payload: DeletePanelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除指令面板。"""
        await self._api.delete_panel(
            panel_id=payload.panel_id,
        )
        return {'result': None}

    @process(UpdatePanelTargetRequestEvent, UpdatePanelTargetResponseEvent)
    async def update_panel_target(
        self,
        payload: UpdatePanelTargetRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改指令面板关联对象。"""
        await self._api.update_panel_target(
            panel_id=payload.panel_id,
            **(payload.model_extra or {}),
        )
        return {'result': None}

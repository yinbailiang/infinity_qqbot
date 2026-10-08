"""自动生成：interactions RPC —— 请求 / 响应模型、事件声明与强类型客户端。

请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

from typing import Any

from event_bus import EventBus, EventDeclaration
from event_bus.templates import request
from event_bus.templates.request import RequestProtocol, ResponseProtocol
from pydantic import ConfigDict

from ..api import QQBotAPIError
from ..events import qqbot_events
from ..models import (
    BotInfo,
    Guild,
    Menu,
    MenuResponse,
    MenuVersion,
    Panel,
    PanelCreated,
    PanelInfo,
    PanelList,
)

__all__ = [
    'CreatePanelRequest',
    'CreatePanelRequestEvent',
    'CreatePanelResponse',
    'CreatePanelResponseEvent',
    'DeletePanelRequest',
    'DeletePanelRequestEvent',
    'DeletePanelResponse',
    'DeletePanelResponseEvent',
    'GenerateUrlLinkRequest',
    'GenerateUrlLinkRequestEvent',
    'GenerateUrlLinkResponse',
    'GenerateUrlLinkResponseEvent',
    'GetMeRequest',
    'GetMeRequestEvent',
    'GetMeResponse',
    'GetMeResponseEvent',
    'GetMenuRequest',
    'GetMenuRequestEvent',
    'GetMenuResponse',
    'GetMenuResponseEvent',
    'GetMyGuildsRequest',
    'GetMyGuildsRequestEvent',
    'GetMyGuildsResponse',
    'GetMyGuildsResponseEvent',
    'GetPanelRequest',
    'GetPanelRequestEvent',
    'GetPanelResponse',
    'GetPanelResponseEvent',
    'ListPanelsRequest',
    'ListPanelsRequestEvent',
    'ListPanelsResponse',
    'ListPanelsResponseEvent',
    'PutMenuRequest',
    'PutMenuRequestEvent',
    'PutMenuResponse',
    'PutMenuResponseEvent',
    'RespondInteractionRequest',
    'RespondInteractionRequestEvent',
    'RespondInteractionResponse',
    'RespondInteractionResponseEvent',
    'UpdatePanelRequest',
    'UpdatePanelRequestEvent',
    'UpdatePanelResponse',
    'UpdatePanelResponseEvent',
    'UpdatePanelTargetRequest',
    'UpdatePanelTargetRequestEvent',
    'UpdatePanelTargetResponse',
    'UpdatePanelTargetResponseEvent',
    'create_panel',
    'delete_panel',
    'generate_url_link',
    'get_me',
    'get_menu',
    'get_my_guilds',
    'get_panel',
    'list_panels',
    'put_menu',
    'respond_interaction',
    'update_panel',
    'update_panel_target',
]


# ======================================================================
# get_me —— 获取机器人详情
# ======================================================================


class GetMeRequest(RequestProtocol):
    """获取机器人详情（``QQBotAPI.get_me`` 请求参数）。"""


class GetMeResponse(ResponseProtocol):
    """获取机器人详情响应。"""

    result: BotInfo | None = None


@qqbot_events.event
class GetMeRequestEvent(EventDeclaration):
    """获取机器人详情（请求事件 ``qqbot.api.get_me.request``）。"""

    name = 'qqbot.api.get_me.request'
    payload_type = GetMeRequest


@qqbot_events.event
class GetMeResponseEvent(EventDeclaration):
    """获取机器人详情（响应事件 ``qqbot.api.get_me.response``）。"""

    name = 'qqbot.api.get_me.response'
    payload_type = GetMeResponse


async def get_me(
    bus_proxy: EventBus.Proxy,
    *,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> BotInfo:
    """获取机器人详情（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {}
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetMeRequestEvent.name,
        req_data=req_data,
        resp_event=GetMeResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetMeResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_my_guilds —— 获取机器人频道列表
# ======================================================================


class GetMyGuildsRequest(RequestProtocol):
    """获取机器人频道列表（``QQBotAPI.get_my_guilds`` 请求参数）。"""

    before: str | None = None
    after: str | None = None
    limit: int | None = None


class GetMyGuildsResponse(ResponseProtocol):
    """获取机器人频道列表响应。"""

    result: list[Guild] | None = None


@qqbot_events.event
class GetMyGuildsRequestEvent(EventDeclaration):
    """获取机器人频道列表（请求事件 ``qqbot.api.get_my_guilds.request``）。"""

    name = 'qqbot.api.get_my_guilds.request'
    payload_type = GetMyGuildsRequest


@qqbot_events.event
class GetMyGuildsResponseEvent(EventDeclaration):
    """获取机器人频道列表（响应事件 ``qqbot.api.get_my_guilds.response``）。"""

    name = 'qqbot.api.get_my_guilds.response'
    payload_type = GetMyGuildsResponse


async def get_my_guilds(
    bus_proxy: EventBus.Proxy,
    *,
    before: str | None = None,
    after: str | None = None,
    limit: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> list[Guild]:
    """获取机器人频道列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'before': before,
        'after': after,
        'limit': limit,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetMyGuildsRequestEvent.name,
        req_data=req_data,
        resp_event=GetMyGuildsResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetMyGuildsResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# generate_url_link —— 生成分享链接
# ======================================================================


class GenerateUrlLinkRequest(RequestProtocol):
    """生成分享链接（``QQBotAPI.generate_url_link`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')


class GenerateUrlLinkResponse(ResponseProtocol):
    """生成分享链接响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class GenerateUrlLinkRequestEvent(EventDeclaration):
    """生成分享链接（请求事件 ``qqbot.api.generate_url_link.request``）。"""

    name = 'qqbot.api.generate_url_link.request'
    payload_type = GenerateUrlLinkRequest


@qqbot_events.event
class GenerateUrlLinkResponseEvent(EventDeclaration):
    """生成分享链接（响应事件 ``qqbot.api.generate_url_link.response``）。"""

    name = 'qqbot.api.generate_url_link.response'
    payload_type = GenerateUrlLinkResponse


async def generate_url_link(
    bus_proxy: EventBus.Proxy,
    *,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """生成分享链接（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {}
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GenerateUrlLinkRequestEvent.name,
        req_data=req_data,
        resp_event=GenerateUrlLinkResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GenerateUrlLinkResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# respond_interaction —— 互动事件响应
# ======================================================================


class RespondInteractionRequest(RequestProtocol):
    """互动事件响应（``QQBotAPI.respond_interaction`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    interaction_id: str
    code: int = 0


class RespondInteractionResponse(ResponseProtocol):
    """互动事件响应响应。"""

    result: None = None


@qqbot_events.event
class RespondInteractionRequestEvent(EventDeclaration):
    """互动事件响应（请求事件 ``qqbot.api.respond_interaction.request``）。"""

    name = 'qqbot.api.respond_interaction.request'
    payload_type = RespondInteractionRequest


@qqbot_events.event
class RespondInteractionResponseEvent(EventDeclaration):
    """互动事件响应（响应事件 ``qqbot.api.respond_interaction.response``）。"""

    name = 'qqbot.api.respond_interaction.response'
    payload_type = RespondInteractionResponse


async def respond_interaction(
    bus_proxy: EventBus.Proxy,
    *,
    interaction_id: str,
    code: int = 0,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> None:
    """互动事件响应（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'interaction_id': interaction_id,
        'code': code,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RespondInteractionRequestEvent.name,
        req_data=req_data,
        resp_event=RespondInteractionResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RespondInteractionResponse)
    return response.result


# ======================================================================
# get_menu —— 查询全局自定义菜单
# ======================================================================


class GetMenuRequest(RequestProtocol):
    """查询全局自定义菜单（``QQBotAPI.get_menu`` 请求参数）。"""


class GetMenuResponse(ResponseProtocol):
    """查询全局自定义菜单响应。"""

    result: MenuResponse | None = None


@qqbot_events.event
class GetMenuRequestEvent(EventDeclaration):
    """查询全局自定义菜单（请求事件 ``qqbot.api.get_menu.request``）。"""

    name = 'qqbot.api.get_menu.request'
    payload_type = GetMenuRequest


@qqbot_events.event
class GetMenuResponseEvent(EventDeclaration):
    """查询全局自定义菜单（响应事件 ``qqbot.api.get_menu.response``）。"""

    name = 'qqbot.api.get_menu.response'
    payload_type = GetMenuResponse


async def get_menu(
    bus_proxy: EventBus.Proxy,
    *,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> MenuResponse:
    """查询全局自定义菜单（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {}
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetMenuRequestEvent.name,
        req_data=req_data,
        resp_event=GetMenuResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetMenuResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# put_menu —— 修改全局自定义菜单
# ======================================================================


class PutMenuRequest(RequestProtocol):
    """修改全局自定义菜单（``QQBotAPI.put_menu`` 请求参数）。"""

    menu: Menu


class PutMenuResponse(ResponseProtocol):
    """修改全局自定义菜单响应。"""

    result: MenuVersion | None = None


@qqbot_events.event
class PutMenuRequestEvent(EventDeclaration):
    """修改全局自定义菜单（请求事件 ``qqbot.api.put_menu.request``）。"""

    name = 'qqbot.api.put_menu.request'
    payload_type = PutMenuRequest


@qqbot_events.event
class PutMenuResponseEvent(EventDeclaration):
    """修改全局自定义菜单（响应事件 ``qqbot.api.put_menu.response``）。"""

    name = 'qqbot.api.put_menu.response'
    payload_type = PutMenuResponse


async def put_menu(
    bus_proxy: EventBus.Proxy,
    *,
    menu: Menu,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> MenuVersion:
    """修改全局自定义菜单（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'menu': menu,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=PutMenuRequestEvent.name,
        req_data=req_data,
        resp_event=PutMenuResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, PutMenuResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# list_panels —— 查询指令面板列表
# ======================================================================


class ListPanelsRequest(RequestProtocol):
    """查询指令面板列表（``QQBotAPI.list_panels`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')


class ListPanelsResponse(ResponseProtocol):
    """查询指令面板列表响应。"""

    result: PanelList | None = None


@qqbot_events.event
class ListPanelsRequestEvent(EventDeclaration):
    """查询指令面板列表（请求事件 ``qqbot.api.list_panels.request``）。"""

    name = 'qqbot.api.list_panels.request'
    payload_type = ListPanelsRequest


@qqbot_events.event
class ListPanelsResponseEvent(EventDeclaration):
    """查询指令面板列表（响应事件 ``qqbot.api.list_panels.response``）。"""

    name = 'qqbot.api.list_panels.response'
    payload_type = ListPanelsResponse


async def list_panels(
    bus_proxy: EventBus.Proxy,
    *,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> PanelList:
    """查询指令面板列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {}
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=ListPanelsRequestEvent.name,
        req_data=req_data,
        resp_event=ListPanelsResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, ListPanelsResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# create_panel —— 创建指令面板
# ======================================================================


class CreatePanelRequest(RequestProtocol):
    """创建指令面板（``QQBotAPI.create_panel`` 请求参数）。"""

    scope: str
    panel: Panel
    target_type: str | None = None
    user_openids: list[str] | None = None
    group_openids: list[str] | None = None


class CreatePanelResponse(ResponseProtocol):
    """创建指令面板响应。"""

    result: PanelCreated | None = None


@qqbot_events.event
class CreatePanelRequestEvent(EventDeclaration):
    """创建指令面板（请求事件 ``qqbot.api.create_panel.request``）。"""

    name = 'qqbot.api.create_panel.request'
    payload_type = CreatePanelRequest


@qqbot_events.event
class CreatePanelResponseEvent(EventDeclaration):
    """创建指令面板（响应事件 ``qqbot.api.create_panel.response``）。"""

    name = 'qqbot.api.create_panel.response'
    payload_type = CreatePanelResponse


async def create_panel(
    bus_proxy: EventBus.Proxy,
    *,
    scope: str,
    panel: Panel,
    target_type: str | None = None,
    user_openids: list[str] | None = None,
    group_openids: list[str] | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> PanelCreated:
    """创建指令面板（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'scope': scope,
        'panel': panel,
        'target_type': target_type,
        'user_openids': user_openids,
        'group_openids': group_openids,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreatePanelRequestEvent.name,
        req_data=req_data,
        resp_event=CreatePanelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreatePanelResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_panel —— 查询指令面板详情
# ======================================================================


class GetPanelRequest(RequestProtocol):
    """查询指令面板详情（``QQBotAPI.get_panel`` 请求参数）。"""

    panel_id: str


class GetPanelResponse(ResponseProtocol):
    """查询指令面板详情响应。"""

    result: PanelInfo | None = None


@qqbot_events.event
class GetPanelRequestEvent(EventDeclaration):
    """查询指令面板详情（请求事件 ``qqbot.api.get_panel.request``）。"""

    name = 'qqbot.api.get_panel.request'
    payload_type = GetPanelRequest


@qqbot_events.event
class GetPanelResponseEvent(EventDeclaration):
    """查询指令面板详情（响应事件 ``qqbot.api.get_panel.response``）。"""

    name = 'qqbot.api.get_panel.response'
    payload_type = GetPanelResponse


async def get_panel(
    bus_proxy: EventBus.Proxy,
    *,
    panel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> PanelInfo:
    """查询指令面板详情（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'panel_id': panel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetPanelRequestEvent.name,
        req_data=req_data,
        resp_event=GetPanelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetPanelResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# update_panel —— 修改指令面板
# ======================================================================


class UpdatePanelRequest(RequestProtocol):
    """修改指令面板（``QQBotAPI.update_panel`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    panel_id: str


class UpdatePanelResponse(ResponseProtocol):
    """修改指令面板响应。"""

    result: None = None


@qqbot_events.event
class UpdatePanelRequestEvent(EventDeclaration):
    """修改指令面板（请求事件 ``qqbot.api.update_panel.request``）。"""

    name = 'qqbot.api.update_panel.request'
    payload_type = UpdatePanelRequest


@qqbot_events.event
class UpdatePanelResponseEvent(EventDeclaration):
    """修改指令面板（响应事件 ``qqbot.api.update_panel.response``）。"""

    name = 'qqbot.api.update_panel.response'
    payload_type = UpdatePanelResponse


async def update_panel(
    bus_proxy: EventBus.Proxy,
    *,
    panel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> None:
    """修改指令面板（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'panel_id': panel_id,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdatePanelRequestEvent.name,
        req_data=req_data,
        resp_event=UpdatePanelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdatePanelResponse)
    return response.result


# ======================================================================
# delete_panel —— 删除指令面板
# ======================================================================


class DeletePanelRequest(RequestProtocol):
    """删除指令面板（``QQBotAPI.delete_panel`` 请求参数）。"""

    panel_id: str


class DeletePanelResponse(ResponseProtocol):
    """删除指令面板响应。"""

    result: None = None


@qqbot_events.event
class DeletePanelRequestEvent(EventDeclaration):
    """删除指令面板（请求事件 ``qqbot.api.delete_panel.request``）。"""

    name = 'qqbot.api.delete_panel.request'
    payload_type = DeletePanelRequest


@qqbot_events.event
class DeletePanelResponseEvent(EventDeclaration):
    """删除指令面板（响应事件 ``qqbot.api.delete_panel.response``）。"""

    name = 'qqbot.api.delete_panel.response'
    payload_type = DeletePanelResponse


async def delete_panel(
    bus_proxy: EventBus.Proxy,
    *,
    panel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除指令面板（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'panel_id': panel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeletePanelRequestEvent.name,
        req_data=req_data,
        resp_event=DeletePanelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeletePanelResponse)
    return response.result


# ======================================================================
# update_panel_target —— 修改指令面板关联对象
# ======================================================================


class UpdatePanelTargetRequest(RequestProtocol):
    """修改指令面板关联对象（``QQBotAPI.update_panel_target`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    panel_id: str


class UpdatePanelTargetResponse(ResponseProtocol):
    """修改指令面板关联对象响应。"""

    result: None = None


@qqbot_events.event
class UpdatePanelTargetRequestEvent(EventDeclaration):
    """修改指令面板关联对象（请求事件 ``qqbot.api.update_panel_target.request``）。"""

    name = 'qqbot.api.update_panel_target.request'
    payload_type = UpdatePanelTargetRequest


@qqbot_events.event
class UpdatePanelTargetResponseEvent(EventDeclaration):
    """修改指令面板关联对象（响应事件 ``qqbot.api.update_panel_target.response``）。"""

    name = 'qqbot.api.update_panel_target.response'
    payload_type = UpdatePanelTargetResponse


async def update_panel_target(
    bus_proxy: EventBus.Proxy,
    *,
    panel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> None:
    """修改指令面板关联对象（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'panel_id': panel_id,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdatePanelTargetRequestEvent.name,
        req_data=req_data,
        resp_event=UpdatePanelTargetResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdatePanelTargetResponse)
    return response.result

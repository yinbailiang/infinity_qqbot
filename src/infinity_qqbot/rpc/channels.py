"""自动生成：channels RPC —— 请求 / 响应模型、事件声明与强类型客户端。

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
    DMS,
    Announce,
    ApiPermissionDemand,
    ApiPermissionList,
    Channel,
    Guild,
    GuildMember,
    Message,
    MessageMarkdown,
    MessageReference,
    ReactionUsers,
    RecommendChannel,
    Role,
    Schedule,
)

__all__ = [
    'AddPinRequest',
    'AddPinRequestEvent',
    'AddPinResponse',
    'AddPinResponseEvent',
    'AddReactionRequest',
    'AddReactionRequestEvent',
    'AddReactionResponse',
    'AddReactionResponseEvent',
    'AddRoleMemberRequest',
    'AddRoleMemberRequestEvent',
    'AddRoleMemberResponse',
    'AddRoleMemberResponseEvent',
    'CreateApiPermissionDemandRequest',
    'CreateApiPermissionDemandRequestEvent',
    'CreateApiPermissionDemandResponse',
    'CreateApiPermissionDemandResponseEvent',
    'CreateChannelAnnounceRequest',
    'CreateChannelAnnounceRequestEvent',
    'CreateChannelAnnounceResponse',
    'CreateChannelAnnounceResponseEvent',
    'CreateDmSessionRequest',
    'CreateDmSessionRequestEvent',
    'CreateDmSessionResponse',
    'CreateDmSessionResponseEvent',
    'CreateGuildAnnounceRequest',
    'CreateGuildAnnounceRequestEvent',
    'CreateGuildAnnounceResponse',
    'CreateGuildAnnounceResponseEvent',
    'CreateGuildChannelRequest',
    'CreateGuildChannelRequestEvent',
    'CreateGuildChannelResponse',
    'CreateGuildChannelResponseEvent',
    'CreateGuildRoleRequest',
    'CreateGuildRoleRequestEvent',
    'CreateGuildRoleResponse',
    'CreateGuildRoleResponseEvent',
    'CreateScheduleRequest',
    'CreateScheduleRequestEvent',
    'CreateScheduleResponse',
    'CreateScheduleResponseEvent',
    'DeleteChannelAnnounceRequest',
    'DeleteChannelAnnounceRequestEvent',
    'DeleteChannelAnnounceResponse',
    'DeleteChannelAnnounceResponseEvent',
    'DeleteChannelRequest',
    'DeleteChannelRequestEvent',
    'DeleteChannelResponse',
    'DeleteChannelResponseEvent',
    'DeleteGuildAnnounceRequest',
    'DeleteGuildAnnounceRequestEvent',
    'DeleteGuildAnnounceResponse',
    'DeleteGuildAnnounceResponseEvent',
    'DeleteGuildRoleRequest',
    'DeleteGuildRoleRequestEvent',
    'DeleteGuildRoleResponse',
    'DeleteGuildRoleResponseEvent',
    'DeletePinRequest',
    'DeletePinRequestEvent',
    'DeletePinResponse',
    'DeletePinResponseEvent',
    'DeleteReactionRequest',
    'DeleteReactionRequestEvent',
    'DeleteReactionResponse',
    'DeleteReactionResponseEvent',
    'DeleteScheduleRequest',
    'DeleteScheduleRequestEvent',
    'DeleteScheduleResponse',
    'DeleteScheduleResponseEvent',
    'GetApiPermissionRequest',
    'GetApiPermissionRequestEvent',
    'GetApiPermissionResponse',
    'GetApiPermissionResponseEvent',
    'GetChannelMessageRequest',
    'GetChannelMessageRequestEvent',
    'GetChannelMessageResponse',
    'GetChannelMessageResponseEvent',
    'GetChannelRequest',
    'GetChannelRequestEvent',
    'GetChannelResponse',
    'GetChannelResponseEvent',
    'GetGuildChannelsRequest',
    'GetGuildChannelsRequestEvent',
    'GetGuildChannelsResponse',
    'GetGuildChannelsResponseEvent',
    'GetGuildMemberRequest',
    'GetGuildMemberRequestEvent',
    'GetGuildMemberResponse',
    'GetGuildMemberResponseEvent',
    'GetGuildMembersRequest',
    'GetGuildMembersRequestEvent',
    'GetGuildMembersResponse',
    'GetGuildMembersResponseEvent',
    'GetGuildRequest',
    'GetGuildRequestEvent',
    'GetGuildResponse',
    'GetGuildResponseEvent',
    'GetGuildRolesRequest',
    'GetGuildRolesRequestEvent',
    'GetGuildRolesResponse',
    'GetGuildRolesResponseEvent',
    'GetPinsRequest',
    'GetPinsRequestEvent',
    'GetPinsResponse',
    'GetPinsResponseEvent',
    'GetReactionsRequest',
    'GetReactionsRequestEvent',
    'GetReactionsResponse',
    'GetReactionsResponseEvent',
    'GetScheduleRequest',
    'GetScheduleRequestEvent',
    'GetScheduleResponse',
    'GetScheduleResponseEvent',
    'GetSchedulesRequest',
    'GetSchedulesRequestEvent',
    'GetSchedulesResponse',
    'GetSchedulesResponseEvent',
    'MuteGuildMemberRequest',
    'MuteGuildMemberRequestEvent',
    'MuteGuildMemberResponse',
    'MuteGuildMemberResponseEvent',
    'MuteGuildRequest',
    'MuteGuildRequestEvent',
    'MuteGuildResponse',
    'MuteGuildResponseEvent',
    'RecallChannelMessageRequest',
    'RecallChannelMessageRequestEvent',
    'RecallChannelMessageResponse',
    'RecallChannelMessageResponseEvent',
    'RecallDmMessageRequest',
    'RecallDmMessageRequestEvent',
    'RecallDmMessageResponse',
    'RecallDmMessageResponseEvent',
    'RemoveGuildMemberRequest',
    'RemoveGuildMemberRequestEvent',
    'RemoveGuildMemberResponse',
    'RemoveGuildMemberResponseEvent',
    'RemoveRoleMemberRequest',
    'RemoveRoleMemberRequestEvent',
    'RemoveRoleMemberResponse',
    'RemoveRoleMemberResponseEvent',
    'SendChannelMessageRequest',
    'SendChannelMessageRequestEvent',
    'SendChannelMessageResponse',
    'SendChannelMessageResponseEvent',
    'SendDmMessageRequest',
    'SendDmMessageRequestEvent',
    'SendDmMessageResponse',
    'SendDmMessageResponseEvent',
    'UpdateChannelRequest',
    'UpdateChannelRequestEvent',
    'UpdateChannelResponse',
    'UpdateChannelResponseEvent',
    'UpdateGuildRoleRequest',
    'UpdateGuildRoleRequestEvent',
    'UpdateGuildRoleResponse',
    'UpdateGuildRoleResponseEvent',
    'UpdateScheduleRequest',
    'UpdateScheduleRequestEvent',
    'UpdateScheduleResponse',
    'UpdateScheduleResponseEvent',
    'add_pin',
    'add_reaction',
    'add_role_member',
    'create_api_permission_demand',
    'create_channel_announce',
    'create_dm_session',
    'create_guild_announce',
    'create_guild_channel',
    'create_guild_role',
    'create_schedule',
    'delete_channel',
    'delete_channel_announce',
    'delete_guild_announce',
    'delete_guild_role',
    'delete_pin',
    'delete_reaction',
    'delete_schedule',
    'get_api_permission',
    'get_channel',
    'get_channel_message',
    'get_guild',
    'get_guild_channels',
    'get_guild_member',
    'get_guild_members',
    'get_guild_roles',
    'get_pins',
    'get_reactions',
    'get_schedule',
    'get_schedules',
    'mute_guild',
    'mute_guild_member',
    'recall_channel_message',
    'recall_dm_message',
    'remove_guild_member',
    'remove_role_member',
    'send_channel_message',
    'send_dm_message',
    'update_channel',
    'update_guild_role',
    'update_schedule',
]


# ======================================================================
# get_guild —— 获取频道详情
# ======================================================================


class GetGuildRequest(RequestProtocol):
    """获取频道详情（``QQBotAPI.get_guild`` 请求参数）。"""

    guild_id: str


class GetGuildResponse(ResponseProtocol):
    """获取频道详情响应。"""

    result: Guild | None = None


@qqbot_events.event
class GetGuildRequestEvent(EventDeclaration):
    """获取频道详情（请求事件 ``qqbot.api.get_guild.request``）。"""

    name = 'qqbot.api.get_guild.request'
    payload_type = GetGuildRequest


@qqbot_events.event
class GetGuildResponseEvent(EventDeclaration):
    """获取频道详情（响应事件 ``qqbot.api.get_guild.response``）。"""

    name = 'qqbot.api.get_guild.response'
    payload_type = GetGuildResponse


async def get_guild(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Guild:
    """获取频道详情（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGuildRequestEvent.name,
        req_data=req_data,
        resp_event=GetGuildResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGuildResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_guild_channels —— 获取子频道列表
# ======================================================================


class GetGuildChannelsRequest(RequestProtocol):
    """获取子频道列表（``QQBotAPI.get_guild_channels`` 请求参数）。"""

    guild_id: str


class GetGuildChannelsResponse(ResponseProtocol):
    """获取子频道列表响应。"""

    result: list[Channel] | None = None


@qqbot_events.event
class GetGuildChannelsRequestEvent(EventDeclaration):
    """获取子频道列表（请求事件 ``qqbot.api.get_guild_channels.request``）。"""

    name = 'qqbot.api.get_guild_channels.request'
    payload_type = GetGuildChannelsRequest


@qqbot_events.event
class GetGuildChannelsResponseEvent(EventDeclaration):
    """获取子频道列表（响应事件 ``qqbot.api.get_guild_channels.response``）。"""

    name = 'qqbot.api.get_guild_channels.response'
    payload_type = GetGuildChannelsResponse


async def get_guild_channels(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> list[Channel]:
    """获取子频道列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGuildChannelsRequestEvent.name,
        req_data=req_data,
        resp_event=GetGuildChannelsResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGuildChannelsResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# create_guild_channel —— 创建子频道
# ======================================================================


class CreateGuildChannelRequest(RequestProtocol):
    """创建子频道（``QQBotAPI.create_guild_channel`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    guild_id: str
    name: str
    type: int
    position: int | None = None
    parent_id: str | None = None
    sub_type: int | None = None
    private_type: int | None = None
    private_user_limit: int | None = None


class CreateGuildChannelResponse(ResponseProtocol):
    """创建子频道响应。"""

    result: Channel | None = None


@qqbot_events.event
class CreateGuildChannelRequestEvent(EventDeclaration):
    """创建子频道（请求事件 ``qqbot.api.create_guild_channel.request``）。"""

    name = 'qqbot.api.create_guild_channel.request'
    payload_type = CreateGuildChannelRequest


@qqbot_events.event
class CreateGuildChannelResponseEvent(EventDeclaration):
    """创建子频道（响应事件 ``qqbot.api.create_guild_channel.response``）。"""

    name = 'qqbot.api.create_guild_channel.response'
    payload_type = CreateGuildChannelResponse


async def create_guild_channel(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    name: str,
    type: int,
    position: int | None = None,
    parent_id: str | None = None,
    sub_type: int | None = None,
    private_type: int | None = None,
    private_user_limit: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> Channel:
    """创建子频道（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'name': name,
        'type': type,
        'position': position,
        'parent_id': parent_id,
        'sub_type': sub_type,
        'private_type': private_type,
        'private_user_limit': private_user_limit,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateGuildChannelRequestEvent.name,
        req_data=req_data,
        resp_event=CreateGuildChannelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateGuildChannelResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_channel —— 获取子频道详情
# ======================================================================


class GetChannelRequest(RequestProtocol):
    """获取子频道详情（``QQBotAPI.get_channel`` 请求参数）。"""

    channel_id: str


class GetChannelResponse(ResponseProtocol):
    """获取子频道详情响应。"""

    result: Channel | None = None


@qqbot_events.event
class GetChannelRequestEvent(EventDeclaration):
    """获取子频道详情（请求事件 ``qqbot.api.get_channel.request``）。"""

    name = 'qqbot.api.get_channel.request'
    payload_type = GetChannelRequest


@qqbot_events.event
class GetChannelResponseEvent(EventDeclaration):
    """获取子频道详情（响应事件 ``qqbot.api.get_channel.response``）。"""

    name = 'qqbot.api.get_channel.response'
    payload_type = GetChannelResponse


async def get_channel(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Channel:
    """获取子频道详情（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetChannelRequestEvent.name,
        req_data=req_data,
        resp_event=GetChannelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetChannelResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# update_channel —— 修改子频道
# ======================================================================


class UpdateChannelRequest(RequestProtocol):
    """修改子频道（``QQBotAPI.update_channel`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    channel_id: str
    name: str | None = None
    position: int | None = None
    parent_id: str | None = None
    private_type: int | None = None


class UpdateChannelResponse(ResponseProtocol):
    """修改子频道响应。"""

    result: Channel | None = None


@qqbot_events.event
class UpdateChannelRequestEvent(EventDeclaration):
    """修改子频道（请求事件 ``qqbot.api.update_channel.request``）。"""

    name = 'qqbot.api.update_channel.request'
    payload_type = UpdateChannelRequest


@qqbot_events.event
class UpdateChannelResponseEvent(EventDeclaration):
    """修改子频道（响应事件 ``qqbot.api.update_channel.response``）。"""

    name = 'qqbot.api.update_channel.response'
    payload_type = UpdateChannelResponse


async def update_channel(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    name: str | None = None,
    position: int | None = None,
    parent_id: str | None = None,
    private_type: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> Channel:
    """修改子频道（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'name': name,
        'position': position,
        'parent_id': parent_id,
        'private_type': private_type,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdateChannelRequestEvent.name,
        req_data=req_data,
        resp_event=UpdateChannelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdateChannelResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# delete_channel —— 删除子频道
# ======================================================================


class DeleteChannelRequest(RequestProtocol):
    """删除子频道（``QQBotAPI.delete_channel`` 请求参数）。"""

    channel_id: str


class DeleteChannelResponse(ResponseProtocol):
    """删除子频道响应。"""

    result: None = None


@qqbot_events.event
class DeleteChannelRequestEvent(EventDeclaration):
    """删除子频道（请求事件 ``qqbot.api.delete_channel.request``）。"""

    name = 'qqbot.api.delete_channel.request'
    payload_type = DeleteChannelRequest


@qqbot_events.event
class DeleteChannelResponseEvent(EventDeclaration):
    """删除子频道（响应事件 ``qqbot.api.delete_channel.response``）。"""

    name = 'qqbot.api.delete_channel.response'
    payload_type = DeleteChannelResponse


async def delete_channel(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除子频道（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteChannelRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteChannelResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteChannelResponse)
    return response.result


# ======================================================================
# send_channel_message —— 发送子频道消息
# ======================================================================


class SendChannelMessageRequest(RequestProtocol):
    """发送子频道消息（``QQBotAPI.send_channel_message`` 请求参数）。"""

    channel_id: str
    content: str | None = None
    embed: dict[str, Any] | None = None
    ark: dict[str, Any] | None = None
    image: str | None = None
    msg_id: str | None = None
    event_id: str | None = None
    markdown: MessageMarkdown | None = None
    message_reference: MessageReference | None = None


class SendChannelMessageResponse(ResponseProtocol):
    """发送子频道消息响应。"""

    result: Message | None = None


@qqbot_events.event
class SendChannelMessageRequestEvent(EventDeclaration):
    """发送子频道消息（请求事件 ``qqbot.api.send_channel_message.request``）。"""

    name = 'qqbot.api.send_channel_message.request'
    payload_type = SendChannelMessageRequest


@qqbot_events.event
class SendChannelMessageResponseEvent(EventDeclaration):
    """发送子频道消息（响应事件 ``qqbot.api.send_channel_message.response``）。"""

    name = 'qqbot.api.send_channel_message.response'
    payload_type = SendChannelMessageResponse


async def send_channel_message(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    content: str | None = None,
    embed: dict[str, Any] | None = None,
    ark: dict[str, Any] | None = None,
    image: str | None = None,
    msg_id: str | None = None,
    event_id: str | None = None,
    markdown: MessageMarkdown | None = None,
    message_reference: MessageReference | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Message:
    """发送子频道消息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'content': content,
        'embed': embed,
        'ark': ark,
        'image': image,
        'msg_id': msg_id,
        'event_id': event_id,
        'markdown': markdown,
        'message_reference': message_reference,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=SendChannelMessageRequestEvent.name,
        req_data=req_data,
        resp_event=SendChannelMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, SendChannelMessageResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_channel_message —— 获取子频道消息
# ======================================================================


class GetChannelMessageRequest(RequestProtocol):
    """获取子频道消息（``QQBotAPI.get_channel_message`` 请求参数）。"""

    channel_id: str
    message_id: str


class GetChannelMessageResponse(ResponseProtocol):
    """获取子频道消息响应。"""

    result: Message | None = None


@qqbot_events.event
class GetChannelMessageRequestEvent(EventDeclaration):
    """获取子频道消息（请求事件 ``qqbot.api.get_channel_message.request``）。"""

    name = 'qqbot.api.get_channel_message.request'
    payload_type = GetChannelMessageRequest


@qqbot_events.event
class GetChannelMessageResponseEvent(EventDeclaration):
    """获取子频道消息（响应事件 ``qqbot.api.get_channel_message.response``）。"""

    name = 'qqbot.api.get_channel_message.response'
    payload_type = GetChannelMessageResponse


async def get_channel_message(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Message:
    """获取子频道消息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetChannelMessageRequestEvent.name,
        req_data=req_data,
        resp_event=GetChannelMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetChannelMessageResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# recall_channel_message —— 撤回子频道消息
# ======================================================================


class RecallChannelMessageRequest(RequestProtocol):
    """撤回子频道消息（``QQBotAPI.recall_channel_message`` 请求参数）。"""

    channel_id: str
    message_id: str
    hidetip: bool = False


class RecallChannelMessageResponse(ResponseProtocol):
    """撤回子频道消息响应。"""

    result: None = None


@qqbot_events.event
class RecallChannelMessageRequestEvent(EventDeclaration):
    """撤回子频道消息（请求事件 ``qqbot.api.recall_channel_message.request``）。"""

    name = 'qqbot.api.recall_channel_message.request'
    payload_type = RecallChannelMessageRequest


@qqbot_events.event
class RecallChannelMessageResponseEvent(EventDeclaration):
    """撤回子频道消息（响应事件 ``qqbot.api.recall_channel_message.response``）。"""

    name = 'qqbot.api.recall_channel_message.response'
    payload_type = RecallChannelMessageResponse


async def recall_channel_message(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    hidetip: bool = False,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """撤回子频道消息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
        'hidetip': hidetip,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RecallChannelMessageRequestEvent.name,
        req_data=req_data,
        resp_event=RecallChannelMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RecallChannelMessageResponse)
    return response.result


# ======================================================================
# create_dm_session —— 创建频道私信会话
# ======================================================================


class CreateDmSessionRequest(RequestProtocol):
    """创建频道私信会话（``QQBotAPI.create_dm_session`` 请求参数）。"""

    recipient_id: str
    source_guild_id: str


class CreateDmSessionResponse(ResponseProtocol):
    """创建频道私信会话响应。"""

    result: DMS | None = None


@qqbot_events.event
class CreateDmSessionRequestEvent(EventDeclaration):
    """创建频道私信会话（请求事件 ``qqbot.api.create_dm_session.request``）。"""

    name = 'qqbot.api.create_dm_session.request'
    payload_type = CreateDmSessionRequest


@qqbot_events.event
class CreateDmSessionResponseEvent(EventDeclaration):
    """创建频道私信会话（响应事件 ``qqbot.api.create_dm_session.response``）。"""

    name = 'qqbot.api.create_dm_session.response'
    payload_type = CreateDmSessionResponse


async def create_dm_session(
    bus_proxy: EventBus.Proxy,
    *,
    recipient_id: str,
    source_guild_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> DMS:
    """创建频道私信会话（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'recipient_id': recipient_id,
        'source_guild_id': source_guild_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateDmSessionRequestEvent.name,
        req_data=req_data,
        resp_event=CreateDmSessionResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateDmSessionResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# send_dm_message —— 发送频道私信
# ======================================================================


class SendDmMessageRequest(RequestProtocol):
    """发送频道私信（``QQBotAPI.send_dm_message`` 请求参数）。"""

    guild_id: str
    content: str | None = None
    embed: dict[str, Any] | None = None
    ark: dict[str, Any] | None = None
    image: str | None = None
    msg_id: str | None = None
    event_id: str | None = None
    markdown: MessageMarkdown | None = None
    message_reference: MessageReference | None = None


class SendDmMessageResponse(ResponseProtocol):
    """发送频道私信响应。"""

    result: Message | None = None


@qqbot_events.event
class SendDmMessageRequestEvent(EventDeclaration):
    """发送频道私信（请求事件 ``qqbot.api.send_dm_message.request``）。"""

    name = 'qqbot.api.send_dm_message.request'
    payload_type = SendDmMessageRequest


@qqbot_events.event
class SendDmMessageResponseEvent(EventDeclaration):
    """发送频道私信（响应事件 ``qqbot.api.send_dm_message.response``）。"""

    name = 'qqbot.api.send_dm_message.response'
    payload_type = SendDmMessageResponse


async def send_dm_message(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    content: str | None = None,
    embed: dict[str, Any] | None = None,
    ark: dict[str, Any] | None = None,
    image: str | None = None,
    msg_id: str | None = None,
    event_id: str | None = None,
    markdown: MessageMarkdown | None = None,
    message_reference: MessageReference | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Message:
    """发送频道私信（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'content': content,
        'embed': embed,
        'ark': ark,
        'image': image,
        'msg_id': msg_id,
        'event_id': event_id,
        'markdown': markdown,
        'message_reference': message_reference,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=SendDmMessageRequestEvent.name,
        req_data=req_data,
        resp_event=SendDmMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, SendDmMessageResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# recall_dm_message —— 撤回频道私信
# ======================================================================


class RecallDmMessageRequest(RequestProtocol):
    """撤回频道私信（``QQBotAPI.recall_dm_message`` 请求参数）。"""

    guild_id: str
    message_id: str
    hidetip: bool = False


class RecallDmMessageResponse(ResponseProtocol):
    """撤回频道私信响应。"""

    result: None = None


@qqbot_events.event
class RecallDmMessageRequestEvent(EventDeclaration):
    """撤回频道私信（请求事件 ``qqbot.api.recall_dm_message.request``）。"""

    name = 'qqbot.api.recall_dm_message.request'
    payload_type = RecallDmMessageRequest


@qqbot_events.event
class RecallDmMessageResponseEvent(EventDeclaration):
    """撤回频道私信（响应事件 ``qqbot.api.recall_dm_message.response``）。"""

    name = 'qqbot.api.recall_dm_message.response'
    payload_type = RecallDmMessageResponse


async def recall_dm_message(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    message_id: str,
    hidetip: bool = False,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """撤回频道私信（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'message_id': message_id,
        'hidetip': hidetip,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RecallDmMessageRequestEvent.name,
        req_data=req_data,
        resp_event=RecallDmMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RecallDmMessageResponse)
    return response.result


# ======================================================================
# get_guild_members —— 获取频道成员列表
# ======================================================================


class GetGuildMembersRequest(RequestProtocol):
    """获取频道成员列表（``QQBotAPI.get_guild_members`` 请求参数）。"""

    guild_id: str
    after: str | None = None
    limit: int | None = None


class GetGuildMembersResponse(ResponseProtocol):
    """获取频道成员列表响应。"""

    result: list[GuildMember] | None = None


@qqbot_events.event
class GetGuildMembersRequestEvent(EventDeclaration):
    """获取频道成员列表（请求事件 ``qqbot.api.get_guild_members.request``）。"""

    name = 'qqbot.api.get_guild_members.request'
    payload_type = GetGuildMembersRequest


@qqbot_events.event
class GetGuildMembersResponseEvent(EventDeclaration):
    """获取频道成员列表（响应事件 ``qqbot.api.get_guild_members.response``）。"""

    name = 'qqbot.api.get_guild_members.response'
    payload_type = GetGuildMembersResponse


async def get_guild_members(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    after: str | None = None,
    limit: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> list[GuildMember]:
    """获取频道成员列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'after': after,
        'limit': limit,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGuildMembersRequestEvent.name,
        req_data=req_data,
        resp_event=GetGuildMembersResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGuildMembersResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_guild_member —— 获取频道成员详情
# ======================================================================


class GetGuildMemberRequest(RequestProtocol):
    """获取频道成员详情（``QQBotAPI.get_guild_member`` 请求参数）。"""

    guild_id: str
    user_id: str


class GetGuildMemberResponse(ResponseProtocol):
    """获取频道成员详情响应。"""

    result: GuildMember | None = None


@qqbot_events.event
class GetGuildMemberRequestEvent(EventDeclaration):
    """获取频道成员详情（请求事件 ``qqbot.api.get_guild_member.request``）。"""

    name = 'qqbot.api.get_guild_member.request'
    payload_type = GetGuildMemberRequest


@qqbot_events.event
class GetGuildMemberResponseEvent(EventDeclaration):
    """获取频道成员详情（响应事件 ``qqbot.api.get_guild_member.response``）。"""

    name = 'qqbot.api.get_guild_member.response'
    payload_type = GetGuildMemberResponse


async def get_guild_member(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    user_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> GuildMember:
    """获取频道成员详情（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'user_id': user_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGuildMemberRequestEvent.name,
        req_data=req_data,
        resp_event=GetGuildMemberResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGuildMemberResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# remove_guild_member —— 移除频道成员
# ======================================================================


class RemoveGuildMemberRequest(RequestProtocol):
    """移除频道成员（``QQBotAPI.remove_guild_member`` 请求参数）。"""

    guild_id: str
    user_id: str
    add_blacklist: bool | None = None
    delete_history_msg_days: int | None = None


class RemoveGuildMemberResponse(ResponseProtocol):
    """移除频道成员响应。"""

    result: None = None


@qqbot_events.event
class RemoveGuildMemberRequestEvent(EventDeclaration):
    """移除频道成员（请求事件 ``qqbot.api.remove_guild_member.request``）。"""

    name = 'qqbot.api.remove_guild_member.request'
    payload_type = RemoveGuildMemberRequest


@qqbot_events.event
class RemoveGuildMemberResponseEvent(EventDeclaration):
    """移除频道成员（响应事件 ``qqbot.api.remove_guild_member.response``）。"""

    name = 'qqbot.api.remove_guild_member.response'
    payload_type = RemoveGuildMemberResponse


async def remove_guild_member(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    user_id: str,
    add_blacklist: bool | None = None,
    delete_history_msg_days: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """移除频道成员（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'user_id': user_id,
        'add_blacklist': add_blacklist,
        'delete_history_msg_days': delete_history_msg_days,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RemoveGuildMemberRequestEvent.name,
        req_data=req_data,
        resp_event=RemoveGuildMemberResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RemoveGuildMemberResponse)
    return response.result


# ======================================================================
# get_guild_roles —— 获取频道身份组列表
# ======================================================================


class GetGuildRolesRequest(RequestProtocol):
    """获取频道身份组列表（``QQBotAPI.get_guild_roles`` 请求参数）。"""

    guild_id: str
    limit: int | None = None


class GetGuildRolesResponse(ResponseProtocol):
    """获取频道身份组列表响应。"""

    result: list[Role] | None = None


@qqbot_events.event
class GetGuildRolesRequestEvent(EventDeclaration):
    """获取频道身份组列表（请求事件 ``qqbot.api.get_guild_roles.request``）。"""

    name = 'qqbot.api.get_guild_roles.request'
    payload_type = GetGuildRolesRequest


@qqbot_events.event
class GetGuildRolesResponseEvent(EventDeclaration):
    """获取频道身份组列表（响应事件 ``qqbot.api.get_guild_roles.response``）。"""

    name = 'qqbot.api.get_guild_roles.response'
    payload_type = GetGuildRolesResponse


async def get_guild_roles(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    limit: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> list[Role]:
    """获取频道身份组列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'limit': limit,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGuildRolesRequestEvent.name,
        req_data=req_data,
        resp_event=GetGuildRolesResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGuildRolesResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# create_guild_role —— 创建频道身份组
# ======================================================================


class CreateGuildRoleRequest(RequestProtocol):
    """创建频道身份组（``QQBotAPI.create_guild_role`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    guild_id: str
    name: str | None = None
    color: int | None = None
    hoist: int | None = None
    mentionable: int | None = None


class CreateGuildRoleResponse(ResponseProtocol):
    """创建频道身份组响应。"""

    result: Role | None = None


@qqbot_events.event
class CreateGuildRoleRequestEvent(EventDeclaration):
    """创建频道身份组（请求事件 ``qqbot.api.create_guild_role.request``）。"""

    name = 'qqbot.api.create_guild_role.request'
    payload_type = CreateGuildRoleRequest


@qqbot_events.event
class CreateGuildRoleResponseEvent(EventDeclaration):
    """创建频道身份组（响应事件 ``qqbot.api.create_guild_role.response``）。"""

    name = 'qqbot.api.create_guild_role.response'
    payload_type = CreateGuildRoleResponse


async def create_guild_role(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    name: str | None = None,
    color: int | None = None,
    hoist: int | None = None,
    mentionable: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> Role:
    """创建频道身份组（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'name': name,
        'color': color,
        'hoist': hoist,
        'mentionable': mentionable,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateGuildRoleRequestEvent.name,
        req_data=req_data,
        resp_event=CreateGuildRoleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateGuildRoleResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# update_guild_role —— 修改频道身份组
# ======================================================================


class UpdateGuildRoleRequest(RequestProtocol):
    """修改频道身份组（``QQBotAPI.update_guild_role`` 请求参数）。"""

    guild_id: str
    role_id: str
    name: str | None = None
    color: int | None = None
    hoist: int | None = None


class UpdateGuildRoleResponse(ResponseProtocol):
    """修改频道身份组响应。"""

    result: Role | None = None


@qqbot_events.event
class UpdateGuildRoleRequestEvent(EventDeclaration):
    """修改频道身份组（请求事件 ``qqbot.api.update_guild_role.request``）。"""

    name = 'qqbot.api.update_guild_role.request'
    payload_type = UpdateGuildRoleRequest


@qqbot_events.event
class UpdateGuildRoleResponseEvent(EventDeclaration):
    """修改频道身份组（响应事件 ``qqbot.api.update_guild_role.response``）。"""

    name = 'qqbot.api.update_guild_role.response'
    payload_type = UpdateGuildRoleResponse


async def update_guild_role(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    role_id: str,
    name: str | None = None,
    color: int | None = None,
    hoist: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Role:
    """修改频道身份组（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'role_id': role_id,
        'name': name,
        'color': color,
        'hoist': hoist,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdateGuildRoleRequestEvent.name,
        req_data=req_data,
        resp_event=UpdateGuildRoleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdateGuildRoleResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# delete_guild_role —— 删除频道身份组
# ======================================================================


class DeleteGuildRoleRequest(RequestProtocol):
    """删除频道身份组（``QQBotAPI.delete_guild_role`` 请求参数）。"""

    guild_id: str
    role_id: str


class DeleteGuildRoleResponse(ResponseProtocol):
    """删除频道身份组响应。"""

    result: None = None


@qqbot_events.event
class DeleteGuildRoleRequestEvent(EventDeclaration):
    """删除频道身份组（请求事件 ``qqbot.api.delete_guild_role.request``）。"""

    name = 'qqbot.api.delete_guild_role.request'
    payload_type = DeleteGuildRoleRequest


@qqbot_events.event
class DeleteGuildRoleResponseEvent(EventDeclaration):
    """删除频道身份组（响应事件 ``qqbot.api.delete_guild_role.response``）。"""

    name = 'qqbot.api.delete_guild_role.response'
    payload_type = DeleteGuildRoleResponse


async def delete_guild_role(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    role_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除频道身份组（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'role_id': role_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteGuildRoleRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteGuildRoleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteGuildRoleResponse)
    return response.result


# ======================================================================
# add_role_member —— 添加身份组成员
# ======================================================================


class AddRoleMemberRequest(RequestProtocol):
    """添加身份组成员（``QQBotAPI.add_role_member`` 请求参数）。"""

    guild_id: str
    user_id: str
    role_id: str
    channel_id: str | None = None


class AddRoleMemberResponse(ResponseProtocol):
    """添加身份组成员响应。"""

    result: None = None


@qqbot_events.event
class AddRoleMemberRequestEvent(EventDeclaration):
    """添加身份组成员（请求事件 ``qqbot.api.add_role_member.request``）。"""

    name = 'qqbot.api.add_role_member.request'
    payload_type = AddRoleMemberRequest


@qqbot_events.event
class AddRoleMemberResponseEvent(EventDeclaration):
    """添加身份组成员（响应事件 ``qqbot.api.add_role_member.response``）。"""

    name = 'qqbot.api.add_role_member.response'
    payload_type = AddRoleMemberResponse


async def add_role_member(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    user_id: str,
    role_id: str,
    channel_id: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """添加身份组成员（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'user_id': user_id,
        'role_id': role_id,
        'channel_id': channel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=AddRoleMemberRequestEvent.name,
        req_data=req_data,
        resp_event=AddRoleMemberResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, AddRoleMemberResponse)
    return response.result


# ======================================================================
# remove_role_member —— 移除身份组成员
# ======================================================================


class RemoveRoleMemberRequest(RequestProtocol):
    """移除身份组成员（``QQBotAPI.remove_role_member`` 请求参数）。"""

    guild_id: str
    user_id: str
    role_id: str
    channel_id: str | None = None


class RemoveRoleMemberResponse(ResponseProtocol):
    """移除身份组成员响应。"""

    result: None = None


@qqbot_events.event
class RemoveRoleMemberRequestEvent(EventDeclaration):
    """移除身份组成员（请求事件 ``qqbot.api.remove_role_member.request``）。"""

    name = 'qqbot.api.remove_role_member.request'
    payload_type = RemoveRoleMemberRequest


@qqbot_events.event
class RemoveRoleMemberResponseEvent(EventDeclaration):
    """移除身份组成员（响应事件 ``qqbot.api.remove_role_member.response``）。"""

    name = 'qqbot.api.remove_role_member.response'
    payload_type = RemoveRoleMemberResponse


async def remove_role_member(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    user_id: str,
    role_id: str,
    channel_id: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """移除身份组成员（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'user_id': user_id,
        'role_id': role_id,
        'channel_id': channel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RemoveRoleMemberRequestEvent.name,
        req_data=req_data,
        resp_event=RemoveRoleMemberResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RemoveRoleMemberResponse)
    return response.result


# ======================================================================
# mute_guild —— 频道全员禁言
# ======================================================================


class MuteGuildRequest(RequestProtocol):
    """频道全员禁言（``QQBotAPI.mute_guild`` 请求参数）。"""

    guild_id: str
    mute_seconds: str | None = None
    mute_end_timestamp: str | None = None


class MuteGuildResponse(ResponseProtocol):
    """频道全员禁言响应。"""

    result: None = None


@qqbot_events.event
class MuteGuildRequestEvent(EventDeclaration):
    """频道全员禁言（请求事件 ``qqbot.api.mute_guild.request``）。"""

    name = 'qqbot.api.mute_guild.request'
    payload_type = MuteGuildRequest


@qqbot_events.event
class MuteGuildResponseEvent(EventDeclaration):
    """频道全员禁言（响应事件 ``qqbot.api.mute_guild.response``）。"""

    name = 'qqbot.api.mute_guild.response'
    payload_type = MuteGuildResponse


async def mute_guild(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    mute_seconds: str | None = None,
    mute_end_timestamp: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """频道全员禁言（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'mute_seconds': mute_seconds,
        'mute_end_timestamp': mute_end_timestamp,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=MuteGuildRequestEvent.name,
        req_data=req_data,
        resp_event=MuteGuildResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, MuteGuildResponse)
    return response.result


# ======================================================================
# mute_guild_member —— 指定成员禁言
# ======================================================================


class MuteGuildMemberRequest(RequestProtocol):
    """指定成员禁言（``QQBotAPI.mute_guild_member`` 请求参数）。"""

    guild_id: str
    user_id: str
    mute_seconds: str | None = None
    mute_end_timestamp: str | None = None


class MuteGuildMemberResponse(ResponseProtocol):
    """指定成员禁言响应。"""

    result: None = None


@qqbot_events.event
class MuteGuildMemberRequestEvent(EventDeclaration):
    """指定成员禁言（请求事件 ``qqbot.api.mute_guild_member.request``）。"""

    name = 'qqbot.api.mute_guild_member.request'
    payload_type = MuteGuildMemberRequest


@qqbot_events.event
class MuteGuildMemberResponseEvent(EventDeclaration):
    """指定成员禁言（响应事件 ``qqbot.api.mute_guild_member.response``）。"""

    name = 'qqbot.api.mute_guild_member.response'
    payload_type = MuteGuildMemberResponse


async def mute_guild_member(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    user_id: str,
    mute_seconds: str | None = None,
    mute_end_timestamp: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """指定成员禁言（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'user_id': user_id,
        'mute_seconds': mute_seconds,
        'mute_end_timestamp': mute_end_timestamp,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=MuteGuildMemberRequestEvent.name,
        req_data=req_data,
        resp_event=MuteGuildMemberResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, MuteGuildMemberResponse)
    return response.result


# ======================================================================
# create_guild_announce —— 创建频道公告
# ======================================================================


class CreateGuildAnnounceRequest(RequestProtocol):
    """创建频道公告（``QQBotAPI.create_guild_announce`` 请求参数）。"""

    guild_id: str
    message_id: str | None = None
    channel_id: str | None = None
    announces_type: int | None = None
    recommend_channels: list[RecommendChannel] | None = None


class CreateGuildAnnounceResponse(ResponseProtocol):
    """创建频道公告响应。"""

    result: Announce | None = None


@qqbot_events.event
class CreateGuildAnnounceRequestEvent(EventDeclaration):
    """创建频道公告（请求事件 ``qqbot.api.create_guild_announce.request``）。"""

    name = 'qqbot.api.create_guild_announce.request'
    payload_type = CreateGuildAnnounceRequest


@qqbot_events.event
class CreateGuildAnnounceResponseEvent(EventDeclaration):
    """创建频道公告（响应事件 ``qqbot.api.create_guild_announce.response``）。"""

    name = 'qqbot.api.create_guild_announce.response'
    payload_type = CreateGuildAnnounceResponse


async def create_guild_announce(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    message_id: str | None = None,
    channel_id: str | None = None,
    announces_type: int | None = None,
    recommend_channels: list[RecommendChannel] | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Announce:
    """创建频道公告（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'message_id': message_id,
        'channel_id': channel_id,
        'announces_type': announces_type,
        'recommend_channels': recommend_channels,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateGuildAnnounceRequestEvent.name,
        req_data=req_data,
        resp_event=CreateGuildAnnounceResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateGuildAnnounceResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# delete_guild_announce —— 删除频道公告
# ======================================================================


class DeleteGuildAnnounceRequest(RequestProtocol):
    """删除频道公告（``QQBotAPI.delete_guild_announce`` 请求参数）。"""

    guild_id: str
    message_id: str


class DeleteGuildAnnounceResponse(ResponseProtocol):
    """删除频道公告响应。"""

    result: None = None


@qqbot_events.event
class DeleteGuildAnnounceRequestEvent(EventDeclaration):
    """删除频道公告（请求事件 ``qqbot.api.delete_guild_announce.request``）。"""

    name = 'qqbot.api.delete_guild_announce.request'
    payload_type = DeleteGuildAnnounceRequest


@qqbot_events.event
class DeleteGuildAnnounceResponseEvent(EventDeclaration):
    """删除频道公告（响应事件 ``qqbot.api.delete_guild_announce.response``）。"""

    name = 'qqbot.api.delete_guild_announce.response'
    payload_type = DeleteGuildAnnounceResponse


async def delete_guild_announce(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除频道公告（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteGuildAnnounceRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteGuildAnnounceResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteGuildAnnounceResponse)
    return response.result


# ======================================================================
# create_channel_announce —— 创建子频道公告
# ======================================================================


class CreateChannelAnnounceRequest(RequestProtocol):
    """创建子频道公告（``QQBotAPI.create_channel_announce`` 请求参数）。"""

    channel_id: str
    message_id: str | None = None
    announces_type: int | None = None


class CreateChannelAnnounceResponse(ResponseProtocol):
    """创建子频道公告响应。"""

    result: Announce | None = None


@qqbot_events.event
class CreateChannelAnnounceRequestEvent(EventDeclaration):
    """创建子频道公告（请求事件 ``qqbot.api.create_channel_announce.request``）。"""

    name = 'qqbot.api.create_channel_announce.request'
    payload_type = CreateChannelAnnounceRequest


@qqbot_events.event
class CreateChannelAnnounceResponseEvent(EventDeclaration):
    """创建子频道公告（响应事件 ``qqbot.api.create_channel_announce.response``）。"""

    name = 'qqbot.api.create_channel_announce.response'
    payload_type = CreateChannelAnnounceResponse


async def create_channel_announce(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str | None = None,
    announces_type: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Announce:
    """创建子频道公告（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
        'announces_type': announces_type,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateChannelAnnounceRequestEvent.name,
        req_data=req_data,
        resp_event=CreateChannelAnnounceResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateChannelAnnounceResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# delete_channel_announce —— 删除子频道公告
# ======================================================================


class DeleteChannelAnnounceRequest(RequestProtocol):
    """删除子频道公告（``QQBotAPI.delete_channel_announce`` 请求参数）。"""

    channel_id: str
    message_id: str


class DeleteChannelAnnounceResponse(ResponseProtocol):
    """删除子频道公告响应。"""

    result: None = None


@qqbot_events.event
class DeleteChannelAnnounceRequestEvent(EventDeclaration):
    """删除子频道公告（请求事件 ``qqbot.api.delete_channel_announce.request``）。"""

    name = 'qqbot.api.delete_channel_announce.request'
    payload_type = DeleteChannelAnnounceRequest


@qqbot_events.event
class DeleteChannelAnnounceResponseEvent(EventDeclaration):
    """删除子频道公告（响应事件 ``qqbot.api.delete_channel_announce.response``）。"""

    name = 'qqbot.api.delete_channel_announce.response'
    payload_type = DeleteChannelAnnounceResponse


async def delete_channel_announce(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除子频道公告（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteChannelAnnounceRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteChannelAnnounceResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteChannelAnnounceResponse)
    return response.result


# ======================================================================
# get_api_permission —— 获取频道可用权限列表
# ======================================================================


class GetApiPermissionRequest(RequestProtocol):
    """获取频道可用权限列表（``QQBotAPI.get_api_permission`` 请求参数）。"""

    guild_id: str


class GetApiPermissionResponse(ResponseProtocol):
    """获取频道可用权限列表响应。"""

    result: ApiPermissionList | None = None


@qqbot_events.event
class GetApiPermissionRequestEvent(EventDeclaration):
    """获取频道可用权限列表（请求事件 ``qqbot.api.get_api_permission.request``）。"""

    name = 'qqbot.api.get_api_permission.request'
    payload_type = GetApiPermissionRequest


@qqbot_events.event
class GetApiPermissionResponseEvent(EventDeclaration):
    """获取频道可用权限列表（响应事件 ``qqbot.api.get_api_permission.response``）。"""

    name = 'qqbot.api.get_api_permission.response'
    payload_type = GetApiPermissionResponse


async def get_api_permission(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> ApiPermissionList:
    """获取频道可用权限列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetApiPermissionRequestEvent.name,
        req_data=req_data,
        resp_event=GetApiPermissionResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetApiPermissionResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# create_api_permission_demand —— 创建频道 API 接口权限授权链接
# ======================================================================


class CreateApiPermissionDemandRequest(RequestProtocol):
    """创建频道 API 接口权限授权链接（``QQBotAPI.create_api_permission_demand`` 请求参数）。"""

    guild_id: str
    channel_id: str
    api_identify: dict[str, Any]
    desc: str | None = None


class CreateApiPermissionDemandResponse(ResponseProtocol):
    """创建频道 API 接口权限授权链接响应。"""

    result: ApiPermissionDemand | None = None


@qqbot_events.event
class CreateApiPermissionDemandRequestEvent(EventDeclaration):
    """创建频道 API 接口权限授权链接（请求事件 ``qqbot.api.create_api_permission_demand.request``）。"""

    name = 'qqbot.api.create_api_permission_demand.request'
    payload_type = CreateApiPermissionDemandRequest


@qqbot_events.event
class CreateApiPermissionDemandResponseEvent(EventDeclaration):
    """创建频道 API 接口权限授权链接（响应事件 ``qqbot.api.create_api_permission_demand.response``）。"""

    name = 'qqbot.api.create_api_permission_demand.response'
    payload_type = CreateApiPermissionDemandResponse


async def create_api_permission_demand(
    bus_proxy: EventBus.Proxy,
    *,
    guild_id: str,
    channel_id: str,
    api_identify: dict[str, Any],
    desc: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> ApiPermissionDemand:
    """创建频道 API 接口权限授权链接（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'guild_id': guild_id,
        'channel_id': channel_id,
        'api_identify': api_identify,
        'desc': desc,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateApiPermissionDemandRequestEvent.name,
        req_data=req_data,
        resp_event=CreateApiPermissionDemandResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateApiPermissionDemandResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# add_reaction —— 添加表情表态
# ======================================================================


class AddReactionRequest(RequestProtocol):
    """添加表情表态（``QQBotAPI.add_reaction`` 请求参数）。"""

    channel_id: str
    message_id: str
    emoji_type: int | str
    emoji_id: str


class AddReactionResponse(ResponseProtocol):
    """添加表情表态响应。"""

    result: None = None


@qqbot_events.event
class AddReactionRequestEvent(EventDeclaration):
    """添加表情表态（请求事件 ``qqbot.api.add_reaction.request``）。"""

    name = 'qqbot.api.add_reaction.request'
    payload_type = AddReactionRequest


@qqbot_events.event
class AddReactionResponseEvent(EventDeclaration):
    """添加表情表态（响应事件 ``qqbot.api.add_reaction.response``）。"""

    name = 'qqbot.api.add_reaction.response'
    payload_type = AddReactionResponse


async def add_reaction(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    emoji_type: int | str,
    emoji_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """添加表情表态（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
        'emoji_type': emoji_type,
        'emoji_id': emoji_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=AddReactionRequestEvent.name,
        req_data=req_data,
        resp_event=AddReactionResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, AddReactionResponse)
    return response.result


# ======================================================================
# delete_reaction —— 删除表情表态
# ======================================================================


class DeleteReactionRequest(RequestProtocol):
    """删除表情表态（``QQBotAPI.delete_reaction`` 请求参数）。"""

    channel_id: str
    message_id: str
    emoji_type: int | str
    emoji_id: str


class DeleteReactionResponse(ResponseProtocol):
    """删除表情表态响应。"""

    result: None = None


@qqbot_events.event
class DeleteReactionRequestEvent(EventDeclaration):
    """删除表情表态（请求事件 ``qqbot.api.delete_reaction.request``）。"""

    name = 'qqbot.api.delete_reaction.request'
    payload_type = DeleteReactionRequest


@qqbot_events.event
class DeleteReactionResponseEvent(EventDeclaration):
    """删除表情表态（响应事件 ``qqbot.api.delete_reaction.response``）。"""

    name = 'qqbot.api.delete_reaction.response'
    payload_type = DeleteReactionResponse


async def delete_reaction(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    emoji_type: int | str,
    emoji_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除表情表态（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
        'emoji_type': emoji_type,
        'emoji_id': emoji_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteReactionRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteReactionResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteReactionResponse)
    return response.result


# ======================================================================
# get_reactions —— 获取表情表态用户列表
# ======================================================================


class GetReactionsRequest(RequestProtocol):
    """获取表情表态用户列表（``QQBotAPI.get_reactions`` 请求参数）。"""

    channel_id: str
    message_id: str
    emoji_type: int | str
    emoji_id: str


class GetReactionsResponse(ResponseProtocol):
    """获取表情表态用户列表响应。"""

    result: ReactionUsers | None = None


@qqbot_events.event
class GetReactionsRequestEvent(EventDeclaration):
    """获取表情表态用户列表（请求事件 ``qqbot.api.get_reactions.request``）。"""

    name = 'qqbot.api.get_reactions.request'
    payload_type = GetReactionsRequest


@qqbot_events.event
class GetReactionsResponseEvent(EventDeclaration):
    """获取表情表态用户列表（响应事件 ``qqbot.api.get_reactions.response``）。"""

    name = 'qqbot.api.get_reactions.response'
    payload_type = GetReactionsResponse


async def get_reactions(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    emoji_type: int | str,
    emoji_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> ReactionUsers:
    """获取表情表态用户列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
        'emoji_type': emoji_type,
        'emoji_id': emoji_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetReactionsRequestEvent.name,
        req_data=req_data,
        resp_event=GetReactionsResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetReactionsResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# add_pin —— 添加精华消息
# ======================================================================


class AddPinRequest(RequestProtocol):
    """添加精华消息（``QQBotAPI.add_pin`` 请求参数）。"""

    channel_id: str
    message_id: str


class AddPinResponse(ResponseProtocol):
    """添加精华消息响应。"""

    result: None = None


@qqbot_events.event
class AddPinRequestEvent(EventDeclaration):
    """添加精华消息（请求事件 ``qqbot.api.add_pin.request``）。"""

    name = 'qqbot.api.add_pin.request'
    payload_type = AddPinRequest


@qqbot_events.event
class AddPinResponseEvent(EventDeclaration):
    """添加精华消息（响应事件 ``qqbot.api.add_pin.response``）。"""

    name = 'qqbot.api.add_pin.response'
    payload_type = AddPinResponse


async def add_pin(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """添加精华消息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=AddPinRequestEvent.name,
        req_data=req_data,
        resp_event=AddPinResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, AddPinResponse)
    return response.result


# ======================================================================
# delete_pin —— 删除精华消息
# ======================================================================


class DeletePinRequest(RequestProtocol):
    """删除精华消息（``QQBotAPI.delete_pin`` 请求参数）。"""

    channel_id: str
    message_id: str


class DeletePinResponse(ResponseProtocol):
    """删除精华消息响应。"""

    result: None = None


@qqbot_events.event
class DeletePinRequestEvent(EventDeclaration):
    """删除精华消息（请求事件 ``qqbot.api.delete_pin.request``）。"""

    name = 'qqbot.api.delete_pin.request'
    payload_type = DeletePinRequest


@qqbot_events.event
class DeletePinResponseEvent(EventDeclaration):
    """删除精华消息（响应事件 ``qqbot.api.delete_pin.response``）。"""

    name = 'qqbot.api.delete_pin.response'
    payload_type = DeletePinResponse


async def delete_pin(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除精华消息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeletePinRequestEvent.name,
        req_data=req_data,
        resp_event=DeletePinResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeletePinResponse)
    return response.result


# ======================================================================
# get_pins —— 获取精华消息列表
# ======================================================================


class GetPinsRequest(RequestProtocol):
    """获取精华消息列表（``QQBotAPI.get_pins`` 请求参数）。"""

    channel_id: str


class GetPinsResponse(ResponseProtocol):
    """获取精华消息列表响应。"""

    result: list[Message] | None = None


@qqbot_events.event
class GetPinsRequestEvent(EventDeclaration):
    """获取精华消息列表（请求事件 ``qqbot.api.get_pins.request``）。"""

    name = 'qqbot.api.get_pins.request'
    payload_type = GetPinsRequest


@qqbot_events.event
class GetPinsResponseEvent(EventDeclaration):
    """获取精华消息列表（响应事件 ``qqbot.api.get_pins.response``）。"""

    name = 'qqbot.api.get_pins.response'
    payload_type = GetPinsResponse


async def get_pins(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> list[Message]:
    """获取精华消息列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetPinsRequestEvent.name,
        req_data=req_data,
        resp_event=GetPinsResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetPinsResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_schedules —— 获取日程列表
# ======================================================================


class GetSchedulesRequest(RequestProtocol):
    """获取日程列表（``QQBotAPI.get_schedules`` 请求参数）。"""

    channel_id: str
    since: str | None = None


class GetSchedulesResponse(ResponseProtocol):
    """获取日程列表响应。"""

    result: list[Schedule] | None = None


@qqbot_events.event
class GetSchedulesRequestEvent(EventDeclaration):
    """获取日程列表（请求事件 ``qqbot.api.get_schedules.request``）。"""

    name = 'qqbot.api.get_schedules.request'
    payload_type = GetSchedulesRequest


@qqbot_events.event
class GetSchedulesResponseEvent(EventDeclaration):
    """获取日程列表（响应事件 ``qqbot.api.get_schedules.response``）。"""

    name = 'qqbot.api.get_schedules.response'
    payload_type = GetSchedulesResponse


async def get_schedules(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    since: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> list[Schedule]:
    """获取日程列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'since': since,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetSchedulesRequestEvent.name,
        req_data=req_data,
        resp_event=GetSchedulesResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetSchedulesResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# create_schedule —— 创建日程
# ======================================================================


class CreateScheduleRequest(RequestProtocol):
    """创建日程（``QQBotAPI.create_schedule`` 请求参数）。"""

    channel_id: str
    schedule: Schedule


class CreateScheduleResponse(ResponseProtocol):
    """创建日程响应。"""

    result: Schedule | None = None


@qqbot_events.event
class CreateScheduleRequestEvent(EventDeclaration):
    """创建日程（请求事件 ``qqbot.api.create_schedule.request``）。"""

    name = 'qqbot.api.create_schedule.request'
    payload_type = CreateScheduleRequest


@qqbot_events.event
class CreateScheduleResponseEvent(EventDeclaration):
    """创建日程（响应事件 ``qqbot.api.create_schedule.response``）。"""

    name = 'qqbot.api.create_schedule.response'
    payload_type = CreateScheduleResponse


async def create_schedule(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    schedule: Schedule,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Schedule:
    """创建日程（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'schedule': schedule,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateScheduleRequestEvent.name,
        req_data=req_data,
        resp_event=CreateScheduleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateScheduleResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_schedule —— 获取日程详情
# ======================================================================


class GetScheduleRequest(RequestProtocol):
    """获取日程详情（``QQBotAPI.get_schedule`` 请求参数）。"""

    channel_id: str
    schedule_id: str


class GetScheduleResponse(ResponseProtocol):
    """获取日程详情响应。"""

    result: Schedule | None = None


@qqbot_events.event
class GetScheduleRequestEvent(EventDeclaration):
    """获取日程详情（请求事件 ``qqbot.api.get_schedule.request``）。"""

    name = 'qqbot.api.get_schedule.request'
    payload_type = GetScheduleRequest


@qqbot_events.event
class GetScheduleResponseEvent(EventDeclaration):
    """获取日程详情（响应事件 ``qqbot.api.get_schedule.response``）。"""

    name = 'qqbot.api.get_schedule.response'
    payload_type = GetScheduleResponse


async def get_schedule(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    schedule_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Schedule:
    """获取日程详情（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'schedule_id': schedule_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetScheduleRequestEvent.name,
        req_data=req_data,
        resp_event=GetScheduleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetScheduleResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# update_schedule —— 修改日程
# ======================================================================


class UpdateScheduleRequest(RequestProtocol):
    """修改日程（``QQBotAPI.update_schedule`` 请求参数）。"""

    channel_id: str
    schedule_id: str
    schedule: Schedule


class UpdateScheduleResponse(ResponseProtocol):
    """修改日程响应。"""

    result: Schedule | None = None


@qqbot_events.event
class UpdateScheduleRequestEvent(EventDeclaration):
    """修改日程（请求事件 ``qqbot.api.update_schedule.request``）。"""

    name = 'qqbot.api.update_schedule.request'
    payload_type = UpdateScheduleRequest


@qqbot_events.event
class UpdateScheduleResponseEvent(EventDeclaration):
    """修改日程（响应事件 ``qqbot.api.update_schedule.response``）。"""

    name = 'qqbot.api.update_schedule.response'
    payload_type = UpdateScheduleResponse


async def update_schedule(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    schedule_id: str,
    schedule: Schedule,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> Schedule:
    """修改日程（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'schedule_id': schedule_id,
        'schedule': schedule,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdateScheduleRequestEvent.name,
        req_data=req_data,
        resp_event=UpdateScheduleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdateScheduleResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# delete_schedule —— 删除日程
# ======================================================================


class DeleteScheduleRequest(RequestProtocol):
    """删除日程（``QQBotAPI.delete_schedule`` 请求参数）。"""

    channel_id: str
    schedule_id: str


class DeleteScheduleResponse(ResponseProtocol):
    """删除日程响应。"""

    result: None = None


@qqbot_events.event
class DeleteScheduleRequestEvent(EventDeclaration):
    """删除日程（请求事件 ``qqbot.api.delete_schedule.request``）。"""

    name = 'qqbot.api.delete_schedule.request'
    payload_type = DeleteScheduleRequest


@qqbot_events.event
class DeleteScheduleResponseEvent(EventDeclaration):
    """删除日程（响应事件 ``qqbot.api.delete_schedule.response``）。"""

    name = 'qqbot.api.delete_schedule.response'
    payload_type = DeleteScheduleResponse


async def delete_schedule(
    bus_proxy: EventBus.Proxy,
    *,
    channel_id: str,
    schedule_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除日程（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'channel_id': channel_id,
        'schedule_id': schedule_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteScheduleRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteScheduleResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteScheduleResponse)
    return response.result

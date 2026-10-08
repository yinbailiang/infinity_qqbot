"""自动生成：groups RPC —— 请求 / 响应模型、事件声明与强类型客户端。

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
    GroupBotState,
    GroupInfo,
    GroupMember,
    GroupMemberPage,
    JoinRequestPage,
    RestrictChatSetting,
    SetMemberMuteState,
)

__all__ = [
    'ApprovalJoinRequestRequest',
    'ApprovalJoinRequestRequestEvent',
    'ApprovalJoinRequestResponse',
    'ApprovalJoinRequestResponseEvent',
    'BatchRemoveGroupMembersRequest',
    'BatchRemoveGroupMembersRequestEvent',
    'BatchRemoveGroupMembersResponse',
    'BatchRemoveGroupMembersResponseEvent',
    'CreateJoinApprovalStrategyRequest',
    'CreateJoinApprovalStrategyRequestEvent',
    'CreateJoinApprovalStrategyResponse',
    'CreateJoinApprovalStrategyResponseEvent',
    'DeleteJoinApprovalStrategyRequest',
    'DeleteJoinApprovalStrategyRequestEvent',
    'DeleteJoinApprovalStrategyResponse',
    'DeleteJoinApprovalStrategyResponseEvent',
    'ExecuteJoinApprovalStrategyRequest',
    'ExecuteJoinApprovalStrategyRequestEvent',
    'ExecuteJoinApprovalStrategyResponse',
    'ExecuteJoinApprovalStrategyResponseEvent',
    'GetGroupBlacklistRequest',
    'GetGroupBlacklistRequestEvent',
    'GetGroupBlacklistResponse',
    'GetGroupBlacklistResponseEvent',
    'GetGroupBotStateRequest',
    'GetGroupBotStateRequestEvent',
    'GetGroupBotStateResponse',
    'GetGroupBotStateResponseEvent',
    'GetGroupInfoRequest',
    'GetGroupInfoRequestEvent',
    'GetGroupInfoResponse',
    'GetGroupInfoResponseEvent',
    'GetGroupMemberRequest',
    'GetGroupMemberRequestEvent',
    'GetGroupMemberResponse',
    'GetGroupMemberResponseEvent',
    'GetGroupMembersRequest',
    'GetGroupMembersRequestEvent',
    'GetGroupMembersResponse',
    'GetGroupMembersResponseEvent',
    'GetGroupRestrictChatSettingRequest',
    'GetGroupRestrictChatSettingRequestEvent',
    'GetGroupRestrictChatSettingResponse',
    'GetGroupRestrictChatSettingResponseEvent',
    'GetJoinApprovalStrategiesRequest',
    'GetJoinApprovalStrategiesRequestEvent',
    'GetJoinApprovalStrategiesResponse',
    'GetJoinApprovalStrategiesResponseEvent',
    'GetJoinRequestListRequest',
    'GetJoinRequestListRequestEvent',
    'GetJoinRequestListResponse',
    'GetJoinRequestListResponseEvent',
    'OperateGroupBlacklistRequest',
    'OperateGroupBlacklistRequestEvent',
    'OperateGroupBlacklistResponse',
    'OperateGroupBlacklistResponseEvent',
    'SetGroupMemberMuteRequest',
    'SetGroupMemberMuteRequestEvent',
    'SetGroupMemberMuteResponse',
    'SetGroupMemberMuteResponseEvent',
    'UpdateJoinApprovalStrategyRequest',
    'UpdateJoinApprovalStrategyRequestEvent',
    'UpdateJoinApprovalStrategyResponse',
    'UpdateJoinApprovalStrategyResponseEvent',
    'UpdateJoinApprovalWhitelistRequest',
    'UpdateJoinApprovalWhitelistRequestEvent',
    'UpdateJoinApprovalWhitelistResponse',
    'UpdateJoinApprovalWhitelistResponseEvent',
    'approval_join_request',
    'batch_remove_group_members',
    'create_join_approval_strategy',
    'delete_join_approval_strategy',
    'execute_join_approval_strategy',
    'get_group_blacklist',
    'get_group_bot_state',
    'get_group_info',
    'get_group_member',
    'get_group_members',
    'get_group_restrict_chat_setting',
    'get_join_approval_strategies',
    'get_join_request_list',
    'operate_group_blacklist',
    'set_group_member_mute',
    'update_join_approval_strategy',
    'update_join_approval_whitelist',
]


# ======================================================================
# get_group_info —— 获取群基本信息
# ======================================================================


class GetGroupInfoRequest(RequestProtocol):
    """获取群基本信息（``QQBotAPI.get_group_info`` 请求参数）。"""

    group_openid: str


class GetGroupInfoResponse(ResponseProtocol):
    """获取群基本信息响应。"""

    result: GroupInfo | None = None


@qqbot_events.event
class GetGroupInfoRequestEvent(EventDeclaration):
    """获取群基本信息（请求事件 ``qqbot.api.get_group_info.request``）。"""

    name = 'qqbot.api.get_group_info.request'
    payload_type = GetGroupInfoRequest


@qqbot_events.event
class GetGroupInfoResponseEvent(EventDeclaration):
    """获取群基本信息（响应事件 ``qqbot.api.get_group_info.response``）。"""

    name = 'qqbot.api.get_group_info.response'
    payload_type = GetGroupInfoResponse


async def get_group_info(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> GroupInfo:
    """获取群基本信息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGroupInfoRequestEvent.name,
        req_data=req_data,
        resp_event=GetGroupInfoResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGroupInfoResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_group_bot_state —— 获取机器人群内状态
# ======================================================================


class GetGroupBotStateRequest(RequestProtocol):
    """获取机器人群内状态（``QQBotAPI.get_group_bot_state`` 请求参数）。"""

    group_openid: str


class GetGroupBotStateResponse(ResponseProtocol):
    """获取机器人群内状态响应。"""

    result: GroupBotState | None = None


@qqbot_events.event
class GetGroupBotStateRequestEvent(EventDeclaration):
    """获取机器人群内状态（请求事件 ``qqbot.api.get_group_bot_state.request``）。"""

    name = 'qqbot.api.get_group_bot_state.request'
    payload_type = GetGroupBotStateRequest


@qqbot_events.event
class GetGroupBotStateResponseEvent(EventDeclaration):
    """获取机器人群内状态（响应事件 ``qqbot.api.get_group_bot_state.response``）。"""

    name = 'qqbot.api.get_group_bot_state.response'
    payload_type = GetGroupBotStateResponse


async def get_group_bot_state(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> GroupBotState:
    """获取机器人群内状态（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGroupBotStateRequestEvent.name,
        req_data=req_data,
        resp_event=GetGroupBotStateResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGroupBotStateResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_group_members —— 获取群成员列表
# ======================================================================


class GetGroupMembersRequest(RequestProtocol):
    """获取群成员列表（``QQBotAPI.get_group_members`` 请求参数）。"""

    group_openid: str
    cursor: str | None = None


class GetGroupMembersResponse(ResponseProtocol):
    """获取群成员列表响应。"""

    result: GroupMemberPage | None = None


@qqbot_events.event
class GetGroupMembersRequestEvent(EventDeclaration):
    """获取群成员列表（请求事件 ``qqbot.api.get_group_members.request``）。"""

    name = 'qqbot.api.get_group_members.request'
    payload_type = GetGroupMembersRequest


@qqbot_events.event
class GetGroupMembersResponseEvent(EventDeclaration):
    """获取群成员列表（响应事件 ``qqbot.api.get_group_members.response``）。"""

    name = 'qqbot.api.get_group_members.response'
    payload_type = GetGroupMembersResponse


async def get_group_members(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    cursor: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> GroupMemberPage:
    """获取群成员列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'cursor': cursor,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGroupMembersRequestEvent.name,
        req_data=req_data,
        resp_event=GetGroupMembersResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGroupMembersResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_group_member —— 获取群成员信息
# ======================================================================


class GetGroupMemberRequest(RequestProtocol):
    """获取群成员信息（``QQBotAPI.get_group_member`` 请求参数）。"""

    group_openid: str
    member_openid: str


class GetGroupMemberResponse(ResponseProtocol):
    """获取群成员信息响应。"""

    result: GroupMember | None = None


@qqbot_events.event
class GetGroupMemberRequestEvent(EventDeclaration):
    """获取群成员信息（请求事件 ``qqbot.api.get_group_member.request``）。"""

    name = 'qqbot.api.get_group_member.request'
    payload_type = GetGroupMemberRequest


@qqbot_events.event
class GetGroupMemberResponseEvent(EventDeclaration):
    """获取群成员信息（响应事件 ``qqbot.api.get_group_member.response``）。"""

    name = 'qqbot.api.get_group_member.response'
    payload_type = GetGroupMemberResponse


async def get_group_member(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    member_openid: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> GroupMember:
    """获取群成员信息（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'member_openid': member_openid,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGroupMemberRequestEvent.name,
        req_data=req_data,
        resp_event=GetGroupMemberResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGroupMemberResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# batch_remove_group_members —— 群成员批量移除
# ======================================================================


class BatchRemoveGroupMembersRequest(RequestProtocol):
    """群成员批量移除（``QQBotAPI.batch_remove_group_members`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    group_openid: str
    members: list[str]


class BatchRemoveGroupMembersResponse(ResponseProtocol):
    """群成员批量移除响应。"""

    result: None = None


@qqbot_events.event
class BatchRemoveGroupMembersRequestEvent(EventDeclaration):
    """群成员批量移除（请求事件 ``qqbot.api.batch_remove_group_members.request``）。"""

    name = 'qqbot.api.batch_remove_group_members.request'
    payload_type = BatchRemoveGroupMembersRequest


@qqbot_events.event
class BatchRemoveGroupMembersResponseEvent(EventDeclaration):
    """群成员批量移除（响应事件 ``qqbot.api.batch_remove_group_members.response``）。"""

    name = 'qqbot.api.batch_remove_group_members.response'
    payload_type = BatchRemoveGroupMembersResponse


async def batch_remove_group_members(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    members: list[str],
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> None:
    """群成员批量移除（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'members': members,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=BatchRemoveGroupMembersRequestEvent.name,
        req_data=req_data,
        resp_event=BatchRemoveGroupMembersResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, BatchRemoveGroupMembersResponse)
    return response.result


# ======================================================================
# get_join_request_list —— 拉取入群申请列表
# ======================================================================


class GetJoinRequestListRequest(RequestProtocol):
    """拉取入群申请列表（``QQBotAPI.get_join_request_list`` 请求参数）。"""

    group_openid: str
    cursor: str | None = None
    limit: int | None = None


class GetJoinRequestListResponse(ResponseProtocol):
    """拉取入群申请列表响应。"""

    result: JoinRequestPage | None = None


@qqbot_events.event
class GetJoinRequestListRequestEvent(EventDeclaration):
    """拉取入群申请列表（请求事件 ``qqbot.api.get_join_request_list.request``）。"""

    name = 'qqbot.api.get_join_request_list.request'
    payload_type = GetJoinRequestListRequest


@qqbot_events.event
class GetJoinRequestListResponseEvent(EventDeclaration):
    """拉取入群申请列表（响应事件 ``qqbot.api.get_join_request_list.response``）。"""

    name = 'qqbot.api.get_join_request_list.response'
    payload_type = GetJoinRequestListResponse


async def get_join_request_list(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    cursor: str | None = None,
    limit: int | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> JoinRequestPage:
    """拉取入群申请列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'cursor': cursor,
        'limit': limit,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetJoinRequestListRequestEvent.name,
        req_data=req_data,
        resp_event=GetJoinRequestListResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetJoinRequestListResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# approval_join_request —— 入群申请审批
# ======================================================================


class ApprovalJoinRequestRequest(RequestProtocol):
    """入群申请审批（``QQBotAPI.approval_join_request`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    group_openid: str
    member_openid: str
    join_request_id: str | None = None
    approve: bool | None = None
    reason: str | None = None


class ApprovalJoinRequestResponse(ResponseProtocol):
    """入群申请审批响应。"""

    result: None = None


@qqbot_events.event
class ApprovalJoinRequestRequestEvent(EventDeclaration):
    """入群申请审批（请求事件 ``qqbot.api.approval_join_request.request``）。"""

    name = 'qqbot.api.approval_join_request.request'
    payload_type = ApprovalJoinRequestRequest


@qqbot_events.event
class ApprovalJoinRequestResponseEvent(EventDeclaration):
    """入群申请审批（响应事件 ``qqbot.api.approval_join_request.response``）。"""

    name = 'qqbot.api.approval_join_request.response'
    payload_type = ApprovalJoinRequestResponse


async def approval_join_request(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    member_openid: str,
    join_request_id: str | None = None,
    approve: bool | None = None,
    reason: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> None:
    """入群申请审批（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'member_openid': member_openid,
        'join_request_id': join_request_id,
        'approve': approve,
        'reason': reason,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=ApprovalJoinRequestRequestEvent.name,
        req_data=req_data,
        resp_event=ApprovalJoinRequestResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, ApprovalJoinRequestResponse)
    return response.result


# ======================================================================
# get_join_approval_strategies —— 查询入群自动审批策略列表
# ======================================================================


class GetJoinApprovalStrategiesRequest(RequestProtocol):
    """查询入群自动审批策略列表（``QQBotAPI.get_join_approval_strategies`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')


class GetJoinApprovalStrategiesResponse(ResponseProtocol):
    """查询入群自动审批策略列表响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class GetJoinApprovalStrategiesRequestEvent(EventDeclaration):
    """查询入群自动审批策略列表（请求事件 ``qqbot.api.get_join_approval_strategies.request``）。"""

    name = 'qqbot.api.get_join_approval_strategies.request'
    payload_type = GetJoinApprovalStrategiesRequest


@qqbot_events.event
class GetJoinApprovalStrategiesResponseEvent(EventDeclaration):
    """查询入群自动审批策略列表（响应事件 ``qqbot.api.get_join_approval_strategies.response``）。"""

    name = 'qqbot.api.get_join_approval_strategies.response'
    payload_type = GetJoinApprovalStrategiesResponse


async def get_join_approval_strategies(
    bus_proxy: EventBus.Proxy,
    *,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """查询入群自动审批策略列表（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {}
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetJoinApprovalStrategiesRequestEvent.name,
        req_data=req_data,
        resp_event=GetJoinApprovalStrategiesResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetJoinApprovalStrategiesResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# create_join_approval_strategy —— 创建入群自动审批策略
# ======================================================================


class CreateJoinApprovalStrategyRequest(RequestProtocol):
    """创建入群自动审批策略（``QQBotAPI.create_join_approval_strategy`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')


class CreateJoinApprovalStrategyResponse(ResponseProtocol):
    """创建入群自动审批策略响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class CreateJoinApprovalStrategyRequestEvent(EventDeclaration):
    """创建入群自动审批策略（请求事件 ``qqbot.api.create_join_approval_strategy.request``）。"""

    name = 'qqbot.api.create_join_approval_strategy.request'
    payload_type = CreateJoinApprovalStrategyRequest


@qqbot_events.event
class CreateJoinApprovalStrategyResponseEvent(EventDeclaration):
    """创建入群自动审批策略（响应事件 ``qqbot.api.create_join_approval_strategy.response``）。"""

    name = 'qqbot.api.create_join_approval_strategy.response'
    payload_type = CreateJoinApprovalStrategyResponse


async def create_join_approval_strategy(
    bus_proxy: EventBus.Proxy,
    *,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """创建入群自动审批策略（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {}
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=CreateJoinApprovalStrategyRequestEvent.name,
        req_data=req_data,
        resp_event=CreateJoinApprovalStrategyResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, CreateJoinApprovalStrategyResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# update_join_approval_strategy —— 修改入群自动审批策略
# ======================================================================


class UpdateJoinApprovalStrategyRequest(RequestProtocol):
    """修改入群自动审批策略（``QQBotAPI.update_join_approval_strategy`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    strategy_id: str


class UpdateJoinApprovalStrategyResponse(ResponseProtocol):
    """修改入群自动审批策略响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class UpdateJoinApprovalStrategyRequestEvent(EventDeclaration):
    """修改入群自动审批策略（请求事件 ``qqbot.api.update_join_approval_strategy.request``）。"""

    name = 'qqbot.api.update_join_approval_strategy.request'
    payload_type = UpdateJoinApprovalStrategyRequest


@qqbot_events.event
class UpdateJoinApprovalStrategyResponseEvent(EventDeclaration):
    """修改入群自动审批策略（响应事件 ``qqbot.api.update_join_approval_strategy.response``）。"""

    name = 'qqbot.api.update_join_approval_strategy.response'
    payload_type = UpdateJoinApprovalStrategyResponse


async def update_join_approval_strategy(
    bus_proxy: EventBus.Proxy,
    *,
    strategy_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """修改入群自动审批策略（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'strategy_id': strategy_id,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdateJoinApprovalStrategyRequestEvent.name,
        req_data=req_data,
        resp_event=UpdateJoinApprovalStrategyResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdateJoinApprovalStrategyResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# delete_join_approval_strategy —— 删除入群自动审批策略
# ======================================================================


class DeleteJoinApprovalStrategyRequest(RequestProtocol):
    """删除入群自动审批策略（``QQBotAPI.delete_join_approval_strategy`` 请求参数）。"""

    strategy_id: str


class DeleteJoinApprovalStrategyResponse(ResponseProtocol):
    """删除入群自动审批策略响应。"""

    result: None = None


@qqbot_events.event
class DeleteJoinApprovalStrategyRequestEvent(EventDeclaration):
    """删除入群自动审批策略（请求事件 ``qqbot.api.delete_join_approval_strategy.request``）。"""

    name = 'qqbot.api.delete_join_approval_strategy.request'
    payload_type = DeleteJoinApprovalStrategyRequest


@qqbot_events.event
class DeleteJoinApprovalStrategyResponseEvent(EventDeclaration):
    """删除入群自动审批策略（响应事件 ``qqbot.api.delete_join_approval_strategy.response``）。"""

    name = 'qqbot.api.delete_join_approval_strategy.response'
    payload_type = DeleteJoinApprovalStrategyResponse


async def delete_join_approval_strategy(
    bus_proxy: EventBus.Proxy,
    *,
    strategy_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """删除入群自动审批策略（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'strategy_id': strategy_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=DeleteJoinApprovalStrategyRequestEvent.name,
        req_data=req_data,
        resp_event=DeleteJoinApprovalStrategyResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, DeleteJoinApprovalStrategyResponse)
    return response.result


# ======================================================================
# execute_join_approval_strategy —— 执行入群自动审批策略
# ======================================================================


class ExecuteJoinApprovalStrategyRequest(RequestProtocol):
    """执行入群自动审批策略（``QQBotAPI.execute_join_approval_strategy`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    strategy_id: str


class ExecuteJoinApprovalStrategyResponse(ResponseProtocol):
    """执行入群自动审批策略响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class ExecuteJoinApprovalStrategyRequestEvent(EventDeclaration):
    """执行入群自动审批策略（请求事件 ``qqbot.api.execute_join_approval_strategy.request``）。"""

    name = 'qqbot.api.execute_join_approval_strategy.request'
    payload_type = ExecuteJoinApprovalStrategyRequest


@qqbot_events.event
class ExecuteJoinApprovalStrategyResponseEvent(EventDeclaration):
    """执行入群自动审批策略（响应事件 ``qqbot.api.execute_join_approval_strategy.response``）。"""

    name = 'qqbot.api.execute_join_approval_strategy.response'
    payload_type = ExecuteJoinApprovalStrategyResponse


async def execute_join_approval_strategy(
    bus_proxy: EventBus.Proxy,
    *,
    strategy_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """执行入群自动审批策略（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'strategy_id': strategy_id,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=ExecuteJoinApprovalStrategyRequestEvent.name,
        req_data=req_data,
        resp_event=ExecuteJoinApprovalStrategyResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, ExecuteJoinApprovalStrategyResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# update_join_approval_whitelist —— 修改入群自动审批策略白名单
# ======================================================================


class UpdateJoinApprovalWhitelistRequest(RequestProtocol):
    """修改入群自动审批策略白名单（``QQBotAPI.update_join_approval_whitelist`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    strategy_id: str


class UpdateJoinApprovalWhitelistResponse(ResponseProtocol):
    """修改入群自动审批策略白名单响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class UpdateJoinApprovalWhitelistRequestEvent(EventDeclaration):
    """修改入群自动审批策略白名单（请求事件 ``qqbot.api.update_join_approval_whitelist.request``）。"""

    name = 'qqbot.api.update_join_approval_whitelist.request'
    payload_type = UpdateJoinApprovalWhitelistRequest


@qqbot_events.event
class UpdateJoinApprovalWhitelistResponseEvent(EventDeclaration):
    """修改入群自动审批策略白名单（响应事件 ``qqbot.api.update_join_approval_whitelist.response``）。"""

    name = 'qqbot.api.update_join_approval_whitelist.response'
    payload_type = UpdateJoinApprovalWhitelistResponse


async def update_join_approval_whitelist(
    bus_proxy: EventBus.Proxy,
    *,
    strategy_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """修改入群自动审批策略白名单（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'strategy_id': strategy_id,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UpdateJoinApprovalWhitelistRequestEvent.name,
        req_data=req_data,
        resp_event=UpdateJoinApprovalWhitelistResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UpdateJoinApprovalWhitelistResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_group_blacklist —— 群黑名单查询
# ======================================================================


class GetGroupBlacklistRequest(RequestProtocol):
    """群黑名单查询（``QQBotAPI.get_group_blacklist`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    group_openid: str


class GetGroupBlacklistResponse(ResponseProtocol):
    """群黑名单查询响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class GetGroupBlacklistRequestEvent(EventDeclaration):
    """群黑名单查询（请求事件 ``qqbot.api.get_group_blacklist.request``）。"""

    name = 'qqbot.api.get_group_blacklist.request'
    payload_type = GetGroupBlacklistRequest


@qqbot_events.event
class GetGroupBlacklistResponseEvent(EventDeclaration):
    """群黑名单查询（响应事件 ``qqbot.api.get_group_blacklist.response``）。"""

    name = 'qqbot.api.get_group_blacklist.response'
    payload_type = GetGroupBlacklistResponse


async def get_group_blacklist(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """群黑名单查询（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGroupBlacklistRequestEvent.name,
        req_data=req_data,
        resp_event=GetGroupBlacklistResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGroupBlacklistResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# operate_group_blacklist —— 群黑名单操作
# ======================================================================


class OperateGroupBlacklistRequest(RequestProtocol):
    """群黑名单操作（``QQBotAPI.operate_group_blacklist`` 请求参数）。"""

    model_config = ConfigDict(extra='allow')

    group_openid: str


class OperateGroupBlacklistResponse(ResponseProtocol):
    """群黑名单操作响应。"""

    result: dict[str, Any] | None = None


@qqbot_events.event
class OperateGroupBlacklistRequestEvent(EventDeclaration):
    """群黑名单操作（请求事件 ``qqbot.api.operate_group_blacklist.request``）。"""

    name = 'qqbot.api.operate_group_blacklist.request'
    payload_type = OperateGroupBlacklistRequest


@qqbot_events.event
class OperateGroupBlacklistResponseEvent(EventDeclaration):
    """群黑名单操作（响应事件 ``qqbot.api.operate_group_blacklist.response``）。"""

    name = 'qqbot.api.operate_group_blacklist.response'
    payload_type = OperateGroupBlacklistResponse


async def operate_group_blacklist(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
    **extra: Any,
) -> dict[str, Any]:
    """群黑名单操作（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
    }
    req_data.update(extra)
    response = await request(
        bus_proxy=bus_proxy,
        req_event=OperateGroupBlacklistRequestEvent.name,
        req_data=req_data,
        resp_event=OperateGroupBlacklistResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, OperateGroupBlacklistResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# get_group_restrict_chat_setting —— 查询群禁言状态
# ======================================================================


class GetGroupRestrictChatSettingRequest(RequestProtocol):
    """查询群禁言状态（``QQBotAPI.get_group_restrict_chat_setting`` 请求参数）。"""

    group_openid: str


class GetGroupRestrictChatSettingResponse(ResponseProtocol):
    """查询群禁言状态响应。"""

    result: RestrictChatSetting | None = None


@qqbot_events.event
class GetGroupRestrictChatSettingRequestEvent(EventDeclaration):
    """查询群禁言状态（请求事件 ``qqbot.api.get_group_restrict_chat_setting.request``）。"""

    name = 'qqbot.api.get_group_restrict_chat_setting.request'
    payload_type = GetGroupRestrictChatSettingRequest


@qqbot_events.event
class GetGroupRestrictChatSettingResponseEvent(EventDeclaration):
    """查询群禁言状态（响应事件 ``qqbot.api.get_group_restrict_chat_setting.response``）。"""

    name = 'qqbot.api.get_group_restrict_chat_setting.response'
    payload_type = GetGroupRestrictChatSettingResponse


async def get_group_restrict_chat_setting(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> RestrictChatSetting:
    """查询群禁言状态（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GetGroupRestrictChatSettingRequestEvent.name,
        req_data=req_data,
        resp_event=GetGroupRestrictChatSettingResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GetGroupRestrictChatSettingResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# set_group_member_mute —— 设置群成员禁言
# ======================================================================


class SetGroupMemberMuteRequest(RequestProtocol):
    """设置群成员禁言（``QQBotAPI.set_group_member_mute`` 请求参数）。"""

    group_openid: str
    members: list[SetMemberMuteState]


class SetGroupMemberMuteResponse(ResponseProtocol):
    """设置群成员禁言响应。"""

    result: None = None


@qqbot_events.event
class SetGroupMemberMuteRequestEvent(EventDeclaration):
    """设置群成员禁言（请求事件 ``qqbot.api.set_group_member_mute.request``）。"""

    name = 'qqbot.api.set_group_member_mute.request'
    payload_type = SetGroupMemberMuteRequest


@qqbot_events.event
class SetGroupMemberMuteResponseEvent(EventDeclaration):
    """设置群成员禁言（响应事件 ``qqbot.api.set_group_member_mute.response``）。"""

    name = 'qqbot.api.set_group_member_mute.response'
    payload_type = SetGroupMemberMuteResponse


async def set_group_member_mute(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    members: list[SetMemberMuteState],
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """设置群成员禁言（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'members': members,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=SetGroupMemberMuteRequestEvent.name,
        req_data=req_data,
        resp_event=SetGroupMemberMuteResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, SetGroupMemberMuteResponse)
    return response.result

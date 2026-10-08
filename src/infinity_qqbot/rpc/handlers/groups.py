"""自动生成：groups RPC 处理器（显式关键字调用 ``QQBotAPI``）。

请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

from typing import Any

from event_bus import Event, EventBus
from event_bus.templates import ServiceHandler, process

from ...api import QQBotAPI
from ..groups import (
    ApprovalJoinRequestRequest,
    ApprovalJoinRequestRequestEvent,
    ApprovalJoinRequestResponseEvent,
    BatchRemoveGroupMembersRequest,
    BatchRemoveGroupMembersRequestEvent,
    BatchRemoveGroupMembersResponseEvent,
    CreateJoinApprovalStrategyRequest,
    CreateJoinApprovalStrategyRequestEvent,
    CreateJoinApprovalStrategyResponseEvent,
    DeleteJoinApprovalStrategyRequest,
    DeleteJoinApprovalStrategyRequestEvent,
    DeleteJoinApprovalStrategyResponseEvent,
    ExecuteJoinApprovalStrategyRequest,
    ExecuteJoinApprovalStrategyRequestEvent,
    ExecuteJoinApprovalStrategyResponseEvent,
    GetGroupBlacklistRequest,
    GetGroupBlacklistRequestEvent,
    GetGroupBlacklistResponseEvent,
    GetGroupBotStateRequest,
    GetGroupBotStateRequestEvent,
    GetGroupBotStateResponseEvent,
    GetGroupInfoRequest,
    GetGroupInfoRequestEvent,
    GetGroupInfoResponseEvent,
    GetGroupMemberRequest,
    GetGroupMemberRequestEvent,
    GetGroupMemberResponseEvent,
    GetGroupMembersRequest,
    GetGroupMembersRequestEvent,
    GetGroupMembersResponseEvent,
    GetGroupRestrictChatSettingRequest,
    GetGroupRestrictChatSettingRequestEvent,
    GetGroupRestrictChatSettingResponseEvent,
    GetJoinApprovalStrategiesRequest,
    GetJoinApprovalStrategiesRequestEvent,
    GetJoinApprovalStrategiesResponseEvent,
    GetJoinRequestListRequest,
    GetJoinRequestListRequestEvent,
    GetJoinRequestListResponseEvent,
    OperateGroupBlacklistRequest,
    OperateGroupBlacklistRequestEvent,
    OperateGroupBlacklistResponseEvent,
    SetGroupMemberMuteRequest,
    SetGroupMemberMuteRequestEvent,
    SetGroupMemberMuteResponseEvent,
    UpdateJoinApprovalStrategyRequest,
    UpdateJoinApprovalStrategyRequestEvent,
    UpdateJoinApprovalStrategyResponseEvent,
    UpdateJoinApprovalWhitelistRequest,
    UpdateJoinApprovalWhitelistRequestEvent,
    UpdateJoinApprovalWhitelistResponseEvent,
)

__all__ = ['GroupHandlersMixin']


class GroupHandlersMixin(ServiceHandler):
    """groups RPC 处理器 mixin。"""

    _api: QQBotAPI

    @process(GetGroupInfoRequestEvent, GetGroupInfoResponseEvent)
    async def get_group_info(
        self,
        payload: GetGroupInfoRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取群基本信息。"""
        result = await self._api.get_group_info(
            group_openid=payload.group_openid,
        )
        return {'result': result}

    @process(GetGroupBotStateRequestEvent, GetGroupBotStateResponseEvent)
    async def get_group_bot_state(
        self,
        payload: GetGroupBotStateRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取机器人群内状态。"""
        result = await self._api.get_group_bot_state(
            group_openid=payload.group_openid,
        )
        return {'result': result}

    @process(GetGroupMembersRequestEvent, GetGroupMembersResponseEvent)
    async def get_group_members(
        self,
        payload: GetGroupMembersRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取群成员列表。"""
        result = await self._api.get_group_members(
            group_openid=payload.group_openid,
            cursor=payload.cursor,
        )
        return {'result': result}

    @process(GetGroupMemberRequestEvent, GetGroupMemberResponseEvent)
    async def get_group_member(
        self,
        payload: GetGroupMemberRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取群成员信息。"""
        result = await self._api.get_group_member(
            group_openid=payload.group_openid,
            member_openid=payload.member_openid,
        )
        return {'result': result}

    @process(BatchRemoveGroupMembersRequestEvent, BatchRemoveGroupMembersResponseEvent)
    async def batch_remove_group_members(
        self,
        payload: BatchRemoveGroupMembersRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """群成员批量移除。"""
        await self._api.batch_remove_group_members(
            group_openid=payload.group_openid,
            members=payload.members,
            **(payload.model_extra or {}),
        )
        return {'result': None}

    @process(GetJoinRequestListRequestEvent, GetJoinRequestListResponseEvent)
    async def get_join_request_list(
        self,
        payload: GetJoinRequestListRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """拉取入群申请列表。"""
        result = await self._api.get_join_request_list(
            group_openid=payload.group_openid,
            cursor=payload.cursor,
            limit=payload.limit,
        )
        return {'result': result}

    @process(ApprovalJoinRequestRequestEvent, ApprovalJoinRequestResponseEvent)
    async def approval_join_request(
        self,
        payload: ApprovalJoinRequestRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """入群申请审批。"""
        await self._api.approval_join_request(
            group_openid=payload.group_openid,
            member_openid=payload.member_openid,
            join_request_id=payload.join_request_id,
            approve=payload.approve,
            reason=payload.reason,
            **(payload.model_extra or {}),
        )
        return {'result': None}

    @process(GetJoinApprovalStrategiesRequestEvent, GetJoinApprovalStrategiesResponseEvent)
    async def get_join_approval_strategies(
        self,
        payload: GetJoinApprovalStrategiesRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """查询入群自动审批策略列表。"""
        result = await self._api.get_join_approval_strategies(
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(CreateJoinApprovalStrategyRequestEvent, CreateJoinApprovalStrategyResponseEvent)
    async def create_join_approval_strategy(
        self,
        payload: CreateJoinApprovalStrategyRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建入群自动审批策略。"""
        result = await self._api.create_join_approval_strategy(
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(UpdateJoinApprovalStrategyRequestEvent, UpdateJoinApprovalStrategyResponseEvent)
    async def update_join_approval_strategy(
        self,
        payload: UpdateJoinApprovalStrategyRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改入群自动审批策略。"""
        result = await self._api.update_join_approval_strategy(
            strategy_id=payload.strategy_id,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(DeleteJoinApprovalStrategyRequestEvent, DeleteJoinApprovalStrategyResponseEvent)
    async def delete_join_approval_strategy(
        self,
        payload: DeleteJoinApprovalStrategyRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除入群自动审批策略。"""
        await self._api.delete_join_approval_strategy(
            strategy_id=payload.strategy_id,
        )
        return {'result': None}

    @process(ExecuteJoinApprovalStrategyRequestEvent, ExecuteJoinApprovalStrategyResponseEvent)
    async def execute_join_approval_strategy(
        self,
        payload: ExecuteJoinApprovalStrategyRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """执行入群自动审批策略。"""
        result = await self._api.execute_join_approval_strategy(
            strategy_id=payload.strategy_id,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(UpdateJoinApprovalWhitelistRequestEvent, UpdateJoinApprovalWhitelistResponseEvent)
    async def update_join_approval_whitelist(
        self,
        payload: UpdateJoinApprovalWhitelistRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改入群自动审批策略白名单。"""
        result = await self._api.update_join_approval_whitelist(
            strategy_id=payload.strategy_id,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(GetGroupBlacklistRequestEvent, GetGroupBlacklistResponseEvent)
    async def get_group_blacklist(
        self,
        payload: GetGroupBlacklistRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """群黑名单查询。"""
        result = await self._api.get_group_blacklist(
            group_openid=payload.group_openid,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(OperateGroupBlacklistRequestEvent, OperateGroupBlacklistResponseEvent)
    async def operate_group_blacklist(
        self,
        payload: OperateGroupBlacklistRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """群黑名单操作。"""
        result = await self._api.operate_group_blacklist(
            group_openid=payload.group_openid,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(GetGroupRestrictChatSettingRequestEvent, GetGroupRestrictChatSettingResponseEvent)
    async def get_group_restrict_chat_setting(
        self,
        payload: GetGroupRestrictChatSettingRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """查询群禁言状态。"""
        result = await self._api.get_group_restrict_chat_setting(
            group_openid=payload.group_openid,
        )
        return {'result': result}

    @process(SetGroupMemberMuteRequestEvent, SetGroupMemberMuteResponseEvent)
    async def set_group_member_mute(
        self,
        payload: SetGroupMemberMuteRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """设置群成员禁言。"""
        await self._api.set_group_member_mute(
            group_openid=payload.group_openid,
            members=payload.members,
        )
        return {'result': None}

"""自动生成：channels RPC 处理器（显式关键字调用 ``QQBotAPI``）。

请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

from typing import Any

from event_bus import Event, EventBus
from event_bus.templates import ServiceHandler, process

from ...api import QQBotAPI
from ..channels import (
    AddPinRequest,
    AddPinRequestEvent,
    AddPinResponseEvent,
    AddReactionRequest,
    AddReactionRequestEvent,
    AddReactionResponseEvent,
    AddRoleMemberRequest,
    AddRoleMemberRequestEvent,
    AddRoleMemberResponseEvent,
    CreateApiPermissionDemandRequest,
    CreateApiPermissionDemandRequestEvent,
    CreateApiPermissionDemandResponseEvent,
    CreateChannelAnnounceRequest,
    CreateChannelAnnounceRequestEvent,
    CreateChannelAnnounceResponseEvent,
    CreateDmSessionRequest,
    CreateDmSessionRequestEvent,
    CreateDmSessionResponseEvent,
    CreateGuildAnnounceRequest,
    CreateGuildAnnounceRequestEvent,
    CreateGuildAnnounceResponseEvent,
    CreateGuildChannelRequest,
    CreateGuildChannelRequestEvent,
    CreateGuildChannelResponseEvent,
    CreateGuildRoleRequest,
    CreateGuildRoleRequestEvent,
    CreateGuildRoleResponseEvent,
    CreateScheduleRequest,
    CreateScheduleRequestEvent,
    CreateScheduleResponseEvent,
    DeleteChannelAnnounceRequest,
    DeleteChannelAnnounceRequestEvent,
    DeleteChannelAnnounceResponseEvent,
    DeleteChannelRequest,
    DeleteChannelRequestEvent,
    DeleteChannelResponseEvent,
    DeleteGuildAnnounceRequest,
    DeleteGuildAnnounceRequestEvent,
    DeleteGuildAnnounceResponseEvent,
    DeleteGuildRoleRequest,
    DeleteGuildRoleRequestEvent,
    DeleteGuildRoleResponseEvent,
    DeletePinRequest,
    DeletePinRequestEvent,
    DeletePinResponseEvent,
    DeleteReactionRequest,
    DeleteReactionRequestEvent,
    DeleteReactionResponseEvent,
    DeleteScheduleRequest,
    DeleteScheduleRequestEvent,
    DeleteScheduleResponseEvent,
    GetApiPermissionRequest,
    GetApiPermissionRequestEvent,
    GetApiPermissionResponseEvent,
    GetChannelMessageRequest,
    GetChannelMessageRequestEvent,
    GetChannelMessageResponseEvent,
    GetChannelRequest,
    GetChannelRequestEvent,
    GetChannelResponseEvent,
    GetGuildChannelsRequest,
    GetGuildChannelsRequestEvent,
    GetGuildChannelsResponseEvent,
    GetGuildMemberRequest,
    GetGuildMemberRequestEvent,
    GetGuildMemberResponseEvent,
    GetGuildMembersRequest,
    GetGuildMembersRequestEvent,
    GetGuildMembersResponseEvent,
    GetGuildRequest,
    GetGuildRequestEvent,
    GetGuildResponseEvent,
    GetGuildRolesRequest,
    GetGuildRolesRequestEvent,
    GetGuildRolesResponseEvent,
    GetPinsRequest,
    GetPinsRequestEvent,
    GetPinsResponseEvent,
    GetReactionsRequest,
    GetReactionsRequestEvent,
    GetReactionsResponseEvent,
    GetScheduleRequest,
    GetScheduleRequestEvent,
    GetScheduleResponseEvent,
    GetSchedulesRequest,
    GetSchedulesRequestEvent,
    GetSchedulesResponseEvent,
    MuteGuildMemberRequest,
    MuteGuildMemberRequestEvent,
    MuteGuildMemberResponseEvent,
    MuteGuildRequest,
    MuteGuildRequestEvent,
    MuteGuildResponseEvent,
    RecallChannelMessageRequest,
    RecallChannelMessageRequestEvent,
    RecallChannelMessageResponseEvent,
    RecallDmMessageRequest,
    RecallDmMessageRequestEvent,
    RecallDmMessageResponseEvent,
    RemoveGuildMemberRequest,
    RemoveGuildMemberRequestEvent,
    RemoveGuildMemberResponseEvent,
    RemoveRoleMemberRequest,
    RemoveRoleMemberRequestEvent,
    RemoveRoleMemberResponseEvent,
    SendChannelMessageRequest,
    SendChannelMessageRequestEvent,
    SendChannelMessageResponseEvent,
    SendDmMessageRequest,
    SendDmMessageRequestEvent,
    SendDmMessageResponseEvent,
    UpdateChannelRequest,
    UpdateChannelRequestEvent,
    UpdateChannelResponseEvent,
    UpdateGuildRoleRequest,
    UpdateGuildRoleRequestEvent,
    UpdateGuildRoleResponseEvent,
    UpdateScheduleRequest,
    UpdateScheduleRequestEvent,
    UpdateScheduleResponseEvent,
)

__all__ = ['ChannelHandlersMixin']


class ChannelHandlersMixin(ServiceHandler):
    """channels RPC 处理器 mixin。"""

    _api: QQBotAPI

    @process(GetGuildRequestEvent, GetGuildResponseEvent)
    async def get_guild(
        self,
        payload: GetGuildRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取频道详情。"""
        result = await self._api.get_guild(
            guild_id=payload.guild_id,
        )
        return {'result': result}

    @process(GetGuildChannelsRequestEvent, GetGuildChannelsResponseEvent)
    async def get_guild_channels(
        self,
        payload: GetGuildChannelsRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取子频道列表。"""
        result = await self._api.get_guild_channels(
            guild_id=payload.guild_id,
        )
        return {'result': result}

    @process(CreateGuildChannelRequestEvent, CreateGuildChannelResponseEvent)
    async def create_guild_channel(
        self,
        payload: CreateGuildChannelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建子频道。"""
        result = await self._api.create_guild_channel(
            guild_id=payload.guild_id,
            name=payload.name,
            type=payload.type,
            position=payload.position,
            parent_id=payload.parent_id,
            sub_type=payload.sub_type,
            private_type=payload.private_type,
            private_user_limit=payload.private_user_limit,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(GetChannelRequestEvent, GetChannelResponseEvent)
    async def get_channel(
        self,
        payload: GetChannelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取子频道详情。"""
        result = await self._api.get_channel(
            channel_id=payload.channel_id,
        )
        return {'result': result}

    @process(UpdateChannelRequestEvent, UpdateChannelResponseEvent)
    async def update_channel(
        self,
        payload: UpdateChannelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改子频道。"""
        result = await self._api.update_channel(
            channel_id=payload.channel_id,
            name=payload.name,
            position=payload.position,
            parent_id=payload.parent_id,
            private_type=payload.private_type,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(DeleteChannelRequestEvent, DeleteChannelResponseEvent)
    async def delete_channel(
        self,
        payload: DeleteChannelRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除子频道。"""
        await self._api.delete_channel(
            channel_id=payload.channel_id,
        )
        return {'result': None}

    @process(SendChannelMessageRequestEvent, SendChannelMessageResponseEvent)
    async def send_channel_message(
        self,
        payload: SendChannelMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """发送子频道消息。"""
        result = await self._api.send_channel_message(
            channel_id=payload.channel_id,
            content=payload.content,
            embed=payload.embed,
            ark=payload.ark,
            image=payload.image,
            msg_id=payload.msg_id,
            event_id=payload.event_id,
            markdown=payload.markdown,
            message_reference=payload.message_reference,
        )
        return {'result': result}

    @process(GetChannelMessageRequestEvent, GetChannelMessageResponseEvent)
    async def get_channel_message(
        self,
        payload: GetChannelMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取子频道消息。"""
        result = await self._api.get_channel_message(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
        )
        return {'result': result}

    @process(RecallChannelMessageRequestEvent, RecallChannelMessageResponseEvent)
    async def recall_channel_message(
        self,
        payload: RecallChannelMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """撤回子频道消息。"""
        await self._api.recall_channel_message(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
            hidetip=payload.hidetip,
        )
        return {'result': None}

    @process(CreateDmSessionRequestEvent, CreateDmSessionResponseEvent)
    async def create_dm_session(
        self,
        payload: CreateDmSessionRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建频道私信会话。"""
        result = await self._api.create_dm_session(
            recipient_id=payload.recipient_id,
            source_guild_id=payload.source_guild_id,
        )
        return {'result': result}

    @process(SendDmMessageRequestEvent, SendDmMessageResponseEvent)
    async def send_dm_message(
        self,
        payload: SendDmMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """发送频道私信。"""
        result = await self._api.send_dm_message(
            guild_id=payload.guild_id,
            content=payload.content,
            embed=payload.embed,
            ark=payload.ark,
            image=payload.image,
            msg_id=payload.msg_id,
            event_id=payload.event_id,
            markdown=payload.markdown,
            message_reference=payload.message_reference,
        )
        return {'result': result}

    @process(RecallDmMessageRequestEvent, RecallDmMessageResponseEvent)
    async def recall_dm_message(
        self,
        payload: RecallDmMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """撤回频道私信。"""
        await self._api.recall_dm_message(
            guild_id=payload.guild_id,
            message_id=payload.message_id,
            hidetip=payload.hidetip,
        )
        return {'result': None}

    @process(GetGuildMembersRequestEvent, GetGuildMembersResponseEvent)
    async def get_guild_members(
        self,
        payload: GetGuildMembersRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取频道成员列表。"""
        result = await self._api.get_guild_members(
            guild_id=payload.guild_id,
            after=payload.after,
            limit=payload.limit,
        )
        return {'result': result}

    @process(GetGuildMemberRequestEvent, GetGuildMemberResponseEvent)
    async def get_guild_member(
        self,
        payload: GetGuildMemberRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取频道成员详情。"""
        result = await self._api.get_guild_member(
            guild_id=payload.guild_id,
            user_id=payload.user_id,
        )
        return {'result': result}

    @process(RemoveGuildMemberRequestEvent, RemoveGuildMemberResponseEvent)
    async def remove_guild_member(
        self,
        payload: RemoveGuildMemberRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """移除频道成员。"""
        await self._api.remove_guild_member(
            guild_id=payload.guild_id,
            user_id=payload.user_id,
            add_blacklist=payload.add_blacklist,
            delete_history_msg_days=payload.delete_history_msg_days,
        )
        return {'result': None}

    @process(GetGuildRolesRequestEvent, GetGuildRolesResponseEvent)
    async def get_guild_roles(
        self,
        payload: GetGuildRolesRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取频道身份组列表。"""
        result = await self._api.get_guild_roles(
            guild_id=payload.guild_id,
            limit=payload.limit,
        )
        return {'result': result}

    @process(CreateGuildRoleRequestEvent, CreateGuildRoleResponseEvent)
    async def create_guild_role(
        self,
        payload: CreateGuildRoleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建频道身份组。"""
        result = await self._api.create_guild_role(
            guild_id=payload.guild_id,
            name=payload.name,
            color=payload.color,
            hoist=payload.hoist,
            mentionable=payload.mentionable,
            **(payload.model_extra or {}),
        )
        return {'result': result}

    @process(UpdateGuildRoleRequestEvent, UpdateGuildRoleResponseEvent)
    async def update_guild_role(
        self,
        payload: UpdateGuildRoleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改频道身份组。"""
        result = await self._api.update_guild_role(
            guild_id=payload.guild_id,
            role_id=payload.role_id,
            name=payload.name,
            color=payload.color,
            hoist=payload.hoist,
        )
        return {'result': result}

    @process(DeleteGuildRoleRequestEvent, DeleteGuildRoleResponseEvent)
    async def delete_guild_role(
        self,
        payload: DeleteGuildRoleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除频道身份组。"""
        await self._api.delete_guild_role(
            guild_id=payload.guild_id,
            role_id=payload.role_id,
        )
        return {'result': None}

    @process(AddRoleMemberRequestEvent, AddRoleMemberResponseEvent)
    async def add_role_member(
        self,
        payload: AddRoleMemberRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """添加身份组成员。"""
        await self._api.add_role_member(
            guild_id=payload.guild_id,
            user_id=payload.user_id,
            role_id=payload.role_id,
            channel_id=payload.channel_id,
        )
        return {'result': None}

    @process(RemoveRoleMemberRequestEvent, RemoveRoleMemberResponseEvent)
    async def remove_role_member(
        self,
        payload: RemoveRoleMemberRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """移除身份组成员。"""
        await self._api.remove_role_member(
            guild_id=payload.guild_id,
            user_id=payload.user_id,
            role_id=payload.role_id,
            channel_id=payload.channel_id,
        )
        return {'result': None}

    @process(MuteGuildRequestEvent, MuteGuildResponseEvent)
    async def mute_guild(
        self,
        payload: MuteGuildRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """频道全员禁言。"""
        await self._api.mute_guild(
            guild_id=payload.guild_id,
            mute_seconds=payload.mute_seconds,
            mute_end_timestamp=payload.mute_end_timestamp,
        )
        return {'result': None}

    @process(MuteGuildMemberRequestEvent, MuteGuildMemberResponseEvent)
    async def mute_guild_member(
        self,
        payload: MuteGuildMemberRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """指定成员禁言。"""
        await self._api.mute_guild_member(
            guild_id=payload.guild_id,
            user_id=payload.user_id,
            mute_seconds=payload.mute_seconds,
            mute_end_timestamp=payload.mute_end_timestamp,
        )
        return {'result': None}

    @process(CreateGuildAnnounceRequestEvent, CreateGuildAnnounceResponseEvent)
    async def create_guild_announce(
        self,
        payload: CreateGuildAnnounceRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建频道公告。"""
        result = await self._api.create_guild_announce(
            guild_id=payload.guild_id,
            message_id=payload.message_id,
            channel_id=payload.channel_id,
            announces_type=payload.announces_type,
            recommend_channels=payload.recommend_channels,
        )
        return {'result': result}

    @process(DeleteGuildAnnounceRequestEvent, DeleteGuildAnnounceResponseEvent)
    async def delete_guild_announce(
        self,
        payload: DeleteGuildAnnounceRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除频道公告。"""
        await self._api.delete_guild_announce(
            guild_id=payload.guild_id,
            message_id=payload.message_id,
        )
        return {'result': None}

    @process(CreateChannelAnnounceRequestEvent, CreateChannelAnnounceResponseEvent)
    async def create_channel_announce(
        self,
        payload: CreateChannelAnnounceRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建子频道公告。"""
        result = await self._api.create_channel_announce(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
            announces_type=payload.announces_type,
        )
        return {'result': result}

    @process(DeleteChannelAnnounceRequestEvent, DeleteChannelAnnounceResponseEvent)
    async def delete_channel_announce(
        self,
        payload: DeleteChannelAnnounceRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除子频道公告。"""
        await self._api.delete_channel_announce(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
        )
        return {'result': None}

    @process(GetApiPermissionRequestEvent, GetApiPermissionResponseEvent)
    async def get_api_permission(
        self,
        payload: GetApiPermissionRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取频道可用权限列表。"""
        result = await self._api.get_api_permission(
            guild_id=payload.guild_id,
        )
        return {'result': result}

    @process(CreateApiPermissionDemandRequestEvent, CreateApiPermissionDemandResponseEvent)
    async def create_api_permission_demand(
        self,
        payload: CreateApiPermissionDemandRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建频道 API 接口权限授权链接。"""
        result = await self._api.create_api_permission_demand(
            guild_id=payload.guild_id,
            channel_id=payload.channel_id,
            api_identify=payload.api_identify,
            desc=payload.desc,
        )
        return {'result': result}

    @process(AddReactionRequestEvent, AddReactionResponseEvent)
    async def add_reaction(
        self,
        payload: AddReactionRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """添加表情表态。"""
        await self._api.add_reaction(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
            emoji_type=payload.emoji_type,
            emoji_id=payload.emoji_id,
        )
        return {'result': None}

    @process(DeleteReactionRequestEvent, DeleteReactionResponseEvent)
    async def delete_reaction(
        self,
        payload: DeleteReactionRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除表情表态。"""
        await self._api.delete_reaction(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
            emoji_type=payload.emoji_type,
            emoji_id=payload.emoji_id,
        )
        return {'result': None}

    @process(GetReactionsRequestEvent, GetReactionsResponseEvent)
    async def get_reactions(
        self,
        payload: GetReactionsRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取表情表态用户列表。"""
        result = await self._api.get_reactions(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
            emoji_type=payload.emoji_type,
            emoji_id=payload.emoji_id,
        )
        return {'result': result}

    @process(AddPinRequestEvent, AddPinResponseEvent)
    async def add_pin(
        self,
        payload: AddPinRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """添加精华消息。"""
        await self._api.add_pin(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
        )
        return {'result': None}

    @process(DeletePinRequestEvent, DeletePinResponseEvent)
    async def delete_pin(
        self,
        payload: DeletePinRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除精华消息。"""
        await self._api.delete_pin(
            channel_id=payload.channel_id,
            message_id=payload.message_id,
        )
        return {'result': None}

    @process(GetPinsRequestEvent, GetPinsResponseEvent)
    async def get_pins(
        self,
        payload: GetPinsRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取精华消息列表。"""
        result = await self._api.get_pins(
            channel_id=payload.channel_id,
        )
        return {'result': result}

    @process(GetSchedulesRequestEvent, GetSchedulesResponseEvent)
    async def get_schedules(
        self,
        payload: GetSchedulesRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取日程列表。"""
        result = await self._api.get_schedules(
            channel_id=payload.channel_id,
            since=payload.since,
        )
        return {'result': result}

    @process(CreateScheduleRequestEvent, CreateScheduleResponseEvent)
    async def create_schedule(
        self,
        payload: CreateScheduleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """创建日程。"""
        result = await self._api.create_schedule(
            channel_id=payload.channel_id,
            schedule=payload.schedule,
        )
        return {'result': result}

    @process(GetScheduleRequestEvent, GetScheduleResponseEvent)
    async def get_schedule(
        self,
        payload: GetScheduleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """获取日程详情。"""
        result = await self._api.get_schedule(
            channel_id=payload.channel_id,
            schedule_id=payload.schedule_id,
        )
        return {'result': result}

    @process(UpdateScheduleRequestEvent, UpdateScheduleResponseEvent)
    async def update_schedule(
        self,
        payload: UpdateScheduleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """修改日程。"""
        result = await self._api.update_schedule(
            channel_id=payload.channel_id,
            schedule_id=payload.schedule_id,
            schedule=payload.schedule,
        )
        return {'result': result}

    @process(DeleteScheduleRequestEvent, DeleteScheduleResponseEvent)
    async def delete_schedule(
        self,
        payload: DeleteScheduleRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """删除日程。"""
        await self._api.delete_schedule(
            channel_id=payload.channel_id,
            schedule_id=payload.schedule_id,
        )
        return {'result': None}

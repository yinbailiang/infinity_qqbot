"""QQBot 事件声明（嵌套 ``Payload`` 风格 + 装饰器注册）。

每个事件声明直接继承 ``infinity_bus.EventDeclaration``，显式声明三件套：

- ``type_name``：QQ 平台事件名（网关 ``t`` 字段）；
- ``name``：总线事件名（``qqbot.event.<type_name 小写>``）；
- ``payload_type``：嵌套 ``Payload`` 负载类。

并用库自带装饰器 ``@qqbot_events.event`` 登记到模块事件注册器
（``infinity_bus.templates.ModuleEventRegister``），注册时直接调用
``qqbot_events.register_all_events(registry)``。

示例::

    @qqbot_events.event
    class GroupAtMessageCreateEvent(EventDeclaration):
        type_name = 'GROUP_AT_MESSAGE_CREATE'
        name = 'qqbot.event.group_at_message_create'

        class Payload(QQMessageEventPayload):
            group_openid: str | None = None

        payload_type = Payload
"""

from __future__ import annotations

from typing import Any

from infinity_bus import EventDeclaration
from infinity_bus.templates import ModuleEventRegister
from pydantic import BaseModel

from .models import (
    AudioEventPayload,
    AudioOrLiveChannelMemberEventPayload,
    ChannelEventPayload,
    ChannelMessageDeleteEventPayload,
    ChannelMessageEventPayload,
    ForumEventPayload,
    FriendEventPayload,
    GroupJoinRequestEventPayload,
    GroupMemberEventPayload,
    GroupRobotEventPayload,
    GuildEventPayload,
    GuildMemberEventPayload,
    InteractionEventPayload,
    MessageAuditEventPayload,
    MsgReceiveSwitchEventPayload,
    OpenForumEventPayload,
    QQBotEventPayload,
    QQMessageEventPayload,
    ReactionEventPayload,
    ReadyEventPayload,
    SubscribeMessageStatusEventPayload,
    UnknownEventPayload,
)

__all__ = [
    'ALL_EVENTS',
    'EVENT_BY_TYPE',
    'AtMessageCreateEvent',
    'AudioFinishEvent',
    'AudioOffMicEvent',
    'AudioOnMicEvent',
    'AudioOrLiveChannelMemberEnterEvent',
    'AudioOrLiveChannelMemberExitEvent',
    'AudioStartEvent',
    'C2CMessageCreateEvent',
    'C2CMsgReceiveEvent',
    'C2CMsgRejectEvent',
    'ChannelCreateEvent',
    'ChannelDeleteEvent',
    'ChannelUpdateEvent',
    'DirectMessageCreateEvent',
    'DirectMessageDeleteEvent',
    'ForumPostCreateEvent',
    'ForumPostDeleteEvent',
    'ForumPublishAuditResultEvent',
    'ForumReplyCreateEvent',
    'ForumReplyDeleteEvent',
    'ForumThreadCreateEvent',
    'ForumThreadDeleteEvent',
    'ForumThreadUpdateEvent',
    'FriendAddEvent',
    'FriendDelEvent',
    'GroupAddRobotEvent',
    'GroupAtMessageCreateEvent',
    'GroupDelRobotEvent',
    'GroupJoinRequestEvent',
    'GroupMemberAddEvent',
    'GroupMemberRemoveEvent',
    'GroupMessageCreateEvent',
    'GroupMsgReceiveEvent',
    'GroupMsgRejectEvent',
    'GuildCreateEvent',
    'GuildDeleteEvent',
    'GuildMemberAddEvent',
    'GuildMemberRemoveEvent',
    'GuildMemberUpdateEvent',
    'GuildUpdateEvent',
    'InteractionCreateEvent',
    'MessageAuditPassEvent',
    'MessageAuditRejectEvent',
    'MessageCreateEvent',
    'MessageDeleteEvent',
    'MessageReactionAddEvent',
    'MessageReactionRemoveEvent',
    'OpenForumPostCreateEvent',
    'OpenForumPostDeleteEvent',
    'OpenForumReplyCreateEvent',
    'OpenForumReplyDeleteEvent',
    'OpenForumThreadCreateEvent',
    'OpenForumThreadDeleteEvent',
    'OpenForumThreadUpdateEvent',
    'PublicMessageDeleteEvent',
    'ReadyEvent',
    'ResumedEvent',
    'SubscribeMessageStatusEvent',
    'UnknownEvent',
    'qqbot_events',
    'resolve_event',
]


#: 事件模块注册器：事件声明通过 ``@qqbot_events.event`` 装饰器登记
qqbot_events = ModuleEventRegister('infinity_qqbot')


# ======================================================================
# 网关元事件
# ======================================================================


@qqbot_events.event
class ReadyEvent(EventDeclaration):
    """网关鉴权成功（READY）。"""

    type_name = 'READY'
    name = 'qqbot.event.ready'

    class Payload(ReadyEventPayload):
        """网关就绪负载：包含 ``session_id`` 与会话基本信息。"""

    payload_type = Payload


@qqbot_events.event
class ResumedEvent(EventDeclaration):
    """网关恢复会话成功（RESUMED）。"""

    type_name = 'RESUMED'
    name = 'qqbot.event.resumed'

    class Payload(QQBotEventPayload):
        """恢复会话负载（通常为空）。"""

    payload_type = Payload


# ======================================================================
# 频道管理
# ======================================================================


@qqbot_events.event
class GuildCreateEvent(EventDeclaration):
    """机器人加入新频道（GUILD_CREATE）。"""

    type_name = 'GUILD_CREATE'
    name = 'qqbot.event.guild_create'

    class Payload(GuildEventPayload):
        """频道对象。"""

    payload_type = Payload


@qqbot_events.event
class GuildUpdateEvent(EventDeclaration):
    """频道资料变更（GUILD_UPDATE）。"""

    type_name = 'GUILD_UPDATE'
    name = 'qqbot.event.guild_update'

    class Payload(GuildEventPayload):
        """频道对象。"""

    payload_type = Payload


@qqbot_events.event
class GuildDeleteEvent(EventDeclaration):
    """机器人退出频道（GUILD_DELETE）。"""

    type_name = 'GUILD_DELETE'
    name = 'qqbot.event.guild_delete'

    class Payload(GuildEventPayload):
        """频道对象。"""

    payload_type = Payload


@qqbot_events.event
class ChannelCreateEvent(EventDeclaration):
    """子频道创建（CHANNEL_CREATE）。"""

    type_name = 'CHANNEL_CREATE'
    name = 'qqbot.event.channel_create'

    class Payload(ChannelEventPayload):
        """子频道对象。"""

    payload_type = Payload


@qqbot_events.event
class ChannelUpdateEvent(EventDeclaration):
    """子频道更新（CHANNEL_UPDATE）。"""

    type_name = 'CHANNEL_UPDATE'
    name = 'qqbot.event.channel_update'

    class Payload(ChannelEventPayload):
        """子频道对象。"""

    payload_type = Payload


@qqbot_events.event
class ChannelDeleteEvent(EventDeclaration):
    """子频道删除（CHANNEL_DELETE）。"""

    type_name = 'CHANNEL_DELETE'
    name = 'qqbot.event.channel_delete'

    class Payload(ChannelEventPayload):
        """子频道对象。"""

    payload_type = Payload


# ======================================================================
# 频道成员
# ======================================================================


@qqbot_events.event
class GuildMemberAddEvent(EventDeclaration):
    """成员加入频道（GUILD_MEMBER_ADD）。"""

    type_name = 'GUILD_MEMBER_ADD'
    name = 'qqbot.event.guild_member_add'

    class Payload(GuildMemberEventPayload):
        """频道成员对象（含 ``guild_id``）。"""

    payload_type = Payload


@qqbot_events.event
class GuildMemberUpdateEvent(EventDeclaration):
    """成员资料变更（GUILD_MEMBER_UPDATE）。"""

    type_name = 'GUILD_MEMBER_UPDATE'
    name = 'qqbot.event.guild_member_update'

    class Payload(GuildMemberEventPayload):
        """频道成员对象（含 ``guild_id``）。"""

    payload_type = Payload


@qqbot_events.event
class GuildMemberRemoveEvent(EventDeclaration):
    """成员被移除（GUILD_MEMBER_REMOVE）。"""

    type_name = 'GUILD_MEMBER_REMOVE'
    name = 'qqbot.event.guild_member_remove'

    class Payload(GuildMemberEventPayload):
        """频道成员对象（含 ``guild_id``）。"""

    payload_type = Payload


# ======================================================================
# 频道消息
# ======================================================================


@qqbot_events.event
class MessageCreateEvent(EventDeclaration):
    """频道全量消息（MESSAGE_CREATE，仅私域机器人）。"""

    type_name = 'MESSAGE_CREATE'
    name = 'qqbot.event.message_create'

    class Payload(ChannelMessageEventPayload):
        """频道消息对象。"""

    payload_type = Payload


@qqbot_events.event
class AtMessageCreateEvent(EventDeclaration):
    """收到 @机器人 的频道消息（AT_MESSAGE_CREATE，公域）。"""

    type_name = 'AT_MESSAGE_CREATE'
    name = 'qqbot.event.at_message_create'

    class Payload(ChannelMessageEventPayload):
        """频道 @ 消息对象。"""

    payload_type = Payload


@qqbot_events.event
class MessageDeleteEvent(EventDeclaration):
    """频道消息被删除 / 撤回（MESSAGE_DELETE）。"""

    type_name = 'MESSAGE_DELETE'
    name = 'qqbot.event.message_delete'

    class Payload(ChannelMessageDeleteEventPayload):
        """消息删除事件负载。"""

    payload_type = Payload


@qqbot_events.event
class PublicMessageDeleteEvent(EventDeclaration):
    """公域频道消息被删除 / 撤回（PUBLIC_MESSAGE_DELETE）。"""

    type_name = 'PUBLIC_MESSAGE_DELETE'
    name = 'qqbot.event.public_message_delete'

    class Payload(ChannelMessageDeleteEventPayload):
        """消息删除事件负载。"""

    payload_type = Payload


@qqbot_events.event
class DirectMessageCreateEvent(EventDeclaration):
    """频道私信消息（DIRECT_MESSAGE_CREATE）。"""

    type_name = 'DIRECT_MESSAGE_CREATE'
    name = 'qqbot.event.direct_message_create'

    class Payload(ChannelMessageEventPayload):
        """频道私信消息对象。"""

    payload_type = Payload


@qqbot_events.event
class DirectMessageDeleteEvent(EventDeclaration):
    """频道私信被删除 / 撤回（DIRECT_MESSAGE_DELETE）。"""

    type_name = 'DIRECT_MESSAGE_DELETE'
    name = 'qqbot.event.direct_message_delete'

    class Payload(ChannelMessageDeleteEventPayload):
        """私信删除事件负载。"""

    payload_type = Payload


@qqbot_events.event
class MessageReactionAddEvent(EventDeclaration):
    """消息表情表态添加（MESSAGE_REACTION_ADD）。"""

    type_name = 'MESSAGE_REACTION_ADD'
    name = 'qqbot.event.message_reaction_add'

    class Payload(ReactionEventPayload):
        """表情表态事件负载。"""

    payload_type = Payload


@qqbot_events.event
class MessageReactionRemoveEvent(EventDeclaration):
    """消息表情表态删除（MESSAGE_REACTION_REMOVE）。"""

    type_name = 'MESSAGE_REACTION_REMOVE'
    name = 'qqbot.event.message_reaction_remove'

    class Payload(ReactionEventPayload):
        """表情表态事件负载。"""

    payload_type = Payload


@qqbot_events.event
class MessageAuditPassEvent(EventDeclaration):
    """消息审核通过（MESSAGE_AUDIT_PASS）。"""

    type_name = 'MESSAGE_AUDIT_PASS'
    name = 'qqbot.event.message_audit_pass'

    class Payload(MessageAuditEventPayload):
        """消息审核事件负载。"""

    payload_type = Payload


@qqbot_events.event
class MessageAuditRejectEvent(EventDeclaration):
    """消息审核不通过（MESSAGE_AUDIT_REJECT）。"""

    type_name = 'MESSAGE_AUDIT_REJECT'
    name = 'qqbot.event.message_audit_reject'

    class Payload(MessageAuditEventPayload):
        """消息审核事件负载。"""

    payload_type = Payload


# ======================================================================
# 群聊 / 单聊
# ======================================================================


@qqbot_events.event
class C2CMessageCreateEvent(EventDeclaration):
    """用户单聊发消息给机器人（C2C_MESSAGE_CREATE）。"""

    type_name = 'C2C_MESSAGE_CREATE'
    name = 'qqbot.event.c2c_message_create'

    class Payload(QQMessageEventPayload):
        """单聊消息负载（``author.user_openid`` 有值）。"""

        user_openid: str | None = None

    payload_type = Payload


@qqbot_events.event
class FriendAddEvent(EventDeclaration):
    """用户添加机器人（FRIEND_ADD）。"""

    type_name = 'FRIEND_ADD'
    name = 'qqbot.event.friend_add'

    class Payload(FriendEventPayload):
        """好友关系事件负载。"""

    payload_type = Payload


@qqbot_events.event
class FriendDelEvent(EventDeclaration):
    """用户删除机器人（FRIEND_DEL）。"""

    type_name = 'FRIEND_DEL'
    name = 'qqbot.event.friend_del'

    class Payload(FriendEventPayload):
        """好友关系事件负载。"""

    payload_type = Payload


@qqbot_events.event
class C2CMsgReceiveEvent(EventDeclaration):
    """用户开启主动消息推送（C2C_MSG_RECEIVE）。"""

    type_name = 'C2C_MSG_RECEIVE'
    name = 'qqbot.event.c2c_msg_receive'

    class Payload(MsgReceiveSwitchEventPayload):
        """消息接收开关事件负载。"""

    payload_type = Payload


@qqbot_events.event
class C2CMsgRejectEvent(EventDeclaration):
    """用户关闭主动消息推送（C2C_MSG_REJECT）。"""

    type_name = 'C2C_MSG_REJECT'
    name = 'qqbot.event.c2c_msg_reject'

    class Payload(MsgReceiveSwitchEventPayload):
        """消息接收开关事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupAtMessageCreateEvent(EventDeclaration):
    """用户在群里 @机器人 发消息（GROUP_AT_MESSAGE_CREATE）。"""

    type_name = 'GROUP_AT_MESSAGE_CREATE'
    name = 'qqbot.event.group_at_message_create'

    class Payload(QQMessageEventPayload):
        """群 @ 消息负载（``author.member_openid`` 有值）。"""

        group_openid: str | None = None

    payload_type = Payload


@qqbot_events.event
class GroupMessageCreateEvent(EventDeclaration):
    """群全量消息（GROUP_MESSAGE_CREATE）。"""

    type_name = 'GROUP_MESSAGE_CREATE'
    name = 'qqbot.event.group_message_create'

    class Payload(QQMessageEventPayload):
        """群消息负载。"""

        group_openid: str | None = None

    payload_type = Payload


@qqbot_events.event
class GroupAddRobotEvent(EventDeclaration):
    """机器人被添加到群聊（GROUP_ADD_ROBOT）。"""

    type_name = 'GROUP_ADD_ROBOT'
    name = 'qqbot.event.group_add_robot'

    class Payload(GroupRobotEventPayload):
        """机器人出入群事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupDelRobotEvent(EventDeclaration):
    """机器人被移出群聊（GROUP_DEL_ROBOT）。"""

    type_name = 'GROUP_DEL_ROBOT'
    name = 'qqbot.event.group_del_robot'

    class Payload(GroupRobotEventPayload):
        """机器人出入群事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupMsgReceiveEvent(EventDeclaration):
    """群管理员开启通知（GROUP_MSG_RECEIVE）。"""

    type_name = 'GROUP_MSG_RECEIVE'
    name = 'qqbot.event.group_msg_receive'

    class Payload(MsgReceiveSwitchEventPayload):
        """消息接收开关事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupMsgRejectEvent(EventDeclaration):
    """群管理员关闭通知（GROUP_MSG_REJECT）。"""

    type_name = 'GROUP_MSG_REJECT'
    name = 'qqbot.event.group_msg_reject'

    class Payload(MsgReceiveSwitchEventPayload):
        """消息接收开关事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupJoinRequestEvent(EventDeclaration):
    """用户申请加群（GROUP_JOIN_REQUEST）。"""

    type_name = 'GROUP_JOIN_REQUEST'
    name = 'qqbot.event.group_join_request'

    class Payload(GroupJoinRequestEventPayload):
        """入群申请事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupMemberAddEvent(EventDeclaration):
    """群成员加入（GROUP_MEMBER_ADD）。"""

    type_name = 'GROUP_MEMBER_ADD'
    name = 'qqbot.event.group_member_add'

    class Payload(GroupMemberEventPayload):
        """群成员事件负载。"""

    payload_type = Payload


@qqbot_events.event
class GroupMemberRemoveEvent(EventDeclaration):
    """群成员退出（GROUP_MEMBER_REMOVE）。"""

    type_name = 'GROUP_MEMBER_REMOVE'
    name = 'qqbot.event.group_member_remove'

    class Payload(GroupMemberEventPayload):
        """群成员事件负载。"""

    payload_type = Payload


# ======================================================================
# 互动
# ======================================================================


@qqbot_events.event
class InteractionCreateEvent(EventDeclaration):
    """互动事件（INTERACTION_CREATE）。"""

    type_name = 'INTERACTION_CREATE'
    name = 'qqbot.event.interaction_create'

    class Payload(InteractionEventPayload):
        """互动事件负载，收到后可使用 ``PUT /interactions/{id}`` 回应。"""

    payload_type = Payload


# ======================================================================
# 论坛（仅私域机器人）
# ======================================================================


@qqbot_events.event
class ForumThreadCreateEvent(EventDeclaration):
    """用户创建主题（FORUM_THREAD_CREATE）。"""

    type_name = 'FORUM_THREAD_CREATE'
    name = 'qqbot.event.forum_thread_create'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumThreadUpdateEvent(EventDeclaration):
    """用户更新主题（FORUM_THREAD_UPDATE）。"""

    type_name = 'FORUM_THREAD_UPDATE'
    name = 'qqbot.event.forum_thread_update'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumThreadDeleteEvent(EventDeclaration):
    """用户删除主题（FORUM_THREAD_DELETE）。"""

    type_name = 'FORUM_THREAD_DELETE'
    name = 'qqbot.event.forum_thread_delete'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumPostCreateEvent(EventDeclaration):
    """用户创建帖子（FORUM_POST_CREATE）。"""

    type_name = 'FORUM_POST_CREATE'
    name = 'qqbot.event.forum_post_create'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumPostDeleteEvent(EventDeclaration):
    """用户删除帖子（FORUM_POST_DELETE）。"""

    type_name = 'FORUM_POST_DELETE'
    name = 'qqbot.event.forum_post_delete'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumReplyCreateEvent(EventDeclaration):
    """用户回复评论（FORUM_REPLY_CREATE）。"""

    type_name = 'FORUM_REPLY_CREATE'
    name = 'qqbot.event.forum_reply_create'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumReplyDeleteEvent(EventDeclaration):
    """用户删除评论（FORUM_REPLY_DELETE）。"""

    type_name = 'FORUM_REPLY_DELETE'
    name = 'qqbot.event.forum_reply_delete'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class ForumPublishAuditResultEvent(EventDeclaration):
    """论坛帖子审核结果（FORUM_PUBLISH_AUDIT_RESULT）。"""

    type_name = 'FORUM_PUBLISH_AUDIT_RESULT'
    name = 'qqbot.event.forum_publish_audit_result'

    class Payload(ForumEventPayload):
        """论坛事件负载。"""

    payload_type = Payload


# ======================================================================
# 开放论坛（OPEN_FORUM_EVENT，仅私域）
# ======================================================================


@qqbot_events.event
class OpenForumThreadCreateEvent(EventDeclaration):
    """用户创建主题（OPEN_FORUM_THREAD_CREATE）。"""

    type_name = 'OPEN_FORUM_THREAD_CREATE'
    name = 'qqbot.event.open_forum_thread_create'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class OpenForumThreadUpdateEvent(EventDeclaration):
    """用户更新主题（OPEN_FORUM_THREAD_UPDATE）。"""

    type_name = 'OPEN_FORUM_THREAD_UPDATE'
    name = 'qqbot.event.open_forum_thread_update'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class OpenForumThreadDeleteEvent(EventDeclaration):
    """用户删除主题（OPEN_FORUM_THREAD_DELETE）。"""

    type_name = 'OPEN_FORUM_THREAD_DELETE'
    name = 'qqbot.event.open_forum_thread_delete'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class OpenForumPostCreateEvent(EventDeclaration):
    """用户创建帖子（OPEN_FORUM_POST_CREATE）。"""

    type_name = 'OPEN_FORUM_POST_CREATE'
    name = 'qqbot.event.open_forum_post_create'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class OpenForumPostDeleteEvent(EventDeclaration):
    """用户删除帖子（OPEN_FORUM_POST_DELETE）。"""

    type_name = 'OPEN_FORUM_POST_DELETE'
    name = 'qqbot.event.open_forum_post_delete'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class OpenForumReplyCreateEvent(EventDeclaration):
    """用户回复评论（OPEN_FORUM_REPLY_CREATE）。"""

    type_name = 'OPEN_FORUM_REPLY_CREATE'
    name = 'qqbot.event.open_forum_reply_create'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


@qqbot_events.event
class OpenForumReplyDeleteEvent(EventDeclaration):
    """用户删除评论（OPEN_FORUM_REPLY_DELETE）。"""

    type_name = 'OPEN_FORUM_REPLY_DELETE'
    name = 'qqbot.event.open_forum_reply_delete'

    class Payload(OpenForumEventPayload):
        """开放论坛事件负载。"""

    payload_type = Payload


# ======================================================================
# 音频
# ======================================================================


@qqbot_events.event
class AudioStartEvent(EventDeclaration):
    """音频开始播放（AUDIO_START）。"""

    type_name = 'AUDIO_START'
    name = 'qqbot.event.audio_start'

    class Payload(AudioEventPayload):
        """音频事件负载。"""

    payload_type = Payload


@qqbot_events.event
class AudioFinishEvent(EventDeclaration):
    """音频播放结束（AUDIO_FINISH）。"""

    type_name = 'AUDIO_FINISH'
    name = 'qqbot.event.audio_finish'

    class Payload(AudioEventPayload):
        """音频事件负载。"""

    payload_type = Payload


@qqbot_events.event
class AudioOnMicEvent(EventDeclaration):
    """上麦（AUDIO_ON_MIC）。"""

    type_name = 'AUDIO_ON_MIC'
    name = 'qqbot.event.audio_on_mic'

    class Payload(AudioEventPayload):
        """音频事件负载。"""

    payload_type = Payload


@qqbot_events.event
class AudioOffMicEvent(EventDeclaration):
    """下麦（AUDIO_OFF_MIC）。"""

    type_name = 'AUDIO_OFF_MIC'
    name = 'qqbot.event.audio_off_mic'

    class Payload(AudioEventPayload):
        """音频事件负载。"""

    payload_type = Payload


@qqbot_events.event
class AudioOrLiveChannelMemberEnterEvent(EventDeclaration):
    """用户进入音视频/直播子频道（AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER）。"""

    type_name = 'AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER'
    name = 'qqbot.event.audio_or_live_channel_member_enter'

    class Payload(AudioOrLiveChannelMemberEventPayload):
        """音视频/直播子频道成员事件负载。"""

    payload_type = Payload


@qqbot_events.event
class AudioOrLiveChannelMemberExitEvent(EventDeclaration):
    """用户离开音视频/直播子频道（AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT）。"""

    type_name = 'AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT'
    name = 'qqbot.event.audio_or_live_channel_member_exit'

    class Payload(AudioOrLiveChannelMemberEventPayload):
        """音视频/直播子频道成员事件负载。"""

    payload_type = Payload


# ======================================================================
# 其他
# ======================================================================


@qqbot_events.event
class SubscribeMessageStatusEvent(EventDeclaration):
    """订阅消息授权状态变更（SUBSCRIBE_MESSAGE_STATUS）。"""

    type_name = 'SUBSCRIBE_MESSAGE_STATUS'
    name = 'qqbot.event.subscribe_message_status'

    class Payload(SubscribeMessageStatusEventPayload):
        """订阅消息授权事件负载。"""

    payload_type = Payload


@qqbot_events.event
class UnknownEvent(EventDeclaration):
    """未建模事件的兜底声明：``qqbot.event.unknown``。"""

    name = 'qqbot.event.unknown'

    class Payload(UnknownEventPayload):
        """透传的原始事件数据。"""

    payload_type = Payload


#: 全部 QQ 网关事件声明：由 ``qqbot_events`` 收集，按总线事件名排序
ALL_EVENTS: tuple[type[EventDeclaration], ...] = tuple(sorted(qqbot_events.events, key=lambda decl: decl.name))

#: 平台事件类型 -> 声明类 的映射（用于网关事件解析）
EVENT_BY_TYPE: dict[str, type[EventDeclaration]] = {
    type_name: decl for decl in ALL_EVENTS if (type_name := getattr(decl, 'type_name', None)) is not None
}


def resolve_event(type_name: str, data: Any) -> tuple[type[EventDeclaration], BaseModel]:
    """把网关下发的 ``t`` / ``d`` 解析为（事件声明类，负载实例）。

    未建模事件返回 :class:`UnknownEvent` 与 :class:`UnknownEventPayload`；
    负载非字典时以 ``{"raw_data": data}`` 包装（如 ``RESUMED`` 的空负载）。
    """
    decl = EVENT_BY_TYPE.get(type_name)
    if decl is None or decl.payload_type is None:
        payload = UnknownEventPayload(type=type_name, data=data)
        return UnknownEvent, payload
    if not isinstance(data, dict):
        data = {'raw_data': data}
    return decl, decl.payload_type.model_validate(data)

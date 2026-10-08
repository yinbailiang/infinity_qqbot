"""事件负载基础模型（供 ``events.py`` 中的嵌套 ``Payload`` 继承）。"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .base import QQModel
from .common import Channel, Guild, GuildMember, User
from .interaction import InteractionData
from .message import ARKData, MessageAttachment, MessageReference, MessageScene, MsgElement
from .responses import ReactionEmoji, ReactionTarget

__all__ = [
    'AudioEventPayload',
    'ChannelEventPayload',
    'ChannelMessageDeleteEventPayload',
    'ChannelMessageEventPayload',
    'ForumEventPayload',
    'FriendEventPayload',
    'GroupJoinRequestEventPayload',
    'GroupMemberEventPayload',
    'GroupRobotEventPayload',
    'GuildEventPayload',
    'GuildMemberEventPayload',
    'InteractionEventPayload',
    'MessageAuditEventPayload',
    'MsgReceiveSwitchEventPayload',
    'QQBotEventPayload',
    'QQMessageEventPayload',
    'ReactionEventPayload',
    'ReadyEventPayload',
    'SubscribeMessageStatusEventPayload',
    'UnknownEventPayload',
]


class QQBotEventPayload(QQModel):
    """事件负载基类：允许携带平台新增字段。"""


class ReadyEventPayload(QQBotEventPayload):
    """``READY`` 网关就绪事件负载。"""

    version: int | None = Field(default=None, description='版本号')
    session_id: str | None = Field(default=None, description='会话 ID，用于 resume')
    user: User | None = Field(default=None, description='机器人用户')
    shard: list[int] | None = Field(default=None, description='分片信息')


class GuildEventPayload(Guild):
    """频道事件负载（GUILD_CREATE / UPDATE / DELETE）。"""


class ChannelEventPayload(Channel):
    """子频道事件负载（CHANNEL_CREATE / UPDATE / DELETE）。"""


class GuildMemberEventPayload(GuildMember):
    """频道成员事件负载（GUILD_MEMBER_ADD / UPDATE / REMOVE）。"""

    guild_id: str | None = Field(default=None, description='频道 ID')


class ChannelMessageEventPayload(QQBotEventPayload):
    """频道消息事件负载（MESSAGE_CREATE / AT_MESSAGE_CREATE / DIRECT_MESSAGE_CREATE）。"""

    id: str = Field(description='消息 ID，可用于被动回复和撤回')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    guild_id: str | None = Field(default=None, description='频道 ID')
    content: str | None = Field(default=None, description='消息内容')
    timestamp: str | None = Field(default=None, description='消息发送时间')
    edited_timestamp: str | None = Field(default=None, description='编辑时间')
    mention_everyone: bool | None = Field(default=None, description='是否 @全体')
    mentions: list[User] = Field(default_factory=list[User], description='@用户列表')
    member: GuildMember | None = Field(default=None, description='发送者成员信息')
    author: User | None = Field(default=None, description='发送者用户')
    attachments: list[MessageAttachment] = Field(default_factory=list[MessageAttachment], description='附件列表')
    embeds: list[Any] = Field(default_factory=list, description='embed 列表')
    ark: Any = Field(default=None, description='ark 消息')
    reference: MessageReference | None = Field(default=None, description='引用消息')
    type: int | None = Field(default=None, description='消息类型')
    flags: int | None = Field(default=None, description='消息标志位')
    pinned: bool | None = Field(default=None, description='是否精华消息')
    seq: int | None = Field(default=None, description='消息序列号')
    seq_in_channel: str | None = Field(default=None, description='子频道内消息序列号')


class ChannelMessageDeleteEventPayload(QQBotEventPayload):
    """频道消息撤回事件负载（MESSAGE_DELETE / PUBLIC_MESSAGE_DELETE / DIRECT_MESSAGE_DELETE）。"""

    id: str = Field(description='被撤回消息 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    guild_id: str | None = Field(default=None, description='频道 ID')
    op_user: User | None = Field(default=None, description='操作者')


class ReactionEventPayload(QQBotEventPayload):
    """表情表态事件负载（MESSAGE_REACTION_ADD / REMOVE）。"""

    user_id: str | None = Field(default=None, description='表态用户 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    guild_id: str | None = Field(default=None, description='频道 ID')
    target: ReactionTarget | None = Field(default=None, description='表态目标')
    emoji: ReactionEmoji | None = Field(default=None, description='表情')


class QQMessageEventPayload(QQBotEventPayload):
    """群聊 / 单聊消息事件负载（C2C_MESSAGE_CREATE / GROUP_AT_MESSAGE_CREATE 等）。"""

    id: str = Field(description='消息 ID，可用于被动回复和撤回')
    author: User | None = Field(default=None, description='发送者')
    content: str | None = Field(default=None, description='消息文本内容')
    timestamp: str | None = Field(default=None, description='消息发送时间（RFC3339）')
    message_type: int | None = Field(
        default=None, description='0 普通文本 / 3 卡片 / 101 并行 / 102 聊天记录 / 103 引用'
    )
    message_scene: MessageScene | None = Field(default=None, description='消息场景上下文')
    attachments: list[MessageAttachment] = Field(default_factory=list[MessageAttachment], description='消息附件')
    mentions: list[User] = Field(default_factory=list[User], description='@用户列表')
    ark_data: ARKData | None = Field(default=None, description='结构化卡片数据')
    msg_elements: list[MsgElement] = Field(default_factory=list['MsgElement'], description='消息元素列表')


class FriendEventPayload(QQBotEventPayload):
    """好友关系事件负载（FRIEND_ADD / FRIEND_DEL）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    openid: str | None = Field(default=None, description='用户 OpenID')


class MsgReceiveSwitchEventPayload(QQBotEventPayload):
    """消息接收开关事件负载（C2C_MSG_RECEIVE / REJECT、GROUP_MSG_RECEIVE / REJECT）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    openid: str | None = Field(default=None, description='用户 / 群 OpenID')


class GroupRobotEventPayload(QQBotEventPayload):
    """机器人出入群事件负载（GROUP_ADD_ROBOT / GROUP_DEL_ROBOT）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    group_openid: str | None = Field(default=None, description='群 OpenID')
    op_member_openid: str | None = Field(default=None, description='操作者 OpenID')


class GroupMemberEventPayload(QQBotEventPayload):
    """群成员出入群事件负载（GROUP_MEMBER_ADD / GROUP_MEMBER_REMOVE）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    group_openid: str | None = Field(default=None, description='群 OpenID')
    member_openid: str | None = Field(default=None, description='成员 OpenID')
    op_member_openid: str | None = Field(default=None, description='操作者 OpenID')


class GroupJoinRequestEventPayload(QQBotEventPayload):
    """用户申请加群事件负载（GROUP_JOIN_REQUEST）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    group_openid: str | None = Field(default=None, description='群 OpenID')
    member_openid: str | None = Field(default=None, description='申请人 OpenID')
    join_request_id: str | None = Field(default=None, description='申请 ID')


class InteractionEventPayload(QQBotEventPayload):
    """互动事件负载（INTERACTION_CREATE）。"""

    id: str = Field(description='事件 ID，用于被动消息发送和互动回调')
    type: int | None = Field(default=None, description='互动类型，见 InteractionType')
    scene: str | None = Field(default=None, description='c2c / group / guild')
    chat_type: int | None = Field(default=None, description='0 频道 / 1 群聊 / 2 单聊')
    timestamp: str | None = Field(default=None, description='触发时间')
    guild_id: str | None = Field(default=None, description='频道 OpenID（仅频道场景）')
    channel_id: str | None = Field(default=None, description='子频道 OpenID（仅频道场景）')
    user_openid: str | None = Field(default=None, description='用户 OpenID（仅单聊场景）')
    group_openid: str | None = Field(default=None, description='群 OpenID（仅群聊场景）')
    group_member_openid: str | None = Field(default=None, description='群成员 OpenID（仅群聊场景）')
    data: InteractionData | None = Field(default=None, description='互动数据')
    version: int | None = Field(default=None, description='版本号')
    application_id: str | None = Field(default=None, description='机器人 AppID')


class MessageAuditEventPayload(QQBotEventPayload):
    """消息审核事件负载（MESSAGE_AUDIT_PASS / MESSAGE_AUDIT_REJECT）。"""

    audit_id: str | None = Field(default=None, description='审核 ID')
    message_id: str | None = Field(default=None, description='消息 ID')
    guild_id: str | None = Field(default=None, description='频道 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    audit_time: str | None = Field(default=None, description='审核时间')
    create_time: str | None = Field(default=None, description='消息创建时间')
    seq: int | None = Field(default=None, description='消息序列号')
    seq_in_channel: str | None = Field(default=None, description='子频道内消息序列号')
    reason: str | None = Field(default=None, description='审核不通过原因')


class ForumEventPayload(QQBotEventPayload):
    """论坛事件负载（仅私域机器人，字段随平台更新）。"""

    guild_id: str | None = Field(default=None, description='频道 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    thread: dict[str, Any] | None = Field(default=None, description='主题数据')
    post: dict[str, Any] | None = Field(default=None, description='帖子数据')
    reply: dict[str, Any] | None = Field(default=None, description='评论数据')
    author: User | None = Field(default=None, description='作者')
    timestamp: str | None = Field(default=None, description='事件时间')


class AudioEventPayload(QQBotEventPayload):
    """音频事件负载（AUDIO_START / FINISH / ON_MIC / OFF_MIC）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    guild_id: str | None = Field(default=None, description='频道 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    audio_id: str | None = Field(default=None, description='音频 ID')


class SubscribeMessageStatusEventPayload(QQBotEventPayload):
    """订阅消息授权状态变更事件负载（SUBSCRIBE_MESSAGE_STATUS）。"""

    timestamp: str | None = Field(default=None, description='事件时间')
    openid: str | None = Field(default=None, description='用户 OpenID')
    scope: str | None = Field(default=None, description='授权范围')
    status: str | None = Field(default=None, description='授权状态')


class UnknownEventPayload(QQBotEventPayload):
    """未建模事件的透传负载。"""

    type: str = Field(description='QQ 平台事件类型')
    data: Any = Field(default=None, description='原始事件数据')
    event_id: str | None = Field(default=None, description='事件 ID')
    sequence: int | None = Field(default=None, description='事件序列号')

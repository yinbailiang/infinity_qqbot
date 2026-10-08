"""平台枚举：Intents / OpCode / 消息类型 / 互动类型 / 聊天场景。"""

from __future__ import annotations

from enum import IntEnum, IntFlag

__all__ = [
    'ChatScene',
    'Intents',
    'InteractionType',
    'OpCode',
    'SendMessageType',
]


class Intents(IntFlag):
    """事件订阅 Intents 位标记（与官方文档一一对应）。"""

    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    DIRECT_MESSAGE = 1 << 12
    OPEN_FORUMS_EVENT = 1 << 18
    AUDIO_OR_LIVE_CHANNEL_MEMBER = 1 << 19
    GROUP_AND_C2C_EVENT = 1 << 25
    INTERACTION = 1 << 26
    MESSAGE_AUDIT = 1 << 27
    FORUMS_EVENT = 1 << 28
    AUDIO_ACTION = 1 << 29
    PUBLIC_GUILD_MESSAGES = 1 << 30

    #: 常用默认组合：群聊/单聊 + 频道@消息 + 频道与成员基础事件
    DEFAULT = GROUP_AND_C2C_EVENT | PUBLIC_GUILD_MESSAGES | GUILDS | GUILD_MEMBERS


class OpCode(IntEnum):
    """网关上下行消息 OpCode。"""

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    RESUME = 6
    RECONNECT = 7
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class SendMessageType(IntEnum):
    """发送消息的 ``msg_type`` 取值。"""

    TEXT = 0
    MARKDOWN = 2
    INPUT_NOTIFY = 6
    MEDIA = 7


class InteractionType(IntEnum):
    """``INTERACTION_CREATE`` 互动事件类型。"""

    INLINE_KEYBOARD = 11
    CALLBACK_COMMAND = 12
    MESSAGE_FEEDBACK = 13
    CLEAR_SESSION = 14
    IN_OUT_STORY = 15
    SWITCH_MODEL = 16
    USER_AUTHORIZE = 18
    GROUP_AUTHORIZE = 19


class ChatScene(IntEnum):
    """互动事件聊天场景 ``chat_type``。"""

    CHANNEL = 0
    GROUP = 1
    C2C = 2

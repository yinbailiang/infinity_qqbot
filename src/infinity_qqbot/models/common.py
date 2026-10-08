"""基础对象：用户、频道、子频道、成员、身份组、私信会话。"""

from __future__ import annotations

from pydantic import Field

from .base import QQModel

__all__ = [
    'DMS',
    'Channel',
    'Guild',
    'GuildMember',
    'Role',
    'User',
]


class User(QQModel):
    """用户 / 成员用户对象。"""

    id: str | None = Field(default=None, description='用户唯一标识（OpenID 格式）')
    username: str | None = Field(default=None, description='用户昵称')
    avatar: str | None = Field(default=None, description='头像地址')
    bot: bool | None = Field(default=None, description='是否为机器人')
    union_openid: str | None = Field(default=None, description='跨应用统一用户 OpenID')
    union_user_account: str | None = Field(default=None, description='跨应用统一用户账号')
    user_openid: str | None = Field(default=None, description='单聊场景用户 OpenID')
    member_openid: str | None = Field(default=None, description='群聊场景成员 OpenID')
    member_role: str | None = Field(default=None, description='群内角色：member/admin/owner')


class Guild(QQModel):
    """频道（Guild）对象。"""

    id: str = Field(description='频道 ID')
    name: str | None = Field(default=None, description='频道名称')
    icon: str | None = Field(default=None, description='频道头像')
    owner_id: str | None = Field(default=None, description='频道创建者 ID')
    owner: bool | None = Field(default=None, description='当前用户是否为频道创建者')
    member_count: int | None = Field(default=None, description='频道成员数')
    max_members: int | None = Field(default=None, description='频道成员上限')
    description: str | None = Field(default=None, description='频道简介')
    joined_at: str | None = Field(default=None, description='加入时间')


class Channel(QQModel):
    """子频道对象。"""

    id: str = Field(description='子频道 ID')
    guild_id: str | None = Field(default=None, description='所属频道 ID')
    name: str | None = Field(default=None, description='子频道名称')
    type: int | None = Field(default=None, description='子频道类型（0 文字 / 2 语音 / 4 分组）')
    sub_type: int | None = Field(default=None, description='子频道子类型')
    position: int | None = Field(default=None, description='排序位置')
    parent_id: str | None = Field(default=None, description='分组 ID')
    owner_id: str | None = Field(default=None, description='创建者 ID')
    private_type: int | None = Field(default=None, description='私密类型')
    private_user_limit: int | None = Field(default=None, description='私密子频道人员上限')
    permissions: str | None = Field(default=None, description='权限位')
    op_user: User | None = Field(default=None, description='操作者')


class GuildMember(QQModel):
    """频道成员对象。"""

    user: User | None = Field(default=None, description='用户对象')
    nick: str | None = Field(default=None, description='频道昵称')
    roles: list[str] = Field(default_factory=list, description='身份组 ID 列表')
    joined_at: str | None = Field(default=None, description='加入时间')
    deaf: bool | None = Field(default=None, description='是否被耳语')
    mute: bool | None = Field(default=None, description='是否被禁言')
    pending: bool | None = Field(default=None, description='是否待审批')


class Role(QQModel):
    """频道身份组对象。"""

    id: str = Field(description='身份组 ID')
    name: str | None = Field(default=None, description='身份组名称')
    color: int | None = Field(default=None, description='颜色 ARGB')
    hoist: int | None = Field(default=None, description='是否在成员列表单独展示')
    number: int | None = Field(default=None, description='成员数量')
    member_limit: int | None = Field(default=None, description='可容纳成员数')
    permissions: str | None = Field(default=None, description='权限位')
    managed: bool | None = Field(default=None, description='是否为管理身份组')


class DMS(QQModel):
    """频道私信会话对象。"""

    guild_id: str = Field(description='私信会话关联的频道 ID')
    channel_id: str = Field(description='私信会话关联的子频道 ID')
    create_time: str | None = Field(default=None, description='创建时间戳')

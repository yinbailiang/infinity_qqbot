"""群聊对象：群信息、群成员、入群申请、禁言。"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import QQModel

__all__ = [
    'GroupBotState',
    'GroupInfo',
    'GroupMember',
    'GroupMemberPage',
    'JoinRequest',
    'JoinRequestPage',
    'JoinRequestVerifyInfo',
    'RestrictChatSetting',
    'ReviewQA',
    'SetMemberMuteState',
]


class GroupInfo(QQModel):
    """群基本信息。"""

    group_openid: str = Field(description='群 OpenID')
    group_name: str | None = Field(default=None, description='群名称')
    group_finger_memo: str | None = Field(default=None, description='群简介')
    group_class_text: str | None = Field(default=None, description='群分类')
    group_tags: list[str] = Field(default_factory=list, description='群标签')
    group_member_num: int | None = Field(default=None, description='群成员人数')


class GroupBotState(QQModel):
    """机器人群内状态（字段随平台更新，未建模字段可通过 extra 获取）。"""


class GroupMember(QQModel):
    """群成员对象。"""

    member_openid: str = Field(description='成员 OpenID')
    username: str | None = Field(default=None, description='用户昵称')
    member_role: str | None = Field(default=None, description='member / owner / admin')
    bot: bool | None = Field(default=None, description='是否机器人')
    joined_at: str | None = Field(default=None, description='入群时间（RFC3339）')
    union_openid: str | None = Field(default=None, description='跨应用统一标识')


class GroupMemberPage(QQModel):
    """群成员分页数据。"""

    members: list[GroupMember] = Field(default_factory=list[GroupMember], description='成员列表，每次最多 30 条')
    next_cursor: str | None = Field(default=None, description='下一页游标，空串表示已到末页')


class ReviewQA(QQModel):
    """入群验证问答。"""

    question: str | None = Field(default=None, description='管理员设置的问题')
    answer: str | None = Field(default=None, description='申请人填写的答案')


class JoinRequestVerifyInfo(QQModel):
    """入群验证方式。"""

    method: str | None = Field(default=None, description='verify_message / admin_review_qa')
    verify_message: str | None = Field(default=None, description='验证消息内容')
    review_qa_list: list[ReviewQA] = Field(default_factory=list[ReviewQA], description='问答列表')


class JoinRequest(QQModel):
    """入群申请对象。"""

    join_request_id: str = Field(description='申请 ID，审批时回传')
    risk_tips: str | None = Field(default=None, description='安全提示语')
    union_openid: str | None = Field(default=None, description='跨应用统一标识')
    member_openid: str | None = Field(default=None, description='申请人 openid')
    username: str | None = Field(default=None, description='申请人昵称')
    apply_at: str | None = Field(default=None, description='申请时间（RFC3339）')
    apply_source: str | None = Field(default=None, description='self_apply / invited')
    invited_by: str | None = Field(default=None, description='邀请人 openid')
    bot: bool | None = Field(default=None, description='是否机器人账号')
    verify_info: JoinRequestVerifyInfo | None = Field(default=None, description='入群验证信息')


class JoinRequestPage(QQModel):
    """入群申请分页数据。"""

    items: list[JoinRequest] = Field(default_factory=list[JoinRequest], alias='list', description='入群申请列表')
    next_cursor: str | None = Field(default=None, description='下一页游标')


class SetMemberMuteState(QQModel):
    """单个群成员的禁言操作。"""

    op: Literal['add', 'update', 'del'] = Field(description='add 增加 / update 更新 / del 解除')
    member_openid: str = Field(description='被禁言成员 openid')
    mute_expire_at: str | None = Field(default=None, description='禁言到期时间（RFC3339）')


class RestrictChatSetting(QQModel):
    """群禁言状态（字段随平台更新，未建模字段可通过 extra 获取）。"""

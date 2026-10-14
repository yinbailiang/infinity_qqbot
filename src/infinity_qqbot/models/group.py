"""群聊对象：群信息、群成员、入群申请、黑名单、自动审批策略、禁言。"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import QQModel

__all__ = [
    'BlacklistUser',
    'GroupBlacklistPage',
    'GroupBlacklistResult',
    'GroupBotState',
    'GroupInfo',
    'GroupMember',
    'GroupMemberPage',
    'JoinApprovalGroupAction',
    'JoinApprovalStrategy',
    'JoinApprovalStrategyCreated',
    'JoinApprovalStrategyPage',
    'JoinApprovalStrategyUpdated',
    'JoinApprovalWhitelistResult',
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


class BlacklistUser(QQModel):
    """群黑名单用户。"""

    union_openid: str | None = Field(default=None, description='跨应用统一标识（如有）')
    member_openid: str | None = Field(default=None, description='用户 openid')
    username: str | None = Field(default=None, description='用户昵称')
    banned_at: str | None = Field(default=None, description='拉黑时间（RFC3339）')
    bot: bool | None = Field(default=None, description='是否机器人账号')


class GroupBlacklistPage(QQModel):
    """群黑名单分页数据。"""

    users: list[BlacklistUser] = Field(default_factory=list[BlacklistUser], description='黑名单用户列表')
    next_cursor: str | None = Field(default=None, description='下一页游标，空串表示已到末页')


class GroupBlacklistResult(QQModel):
    """群黑名单操作结果。"""

    fail_openids: list[str] = Field(default_factory=list[str], description='操作失败的 openid 列表')


class JoinApprovalGroupAction(QQModel):
    """入群自动审批策略的关联群增删操作。"""

    op: Literal['add', 'del'] = Field(description='add 新增关联群 / del 删除关联群')
    group_openids: list[str] | None = Field(default=None, description='群 openid 列表（与 group_ids 互斥）')
    group_ids: list[str | int] | None = Field(default=None, description='QQ 群号列表（与 group_openids 互斥）')


class JoinApprovalStrategy(QQModel):
    """入群自动审批策略。"""

    strategy_id: str = Field(description='策略 ID')
    group_openids: list[str] = Field(default_factory=list[str], description='关联群 openid 列表')
    group_ids: list[str | int] = Field(default_factory=list[str | int], description='关联 QQ 群号列表')
    whitelist_user_count: int | None = Field(default=None, description='白名单号码数量（估算）')
    is_enable: str | None = Field(default=None, description='on 启用 / off 关闭')
    expire_at: str | None = Field(default=None, description='过期时间（RFC3339）')
    created_at: str | None = Field(default=None, description='创建时间（RFC3339）')
    updated_at: str | None = Field(default=None, description='最近更新时间（RFC3339）')
    remark: str | None = Field(default=None, description='策略备注')


class JoinApprovalStrategyPage(QQModel):
    """入群自动审批策略分页数据。"""

    strategies: list[JoinApprovalStrategy] = Field(
        default_factory=list[JoinApprovalStrategy], description='生效中的策略列表'
    )
    next_cursor: str | None = Field(default=None, description='下一页游标，空串表示已到末页')


class JoinApprovalStrategyCreated(QQModel):
    """创建入群自动审批策略响应。"""

    strategy_id: str = Field(description='策略 ID')
    is_enable: str | None = Field(default=None, description='on 启用 / off 关闭')
    expire_at: str | None = Field(default=None, description='过期时间（RFC3339）')


class JoinApprovalStrategyUpdated(QQModel):
    """修改入群自动审批策略响应。"""

    is_enable: str | None = Field(default=None, description='on 启用 / off 关闭')
    expire_at: str | None = Field(default=None, description='过期时间（RFC3339）')


class JoinApprovalWhitelistResult(QQModel):
    """修改白名单号码响应。"""

    strategy_id: str | None = Field(default=None, description='策略 ID')
    whitelist_user_count: int | None = Field(default=None, description='操作后白名单号码数（估算）')
    updated_at: str | None = Field(default=None, description='策略更新时间（RFC3339）')

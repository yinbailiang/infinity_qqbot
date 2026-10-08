"""互动对象：互动数据、解析结果、授权数据。"""

from __future__ import annotations

from pydantic import Field

from .base import QQModel

__all__ = [
    'AuthorizeData',
    'InteractionData',
    'InteractionMessageScene',
    'InteractionResolved',
]


class AuthorizeData(QQModel):
    """授权数据（仅 type=18/19 用户/群授权事件）。"""

    opt_scene: str | None = Field(default=None, description='setting=资料页设置 / dialog=弹窗授权')
    scope: str | None = Field(default=None, description='c2c_push / group_push')


class InteractionMessageScene(QQModel):
    """互动消息场景信息。"""

    ext: list[str] = Field(default_factory=list, description='扩展键值对列表')


class InteractionResolved(QQModel):
    """解析后的互动数据。"""

    button_data: str | None = Field(default=None, description='按钮 data 字段值')
    button_id: str | None = Field(default=None, description='按钮 id 字段值')
    user_id: str | None = Field(default=None, description='操作用户 ID（仅频道）')
    feature_id: str | None = Field(default=None, description='功能 ID（仅快捷菜单）')
    message_id: str | None = Field(default=None, description='操作的消息 ID')
    feedback_opt: str | None = Field(default=None, description='LIKE / UNLIKE（仅消息反馈）')
    checked: int | None = Field(default=None, description='反馈选项是否选中')
    action: str | None = Field(default=None, description='操作类型（故事集 / 切换模型）')
    message_scene: InteractionMessageScene | None = Field(default=None, description='消息场景（仅消息反馈）')
    authorize_data: AuthorizeData | None = Field(default=None, description='授权数据')


class InteractionData(QQModel):
    """互动数据体。"""

    type: int | None = Field(default=None, description='互动数据类型')
    resolved: InteractionResolved | None = Field(default=None, description='解析后的互动数据')

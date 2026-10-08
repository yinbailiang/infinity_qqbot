"""菜单与指令面板对象。"""

from __future__ import annotations

from pydantic import Field

from .base import QQModel

__all__ = [
    'Menu',
    'MenuItem',
    'MenuResponse',
    'MenuSwitch',
    'MenuVersion',
    'Panel',
    'PanelCreated',
    'PanelInfo',
    'PanelItem',
    'PanelList',
    'SubMenuItem',
]


class MenuSwitch(QQModel):
    """菜单开关配置。"""

    switch_id: str | None = Field(default=None, description='开关唯一标识')
    default: bool | None = Field(default=None, description='初始状态')


class SubMenuItem(QQModel):
    """二级菜单项。"""

    name: str | None = Field(default=None, description='按钮名称')
    type: str | None = Field(default=None, description='send_message / link')
    send_message: str | None = Field(default=None, description='发送的内容')
    link: str | None = Field(default=None, description='跳转链接')


class MenuItem(QQModel):
    """一级菜单项。"""

    name: str | None = Field(default=None, description='按钮名称')
    type: str | None = Field(default=None, description='switch / send_message / link / menu')
    sub_menu_items: list[SubMenuItem] | None = Field(default=None, description='子菜单列表')
    send_message: str | None = Field(default=None, description='发送的内容')
    link: str | None = Field(default=None, description='跳转链接')
    switch: MenuSwitch | None = Field(default=None, description='开关配置')


class Menu(QQModel):
    """自定义菜单配置。"""

    items: list[MenuItem] = Field(default_factory=list[MenuItem], description='菜单项列表，最多 10 个')


class MenuVersion(QQModel):
    """菜单版本信息。"""

    version: int | None = Field(default=None, description='菜单版本号')


class MenuResponse(QQModel):
    """查询全局自定义菜单响应。"""

    menu: Menu | None = Field(default=None, description='菜单配置')
    version: int | None = Field(default=None, description='菜单版本号')


class PanelItem(QQModel):
    """指令面板元素。"""

    name: str | None = Field(default=None, description='元素名称')
    desc: str | None = Field(default=None, description='元素描述')
    type: str | None = Field(default=None, description='command / link')
    only_admin: bool | None = Field(default=None, description='是否仅管理员可操作')
    link: str | None = Field(default=None, description='跳转链接')


class Panel(QQModel):
    """指令面板配置。"""

    items: list[PanelItem] = Field(default_factory=list[PanelItem], description='面板元素列表，最多 20 个')
    remark: str | None = Field(default=None, description='面板备注')
    version: int | None = Field(default=None, description='当前版本号')


class PanelInfo(Panel):
    """指令面板详情（含关联信息）。"""

    panel_id: str | None = Field(default=None, description='面板 ID')
    scope: str | None = Field(default=None, description='c2c / group / channel / dm')
    target_type: str | None = Field(default=None, description='all / specific')
    user_openids: list[str] | None = Field(default=None, description='关联用户列表')
    group_openids: list[str] | None = Field(default=None, description='关联群列表')


class PanelCreated(QQModel):
    """创建指令面板响应。"""

    panel_id: str = Field(description='新创建的面板 ID')


class PanelList(QQModel):
    """指令面板列表响应（字段随平台更新）。"""

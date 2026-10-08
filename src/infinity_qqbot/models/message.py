"""消息对象：频道消息、附件、场景、ARK、键盘、Markdown 等消息组件。"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .base import QQModel
from .common import GuildMember, User

__all__ = [
    'ARKData',
    'Action',
    'Button',
    'InputNotify',
    'Keyboard',
    'KeyboardContent',
    'MediaInfo',
    'Message',
    'MessageAttachment',
    'MessageExtInfo',
    'MessageMarkdown',
    'MessageMarkdownParam',
    'MessageReference',
    'MessageScene',
    'Modal',
    'MsgElement',
    'Permission',
    'RenderData',
    'Row',
]


class MessageAttachment(QQModel):
    """消息附件对象。"""

    url: str | None = Field(default=None, description='附件下载 URL')
    filename: str | None = Field(default=None, description='文件名')
    width: int | None = Field(default=None, description='图片宽度（像素）')
    height: int | None = Field(default=None, description='图片高度（像素）')
    size: int | None = Field(default=None, description='文件大小（字节）')
    content_type: str | None = Field(default=None, description='MIME 类型或 voice/file 标记')
    voice_wav_url: str | None = Field(default=None, description='语音转 WAV 文件 URL')
    asr_refer_text: str | None = Field(default=None, description='语音 ASR 参考结果')


class MessageScene(QQModel):
    """消息场景上下文。"""

    source: str | None = Field(default=None, description='场景来源')
    ext: list[str] = Field(default_factory=list, description='扩展键值对列表')


class ARKData(QQModel):
    """结构化卡片（ARK）消息数据。"""

    prompt: str | None = Field(default=None, description='用户操作提示文本')
    ark_type: str | None = Field(default=None, description='卡片类型标识')
    ark_name: str | None = Field(default=None, description='卡片类型中文名')
    fields: dict[str, Any] = Field(default_factory=dict, description='卡片字段')


class MsgElement(QQModel):
    """消息元素（引用消息等场景的嵌套结构）。"""

    msg_idx: str | None = Field(default=None, description='消息索引')
    author: User | None = Field(default=None, description='该元素消息发送者')
    message_type: int | None = Field(default=None, description='元素消息类型')
    content: str | None = Field(default=None, description='元素正文')
    attachments: list[MessageAttachment] = Field(default_factory=list[MessageAttachment], description='元素附件')
    ark_data: ARKData | None = Field(default=None, description='元素卡片数据')
    msg_elements: list[Any] = Field(default_factory=list, description='嵌套消息元素（递归结构）')


class MessageReference(QQModel):
    """引用消息对象。"""

    message_id: str | None = Field(default=None, description='被引用消息 ID')
    ignore_get_message_error: bool | None = Field(default=None, description='是否忽略拉取引用消息失败')


class MessageMarkdownParam(QQModel):
    """Markdown 模板参数。"""

    key: str = Field(description='参数名')
    values: list[str] = Field(description='参数值')


class MessageMarkdown(QQModel):
    """Markdown 消息对象。"""

    template_id: int | None = Field(default=None, description='平台模板 ID（已废弃）')
    content: str | None = Field(default=None, description='Markdown 内容')
    custom_template_id: str | None = Field(default=None, description='自定义模板 ID（已废弃）')
    params: list[MessageMarkdownParam] | None = Field(default=None, description='模板参数')


class MediaInfo(QQModel):
    """富媒体消息对象。"""

    file_info: str = Field(description='文件数据，来自文件上传接口返回值')


class InputNotify(QQModel):
    """输入中状态通知。"""

    input_type: int = Field(default=1, description='填 1')
    input_second: int = Field(description='状态持续时间，最长 60s')


class MessageExtInfo(QQModel):
    """消息扩展信息。"""

    ref_idx: str | None = Field(default=None, description='引用消息索引')


class RenderData(QQModel):
    """按钮渲染数据。"""

    label: str = Field(description='按钮文字，最多 10 字符')
    visited_label: str | None = Field(default=None, description='点击后文字')
    style: int | None = Field(default=None, description='0 灰色线框 / 1 蓝色线框 / 3 白底红字 / 4 蓝底白字')


class Permission(QQModel):
    """按钮操作权限。"""

    type: int = Field(description='0 指定用户 / 1 管理员 / 2 所有人')
    specify_user_ids: list[str] | None = Field(default=None, description='有权限的用户 ID 列表')
    specify_role_ids: list[str] | None = Field(default=None, description='有权限的身份组 ID 列表（仅频道）')


class Modal(QQModel):
    """用户点击二次确认。"""

    content: str = Field(description='二次确认提示文本，最多 40 字符，不能有 URL')
    confirm_text: str | None = Field(default=None, description='确认按钮文字，最多 4 字符')
    cancel_text: str | None = Field(default=None, description='取消按钮文字，最多 4 字符')


class Action(QQModel):
    """按钮点击行为。"""

    type: int = Field(description='0 跳转 / 1 回调 / 2 指令')
    permission: Permission | None = Field(default=None, description='操作权限')
    data: str | None = Field(default=None, description='回调数据')
    click_limit: int | None = Field(default=None, description='可点击次数限制（已废弃）')
    unsupport_tips: str | None = Field(default=None, description='版本过低提示文案')
    enter: bool | None = Field(default=None, description='指令按钮是否点击后直接发送')
    reply: bool | None = Field(default=None, description='指令是否带引用回复')
    anchor: int | None = Field(default=None, description='指令按钮特殊唤起配置')
    modal: Modal | None = Field(default=None, description='二次确认配置')


class Button(QQModel):
    """内嵌键盘按钮。"""

    id: str | None = Field(default=None, description='按钮 ID，同一键盘内唯一')
    render_data: RenderData | None = Field(default=None, description='按钮渲染')
    action: Action | None = Field(default=None, description='按钮点击行为')
    group_id: str | None = Field(default=None, description='分组 ID')


class Row(QQModel):
    """键盘按钮行。"""

    buttons: list[Button] = Field(default_factory=list[Button], description='行内按钮')


class KeyboardContent(QQModel):
    """自定义键盘布局。"""

    rows: list[Row] = Field(default_factory=list[Row], description='按钮行列表')


class Keyboard(QQModel):
    """内嵌键盘。"""

    id: str | None = Field(default=None, description='平台预设键盘模板 ID')
    content: KeyboardContent | None = Field(default=None, description='自定义键盘布局')


class Message(QQModel):
    """频道（子频道）消息对象。"""

    id: str = Field(description='消息 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    guild_id: str | None = Field(default=None, description='频道 ID')
    content: str | None = Field(default=None, description='消息内容')
    timestamp: str | None = Field(default=None, description='发送时间')
    edited_timestamp: str | None = Field(default=None, description='编辑时间')
    mention_everyone: bool | None = Field(default=None, description='是否 @全体')
    mentions: list[User] = Field(default_factory=list[User], description='@用户列表')
    member: GuildMember | None = Field(default=None, description='发送者成员信息')
    attachments: list[MessageAttachment] = Field(default_factory=list[MessageAttachment], description='附件列表')
    embeds: list[Any] = Field(default_factory=list, description='embed 列表')
    ark: Any = Field(default=None, description='ark 消息')
    reference: MessageReference | None = Field(default=None, description='引用消息')
    type: int | None = Field(default=None, description='消息类型')
    flags: int | None = Field(default=None, description='消息标志位')
    pinned: bool | None = Field(default=None, description='是否精华消息')
    seq: int | None = Field(default=None, description='消息序列号')
    seq_in_channel: str | None = Field(default=None, description='子频道内消息序列号')

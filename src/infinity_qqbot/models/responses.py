"""OpenAPI 响应对象：凭证、网关、消息回执、上传、权限、公告、表情、日程。"""

from __future__ import annotations

from pydantic import Field

from .base import QQModel
from .common import User
from .message import MessageExtInfo

__all__ = [
    'AccessTokenResponse',
    'Announce',
    'ApiPermission',
    'ApiPermissionDemand',
    'ApiPermissionList',
    'BotInfo',
    'FileUploadResponse',
    'Gateway',
    'GatewayBot',
    'MessageResponse',
    'ReactionEmoji',
    'ReactionTarget',
    'ReactionUsers',
    'RecommendChannel',
    'Schedule',
    'SessionStartLimit',
    'StreamMessageResponse',
    'UploadConfig',
    'UploadPart',
    'UploadPrepareResponse',
]


class AccessTokenResponse(QQModel):
    """``getAppAccessToken`` 成功响应。"""

    access_token: str = Field(description='获取到的凭证')
    expires_in: int = Field(description='凭证有效时间（秒）')


class Gateway(QQModel):
    """通用 WSS 接入点响应。"""

    url: str = Field(description='WSS 接入点地址')


class SessionStartLimit(QQModel):
    """网关连接数限制信息。"""

    total: int | None = Field(default=None, description='每日总连接数')
    remaining: int | None = Field(default=None, description='剩余连接数')
    reset_after: int | None = Field(default=None, description='重置剩余时间（毫秒）')
    max_concurrency: int | None = Field(default=None, description='最大并发连接数')


class GatewayBot(Gateway):
    """带分片的 WSS 接入点响应。"""

    shards: int | None = Field(default=None, description='建议分片数')
    session_start_limit: SessionStartLimit | None = Field(default=None, description='连接限制信息')


class BotInfo(QQModel):
    """机器人详情。"""

    id: str | None = Field(default=None, description='机器人 ID')
    username: str | None = Field(default=None, description='机器人名称')
    avatar: str | None = Field(default=None, description='机器人头像')


class MessageResponse(QQModel):
    """发送消息响应。"""

    id: str = Field(description='消息 ID，可用于后续撤回')
    timestamp: str | None = Field(default=None, description='发送时间（RFC3339 东八区）')
    ext_info: MessageExtInfo | None = Field(default=None, description='扩展信息')


class StreamMessageResponse(MessageResponse):
    """流式发送单聊消息响应。"""

    remain_msg_len: int | None = Field(default=None, description='流式消息剩余长度（字符数）')


class FileUploadResponse(QQModel):
    """富媒体上传响应。"""

    file_uuid: str | None = Field(default=None, description='文件唯一 ID')
    file_info: str | None = Field(default=None, description='用于发消息 media.file_info 字段')
    ttl: int | None = Field(default=None, description='file_info 有效期（秒），0 表示长期有效')
    id: str | None = Field(default=None, description='消息 ID（仅 srv_send_msg=true）')
    raw_url: str | None = Field(default=None, description='文件下载链接（分片合并且图片/视频/语音时返回）')


class UploadPart(QQModel):
    """分片上传的单个分片。"""

    index: int = Field(description='分片序号，从 0 开始')
    presigned_url: str = Field(description='预签名上传 URL')
    block_size: str | None = Field(default=None, description='该分块大小（字节）')


class UploadConfig(QQModel):
    """上传配置。"""

    concurrency: int | None = Field(default=None, description='上传并发数')
    retry_timeout: int | None = Field(default=None, description='重试超时时间（秒）')
    retry_delay: int | None = Field(default=None, description='重试延迟（秒）')


class UploadPrepareResponse(QQModel):
    """预上传响应。"""

    upload_id: str = Field(description='上传任务 ID')
    block_size: str | None = Field(default=None, description='分块大小（字节），默认 5MB')
    parts: list[UploadPart] = Field(default_factory=list[UploadPart], description='分片列表')
    upload_config: UploadConfig | None = Field(default=None, description='上传配置')


class ApiPermission(QQModel):
    """频道 API 接口权限。"""

    path: str | None = Field(default=None, description='接口路径')
    method: str | None = Field(default=None, description='请求方法')
    desc: str | None = Field(default=None, description='接口描述')
    auth_status: int | None = Field(default=None, description='授权状态')


class ApiPermissionList(QQModel):
    """频道 API 接口权限列表。"""

    api_list: list[ApiPermission] = Field(default_factory=list[ApiPermission], description='权限列表')


class ApiPermissionDemand(QQModel):
    """API 接口权限授权链接。"""

    url: str | None = Field(default=None, description='授权链接')
    demand_id: str | None = Field(default=None, description='申请单 ID')


class RecommendChannel(QQModel):
    """推荐子频道。"""

    channel_id: str | None = Field(default=None, description='子频道 ID')
    introduce: str | None = Field(default=None, description='推荐语')


class Announce(QQModel):
    """频道公告对象。"""

    guild_id: str | None = Field(default=None, description='频道 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID（子频道公告）')
    message_id: str | None = Field(default=None, description='消息 ID')
    announces_type: int | None = Field(default=None, description='公告类型')
    recommend_channels: list[RecommendChannel] = Field(
        default_factory=list[RecommendChannel], description='推荐子频道列表'
    )


class ReactionEmoji(QQModel):
    """表情表态的表情对象。"""

    id: str | None = Field(default=None, description='表情 ID')
    type: int | None = Field(default=None, description='表情类型')


class ReactionTarget(QQModel):
    """表情表态的目标对象。"""

    id: str | None = Field(default=None, description='目标消息 ID')
    type: int | None = Field(default=None, description='目标类型')


class ReactionUsers(QQModel):
    """表情表态用户列表。"""

    users: list[User] = Field(default_factory=list[User], description='用户列表')
    is_end: bool | None = Field(default=None, description='是否已到末尾')


class Schedule(QQModel):
    """日程对象。"""

    id: str | None = Field(default=None, description='日程 ID')
    name: str | None = Field(default=None, description='日程名称')
    description: str | None = Field(default=None, description='日程描述')
    start_timestamp: str | None = Field(default=None, description='开始时间戳（毫秒字符串）')
    end_timestamp: str | None = Field(default=None, description='结束时间戳（毫秒字符串）')
    creator: User | None = Field(default=None, description='创建者')
    jump_channel_id: str | None = Field(default=None, description='跳转子频道 ID')
    remind_type: str | None = Field(default=None, description='提醒类型')

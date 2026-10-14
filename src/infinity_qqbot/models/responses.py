"""OpenAPI 响应对象：凭证、网关、消息回执、上传、权限、公告、表情、日程、频道与论坛。"""

from __future__ import annotations

from pydantic import Field

from .base import QQModel
from .common import GuildMember, User
from .message import MessageExtInfo

__all__ = [
    'AccessTokenResponse',
    'Announce',
    'ApiPermission',
    'ApiPermissionDemand',
    'ApiPermissionList',
    'AudioControl',
    'BotInfo',
    'ChannelRolePermissions',
    'ChannelUserPermissions',
    'FileUploadResponse',
    'ForumThread',
    'Gateway',
    'GatewayBot',
    'MessageResponse',
    'MessageSetting',
    'MuteUsersResult',
    'OnlineNums',
    'ReactionEmoji',
    'ReactionTarget',
    'ReactionUsers',
    'RecommendChannel',
    'RoleMemberPage',
    'Schedule',
    'SessionStartLimit',
    'StreamMessageResponse',
    'ThreadCreateResult',
    'ThreadDetail',
    'ThreadInfo',
    'ThreadList',
    'UploadConfig',
    'UploadPart',
    'UploadPrepareResponse',
    'UrlLinkData',
    'UrlLinkResponse',
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


class ChannelUserPermissions(QQModel):
    """子频道用户权限（``GET /channels/{channel_id}/members/{user_id}/permissions``）。"""

    channel_id: str | None = Field(default=None, description='子频道 ID')
    user_id: str | None = Field(default=None, description='用户 ID')
    permissions: str | None = Field(default=None, description='字符串形式的权限位图')


class ChannelRolePermissions(QQModel):
    """子频道身份组权限（``GET /channels/{channel_id}/roles/{role_id}/permissions``）。"""

    channel_id: str | None = Field(default=None, description='子频道 ID')
    role_id: str | None = Field(default=None, description='身份组 ID')
    permissions: str | None = Field(default=None, description='字符串形式的权限位图')


class OnlineNums(QQModel):
    """子频道在线成员数（``GET /channels/{channel_id}/online_nums``）。"""

    online_nums: int | None = Field(default=None, description='在线成员数')


class RoleMemberPage(QQModel):
    """身份组成员分页数据（``GET /guilds/{guild_id}/roles/{role_id}/members``）。"""

    data: list[GuildMember] = Field(default_factory=list[GuildMember], description='成员列表')
    next: str | None = Field(default=None, description='下一次请求的分页标识（start_index）')


class MuteUsersResult(QQModel):
    """批量禁言结果（``PATCH /guilds/{guild_id}/mute``）。"""

    user_ids: list[str] = Field(default_factory=list[str], description='设置成功的成员 user_id 列表')


class MessageSetting(QQModel):
    """频道消息频率设置（``GET /guilds/{guild_id}/message/setting``）。"""

    disable_create_dm: bool | None = Field(default=None, description='是否禁用创建私信')
    disable_push_msg: bool | None = Field(default=None, description='是否禁用推送消息')
    channel_ids: list[str] = Field(default_factory=list[str], description='设置过的子频道 ID 列表')
    channel_push_max_num: int | None = Field(default=None, description='子频道推送上限')


class AudioControl(QQModel):
    """音频控制请求体（``POST /channels/{channel_id}/audio``）。"""

    audio_url: str | None = Field(default=None, description='音频数据 URL（status=0 时传）')
    text: str | None = Field(default=None, description='状态文本（status=0 时传）')
    status: int = Field(description='0 开始 / 1 暂停 / 2 继续 / 3 停止，见 AudioStatus')


class ThreadInfo(QQModel):
    """帖子内容信息（论坛）。"""

    thread_id: str | None = Field(default=None, description='帖子 ID')
    title: str | None = Field(default=None, description='帖子标题')
    content: str | None = Field(default=None, description='帖子内容（RichText 结构）')
    date_time: str | None = Field(default=None, description='发帖时间（RFC3339）')


class ForumThread(QQModel):
    """论坛帖子对象（``GET /channels/{channel_id}/threads``）。"""

    guild_id: str | None = Field(default=None, description='频道 ID')
    channel_id: str | None = Field(default=None, description='子频道 ID')
    author_id: str | None = Field(default=None, description='作者 ID')
    thread_info: ThreadInfo | None = Field(default=None, description='帖子内容信息')


class ThreadList(QQModel):
    """帖子列表（``GET /channels/{channel_id}/threads``）。"""

    threads: list[ForumThread] = Field(default_factory=list[ForumThread], description='帖子列表')
    is_finish: int | None = Field(default=None, description='是否拉取完毕（0 否 / 1 是）')


class ThreadDetail(QQModel):
    """帖子详情（``GET /channels/{channel_id}/threads/{thread_id}``）。"""

    thread: ForumThread | None = Field(default=None, description='帖子详情对象')


class ThreadCreateResult(QQModel):
    """发表帖子响应（``PUT /channels/{channel_id}/threads``）。"""

    task_id: str | None = Field(default=None, description='帖子任务 ID')
    create_time: str | None = Field(default=None, description='发帖时间戳（秒）')


class UrlLinkData(QQModel):
    """分享链接数据。"""

    url: str | None = Field(default=None, description='生成的分享链接')


class UrlLinkResponse(QQModel):
    """生成分享链接响应（``POST /v2/generate_url_link``）。"""

    data: UrlLinkData | None = Field(default=None, description='分享链接数据')
    creator: User | None = Field(default=None, description='创建者')
    jump_channel_id: str | None = Field(default=None, description='跳转子频道 ID')
    remind_type: str | None = Field(default=None, description='提醒类型')

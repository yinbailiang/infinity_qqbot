"""RPC 代码生成器：从方法规格生成「纯显式」的请求/响应模型、事件声明、客户端与处理器。

生成目标（全部为平铺的显式代码，运行期零元编程）：

- ``src/infinity_qqbot/rpc/{messages,groups,channels,interactions}.py``
  每个方法生成：``XxxRequest``、``XxxResponse``、``XxxRequestEvent``、
  ``XxxResponseEvent``、强类型客户端函数 ``xxx(...)``；
- ``src/infinity_qqbot/rpc/handlers/*.py``
  每个方法生成一个 ``@process(请求事件, 响应事件)`` 处理器方法，
  内部以显式关键字调用 ``QQBotAPI``。

用法::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RPC_DIR = ROOT / 'src' / 'infinity_qqbot' / 'rpc'


@dataclass(frozen=True)
class Method:
    """单个 API 方法的 RPC 规格。"""

    name: str
    label: str
    result: str
    fields: tuple[tuple[str, str], ...] = ()
    extra: bool = False
    passthrough: bool = False


def M(
    name: str,
    label: str,
    result: str,
    /,
    *fields: str,
    extra: bool = False,
    passthrough: bool = False,
) -> Method:
    """紧凑声明一个方法规格：``M('send', '发送', 'MessageResponse', 'user_openid: str', ...)``。"""
    parsed: list[tuple[str, str]] = []
    for field_spec in fields:
        fname, _, annotation = field_spec.partition(': ')
        parsed.append((fname, annotation))
    return Method(name, label, result, tuple(parsed), extra, passthrough)


# ======================================================================
# 方法规格（字段名与 QQBotAPI 方法关键字参数一一对应）
# ======================================================================

QQ_MESSAGE_FIELDS = (
    'content: str | None = None',
    'msg_type: int | None = None',
    'markdown: MessageMarkdown | None = None',
    'keyboard: Keyboard | None = None',
    'msg_id: str | None = None',
    'event_id: str | None = None',
    'msg_seq: int | None = None',
    'media: MediaInfo | None = None',
    'message_reference: MessageReference | None = None',
    'is_wakeup: bool | None = None',
    'input_notify: InputNotify | None = None',
)

FILE_FIELDS = (
    'file_type: int',
    'url: str | None = None',
    'file_name: str | None = None',
    'srv_send_msg: bool | None = None',
    'upload_id: str | None = None',
)

PREPARE_FIELDS = (
    'file_type: int',
    'file_size: int | str',
    'file_name: str',
    'md5: str',
    'sha1: str',
    'md5_10m: str',
)

CHANNEL_MESSAGE_FIELDS = (
    'content: str | None = None',
    'embed: dict[str, Any] | None = None',
    'ark: dict[str, Any] | None = None',
    'image: str | None = None',
    'msg_id: str | None = None',
    'event_id: str | None = None',
    'markdown: MessageMarkdown | None = None',
    'message_reference: MessageReference | None = None',
)

MUTE_FIELDS = (
    'mute_seconds: str | None = None',
    'mute_end_timestamp: str | None = None',
)

MESSAGES: tuple[Method, ...] = (
    M('send_c2c_message', '发送单聊消息', 'MessageResponse', 'user_openid: str', *QQ_MESSAGE_FIELDS),
    M(
        'send_c2c_stream_message',
        '流式发送单聊消息',
        'StreamMessageResponse',
        'user_openid: str',
        'input_state: int',
        'index: int',
        'content_raw: str | None = None',
        'input_mode: str | None = None',
        'content_type: str | None = None',
        'msg_id: str | None = None',
        'event_id: str | None = None',
        'stream_msg_id: str | None = None',
        'msg_seq: int | None = None',
        'is_wakeup: bool | None = None',
    ),
    M('recall_c2c_message', '撤回单聊消息', 'None', 'user_openid: str', 'message_id: str'),
    M('upload_c2c_file', '单聊富媒体上传', 'FileUploadResponse', 'user_openid: str', *FILE_FIELDS),
    M('c2c_upload_prepare', '单聊富媒体预上传', 'UploadPrepareResponse', 'user_openid: str', *PREPARE_FIELDS),
    M(
        'c2c_upload_part_finish',
        '单聊分片上传完成',
        'None',
        'user_openid: str',
        'upload_id: str | None = None',
        'index: int | None = None',
        passthrough=True,
    ),
    M('send_group_message', '发送群聊消息', 'MessageResponse', 'group_openid: str', *QQ_MESSAGE_FIELDS),
    M('recall_group_message', '撤回群聊消息', 'None', 'group_openid: str', 'message_id: str'),
    M('upload_group_file', '群聊富媒体上传', 'FileUploadResponse', 'group_openid: str', *FILE_FIELDS),
    M('group_upload_prepare', '群聊富媒体预上传', 'UploadPrepareResponse', 'group_openid: str', *PREPARE_FIELDS),
    M(
        'group_upload_part_finish',
        '群聊分片上传完成',
        'None',
        'group_openid: str',
        'upload_id: str | None = None',
        'index: int | None = None',
        passthrough=True,
    ),
)

GROUPS: tuple[Method, ...] = (
    M('get_group_info', '获取群基本信息', 'GroupInfo', 'group_openid: str'),
    M('get_group_bot_state', '获取机器人群内状态', 'GroupBotState', 'group_openid: str'),
    M('get_group_members', '获取群成员列表', 'GroupMemberPage', 'group_openid: str', 'cursor: str | None = None'),
    M('get_group_member', '获取群成员信息', 'GroupMember', 'group_openid: str', 'member_openid: str'),
    M(
        'batch_remove_group_members',
        '群成员批量移除',
        'None',
        'group_openid: str',
        'members: list[str]',
        extra=True,
    ),
    M(
        'get_join_request_list',
        '拉取入群申请列表',
        'JoinRequestPage',
        'group_openid: str',
        'cursor: str | None = None',
        'limit: int | None = None',
    ),
    M(
        'approval_join_request',
        '入群申请审批',
        'None',
        'group_openid: str',
        'member_openid: str',
        'join_request_id: str | None = None',
        'approve: bool | None = None',
        'reason: str | None = None',
        extra=True,
    ),
    M('get_join_approval_strategies', '查询入群自动审批策略列表', 'dict[str, Any]', passthrough=True),
    M('create_join_approval_strategy', '创建入群自动审批策略', 'dict[str, Any]', passthrough=True),
    M(
        'update_join_approval_strategy',
        '修改入群自动审批策略',
        'dict[str, Any]',
        'strategy_id: str',
        passthrough=True,
    ),
    M('delete_join_approval_strategy', '删除入群自动审批策略', 'None', 'strategy_id: str'),
    M(
        'execute_join_approval_strategy',
        '执行入群自动审批策略',
        'dict[str, Any]',
        'strategy_id: str',
        passthrough=True,
    ),
    M(
        'update_join_approval_whitelist',
        '修改入群自动审批策略白名单',
        'dict[str, Any]',
        'strategy_id: str',
        passthrough=True,
    ),
    M('get_group_blacklist', '群黑名单查询', 'dict[str, Any]', 'group_openid: str', passthrough=True),
    M('operate_group_blacklist', '群黑名单操作', 'dict[str, Any]', 'group_openid: str', passthrough=True),
    M('get_group_restrict_chat_setting', '查询群禁言状态', 'RestrictChatSetting', 'group_openid: str'),
    M('set_group_member_mute', '设置群成员禁言', 'None', 'group_openid: str', 'members: list[SetMemberMuteState]'),
)

INTERACTIONS: tuple[Method, ...] = (
    M('get_me', '获取机器人详情', 'BotInfo'),
    M(
        'get_my_guilds',
        '获取机器人频道列表',
        'list[Guild]',
        'before: str | None = None',
        'after: str | None = None',
        'limit: int | None = None',
    ),
    M('generate_url_link', '生成分享链接', 'dict[str, Any]', passthrough=True),
    M(
        'respond_interaction',
        '互动事件响应',
        'None',
        'interaction_id: str',
        'code: int = 0',
        extra=True,
    ),
    M('get_menu', '查询全局自定义菜单', 'MenuResponse'),
    M('put_menu', '修改全局自定义菜单', 'MenuVersion', 'menu: Menu'),
    M('list_panels', '查询指令面板列表', 'PanelList', passthrough=True),
    M(
        'create_panel',
        '创建指令面板',
        'PanelCreated',
        'scope: str',
        'panel: Panel',
        'target_type: str | None = None',
        'user_openids: list[str] | None = None',
        'group_openids: list[str] | None = None',
    ),
    M('get_panel', '查询指令面板详情', 'PanelInfo', 'panel_id: str'),
    M('update_panel', '修改指令面板', 'None', 'panel_id: str', passthrough=True),
    M('delete_panel', '删除指令面板', 'None', 'panel_id: str'),
    M('update_panel_target', '修改指令面板关联对象', 'None', 'panel_id: str', passthrough=True),
)

CHANNELS: tuple[Method, ...] = (
    M('get_guild', '获取频道详情', 'Guild', 'guild_id: str'),
    M('get_guild_channels', '获取子频道列表', 'list[Channel]', 'guild_id: str'),
    M(
        'create_guild_channel',
        '创建子频道',
        'Channel',
        'guild_id: str',
        'name: str',
        'type: int',
        'position: int | None = None',
        'parent_id: str | None = None',
        'sub_type: int | None = None',
        'private_type: int | None = None',
        'private_user_limit: int | None = None',
        extra=True,
    ),
    M('get_channel', '获取子频道详情', 'Channel', 'channel_id: str'),
    M(
        'update_channel',
        '修改子频道',
        'Channel',
        'channel_id: str',
        'name: str | None = None',
        'position: int | None = None',
        'parent_id: str | None = None',
        'private_type: int | None = None',
        extra=True,
    ),
    M('delete_channel', '删除子频道', 'None', 'channel_id: str'),
    M('send_channel_message', '发送子频道消息', 'Message', 'channel_id: str', *CHANNEL_MESSAGE_FIELDS),
    M('get_channel_message', '获取子频道消息', 'Message', 'channel_id: str', 'message_id: str'),
    M(
        'recall_channel_message',
        '撤回子频道消息',
        'None',
        'channel_id: str',
        'message_id: str',
        'hidetip: bool = False',
    ),
    M('create_dm_session', '创建频道私信会话', 'DMS', 'recipient_id: str', 'source_guild_id: str'),
    M('send_dm_message', '发送频道私信', 'Message', 'guild_id: str', *CHANNEL_MESSAGE_FIELDS),
    M('recall_dm_message', '撤回频道私信', 'None', 'guild_id: str', 'message_id: str', 'hidetip: bool = False'),
    M(
        'get_guild_members',
        '获取频道成员列表',
        'list[GuildMember]',
        'guild_id: str',
        'after: str | None = None',
        'limit: int | None = None',
    ),
    M('get_guild_member', '获取频道成员详情', 'GuildMember', 'guild_id: str', 'user_id: str'),
    M(
        'remove_guild_member',
        '移除频道成员',
        'None',
        'guild_id: str',
        'user_id: str',
        'add_blacklist: bool | None = None',
        'delete_history_msg_days: int | None = None',
    ),
    M('get_guild_roles', '获取频道身份组列表', 'list[Role]', 'guild_id: str', 'limit: int | None = None'),
    M(
        'create_guild_role',
        '创建频道身份组',
        'Role',
        'guild_id: str',
        'name: str | None = None',
        'color: int | None = None',
        'hoist: int | None = None',
        'mentionable: int | None = None',
        extra=True,
    ),
    M(
        'update_guild_role',
        '修改频道身份组',
        'Role',
        'guild_id: str',
        'role_id: str',
        'name: str | None = None',
        'color: int | None = None',
        'hoist: int | None = None',
    ),
    M('delete_guild_role', '删除频道身份组', 'None', 'guild_id: str', 'role_id: str'),
    M(
        'add_role_member',
        '添加身份组成员',
        'None',
        'guild_id: str',
        'user_id: str',
        'role_id: str',
        'channel_id: str | None = None',
    ),
    M(
        'remove_role_member',
        '移除身份组成员',
        'None',
        'guild_id: str',
        'user_id: str',
        'role_id: str',
        'channel_id: str | None = None',
    ),
    M('mute_guild', '频道全员禁言', 'None', 'guild_id: str', *MUTE_FIELDS),
    M('mute_guild_member', '指定成员禁言', 'None', 'guild_id: str', 'user_id: str', *MUTE_FIELDS),
    M(
        'create_guild_announce',
        '创建频道公告',
        'Announce',
        'guild_id: str',
        'message_id: str | None = None',
        'channel_id: str | None = None',
        'announces_type: int | None = None',
        'recommend_channels: list[RecommendChannel] | None = None',
    ),
    M('delete_guild_announce', '删除频道公告', 'None', 'guild_id: str', 'message_id: str'),
    M(
        'create_channel_announce',
        '创建子频道公告',
        'Announce',
        'channel_id: str',
        'message_id: str | None = None',
        'announces_type: int | None = None',
    ),
    M('delete_channel_announce', '删除子频道公告', 'None', 'channel_id: str', 'message_id: str'),
    M('get_api_permission', '获取频道可用权限列表', 'ApiPermissionList', 'guild_id: str'),
    M(
        'create_api_permission_demand',
        '创建频道 API 接口权限授权链接',
        'ApiPermissionDemand',
        'guild_id: str',
        'channel_id: str',
        'api_identify: dict[str, Any]',
        'desc: str | None = None',
    ),
    M(
        'add_reaction',
        '添加表情表态',
        'None',
        'channel_id: str',
        'message_id: str',
        'emoji_type: int | str',
        'emoji_id: str',
    ),
    M(
        'delete_reaction',
        '删除表情表态',
        'None',
        'channel_id: str',
        'message_id: str',
        'emoji_type: int | str',
        'emoji_id: str',
    ),
    M(
        'get_reactions',
        '获取表情表态用户列表',
        'ReactionUsers',
        'channel_id: str',
        'message_id: str',
        'emoji_type: int | str',
        'emoji_id: str',
    ),
    M('add_pin', '添加精华消息', 'None', 'channel_id: str', 'message_id: str'),
    M('delete_pin', '删除精华消息', 'None', 'channel_id: str', 'message_id: str'),
    M('get_pins', '获取精华消息列表', 'list[Message]', 'channel_id: str'),
    M('get_schedules', '获取日程列表', 'list[Schedule]', 'channel_id: str', 'since: str | None = None'),
    M('create_schedule', '创建日程', 'Schedule', 'channel_id: str', 'schedule: Schedule'),
    M('get_schedule', '获取日程详情', 'Schedule', 'channel_id: str', 'schedule_id: str'),
    M(
        'update_schedule',
        '修改日程',
        'Schedule',
        'channel_id: str',
        'schedule_id: str',
        'schedule: Schedule',
    ),
    M('delete_schedule', '删除日程', 'None', 'channel_id: str', 'schedule_id: str'),
)

CATEGORIES: dict[str, tuple[Method, ...]] = {
    'messages': MESSAGES,
    'groups': GROUPS,
    'interactions': INTERACTIONS,
    'channels': CHANNELS,
}

MIXIN_NAMES = {
    'messages': 'MessageHandlersMixin',
    'groups': 'GroupHandlersMixin',
    'interactions': 'InteractionHandlersMixin',
    'channels': 'ChannelHandlersMixin',
}

_IDENT_RE = re.compile(r'\b[A-Z][A-Za-z0-9_]*\b')
_BUILTIN_TYPES = {'Any', 'False', 'None', 'True'}


def _type_expr(annotation: str) -> str:
    """去掉默认值，仅保留类型表达式（``str | None = None`` -> ``str | None``）。"""
    return annotation.split(' = ', 1)[0]


def _class_stem(method: Method) -> str:
    """``send_c2c_message`` -> ``SendC2CMessage``（含数字的词整体大写）。"""

    def _cap(part: str) -> str:
        if any(ch.isdigit() for ch in part):
            return part.upper()
        return part[:1].upper() + part[1:]

    return ''.join(_cap(part) for part in method.name.split('_'))


def _collect_model_names(methods: tuple[Method, ...]) -> set[str]:
    """从字段与结果类型表达式中提取需要从 ``..models`` 导入的名字。"""
    names: set[str] = set()
    for method in methods:
        texts = [method.result, *(_type_expr(annotation) for _, annotation in method.fields)]
        for text in texts:
            for name in _IDENT_RE.findall(text):
                if name not in _BUILTIN_TYPES:
                    names.add(name)
    return names


def _render_models_module(category: str, methods: tuple[Method, ...]) -> str:
    model_names = sorted(_collect_model_names(methods))
    uses_config = any(m.extra or m.passthrough for m in methods)

    lines: list[str] = [
        f'"""自动生成：{category} RPC —— 请求 / 响应模型、事件声明与强类型客户端。',
        '',
        '请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::',
        '',
        '    uv run python tools/gen_rpc.py',
        '    uv run ruff check --fix src',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from typing import Any',
        '',
        'from event_bus import EventDeclaration, EventBus',
        'from event_bus.templates import request',
        'from event_bus.templates.request import RequestProtocol, ResponseProtocol',
    ]
    if uses_config:
        lines.append('from pydantic import ConfigDict')
    lines.append('')
    lines.append('from ..api import QQBotAPIError')
    lines.append('from ..events import qqbot_events')
    lines.append('from ..models import (')
    for name in model_names:
        lines.append(f'    {name},')
    lines.append(')')
    lines.append('')
    lines.append('__all__ = [')
    exports: list[str] = []
    for method in methods:
        stem = _class_stem(method)
        exports += [f'{stem}Request', f'{stem}Response', f'{stem}RequestEvent', f'{stem}ResponseEvent', method.name]
    for name in sorted(set(exports)):
        lines.append(f"    '{name}',")
    lines.append(']')
    lines.append('')

    for method in methods:
        lines.append('')
        lines.append('# ======================================================================')
        lines.append(f'# {method.name} —— {method.label}')
        lines.append('# ======================================================================')
        lines.append('')
        stem = _class_stem(method)
        result_type = method.result
        is_extra = method.extra or method.passthrough
        lines.append(f'class {stem}Request(RequestProtocol):')
        lines.append(f'    """{method.label}（``QQBotAPI.{method.name}`` 请求参数）。"""')
        if is_extra:
            lines.append('')
            lines.append("    model_config = ConfigDict(extra='allow')")
        if method.fields:
            lines.append('')
            for fname, annotation in method.fields:
                lines.append(f'    {fname}: {annotation}')
        lines.append('')
        lines.append('')
        lines.append(f'class {stem}Response(ResponseProtocol):')
        lines.append(f'    """{method.label}响应。"""')
        lines.append('')
        if result_type == 'None':
            lines.append('    result: None = None')
        else:
            # 允许缺省：失败响应（success=False）不含 result
            lines.append(f'    result: {result_type} | None = None')
        lines.append('')
        lines.append('')
        lines.append('@qqbot_events.event')
        lines.append(f'class {stem}RequestEvent(EventDeclaration):')
        lines.append(f'    """{method.label}（请求事件 ``qqbot.api.{method.name}.request``）。"""')
        lines.append('')
        lines.append(f"    name = 'qqbot.api.{method.name}.request'")
        lines.append(f'    payload_type = {stem}Request')
        lines.append('')
        lines.append('')
        lines.append('@qqbot_events.event')
        lines.append(f'class {stem}ResponseEvent(EventDeclaration):')
        lines.append(f'    """{method.label}（响应事件 ``qqbot.api.{method.name}.response``）。"""')
        lines.append('')
        lines.append(f"    name = 'qqbot.api.{method.name}.response'")
        lines.append(f'    payload_type = {stem}Response')
        lines.append('')
        lines.append('')
        lines.append('async def ' + method.name + '(')
        lines.append('    bus_proxy: EventBus.Proxy,')
        lines.append('    *,')
        for fname, annotation in method.fields:
            lines.append(f'    {fname}: {annotation},')
        lines.append('    session_id: str | None = None,')
        lines.append('    timeout: float | None = 60.0,')
        if is_extra:
            lines.append('    **extra: Any,')
        lines.append(f') -> {result_type}:')
        lines.append(f'    """{method.label}（强类型 RPC 客户端，底层为 ``event_bus.templates.request``）。"""')
        if method.fields:
            lines.append('    req_data: dict[str, Any] = {')
            for fname, _ in method.fields:
                lines.append(f"        '{fname}': {fname},")
            lines.append('    }')
        else:
            lines.append('    req_data: dict[str, Any] = {}')
        if is_extra:
            lines.append('    req_data.update(extra)')
        lines.append('    response = await request(')
        lines.append('        bus_proxy=bus_proxy,')
        lines.append(f'        req_event={stem}RequestEvent.name,')
        lines.append('        req_data=req_data,')
        lines.append(f'        resp_event={stem}ResponseEvent.name,')
        lines.append('        session_id=session_id,')
        lines.append('        timeout=timeout,')
        lines.append('    )')
        lines.append('    if not response.success:')
        lines.append("        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')")
        lines.append(f'    assert isinstance(response, {stem}Response)')
        if result_type != 'None':
            lines.append("    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'")
        lines.append('    return response.result')
        lines.append('')
        lines.append('')

    return '\n'.join(lines)


def _render_handlers_module(category: str, methods: tuple[Method, ...]) -> str:
    mixin = MIXIN_NAMES[category]
    imports: list[str] = []
    for method in methods:
        stem = _class_stem(method)
        imports.append(f'{stem}Request')
        imports.append(f'{stem}RequestEvent')
        imports.append(f'{stem}ResponseEvent')

    lines: list[str] = [
        f'"""自动生成：{category} RPC 处理器（显式关键字调用 ``QQBotAPI``）。',
        '',
        '请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::',
        '',
        '    uv run python tools/gen_rpc.py',
        '    uv run ruff check --fix src',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from typing import Any',
        '',
        'from event_bus import Event, EventBus',
        'from event_bus.templates import ServiceHandler, process',
        '',
        'from ...api import QQBotAPI',
        f'from ..{category} import (',
    ]
    for name in sorted(imports):
        lines.append(f'    {name},')
    lines.append(')')
    lines.append('')
    lines.append(f"__all__ = ['{mixin}']")
    lines.append('')
    lines.append('')
    lines.append(f'class {mixin}(ServiceHandler):')
    lines.append(f'    """{category} RPC 处理器 mixin。"""')
    lines.append('')
    lines.append('    _api: QQBotAPI')

    for method in methods:
        stem = _class_stem(method)
        is_extra = method.extra or method.passthrough
        lines.append('')
        lines.append(f'    @process({stem}RequestEvent, {stem}ResponseEvent)')
        lines.append(f'    async def {method.name}(')
        lines.append('        self,')
        lines.append(f'        payload: {stem}Request,')
        lines.append('        bus_proxy: EventBus.Proxy,')
        lines.append('        raw_event: Event,')
        lines.append('    ) -> dict[str, Any]:')
        lines.append(f'        """{method.label}。"""')
        if method.result == 'None':
            lines.append(f'        await self._api.{method.name}(')
        else:
            lines.append(f'        result = await self._api.{method.name}(')
        for fname, annotation in method.fields:
            annotation = _type_expr(annotation)
            lines.append(f'            {fname}=payload.{fname},')
        if is_extra:
            lines.append('            **(payload.model_extra or {}),')
        lines.append('        )')
        if method.result == 'None':
            lines.append("        return {'result': None}")
        else:
            lines.append("        return {'result': result}")
        lines.append('')

    return '\n'.join(lines)


def main() -> None:
    """生成全部 RPC 模块。"""
    generated: list[Path] = []
    for category, methods in CATEGORIES.items():
        for target, renderer in (
            (RPC_DIR / f'{category}.py', _render_models_module),
            (RPC_DIR / 'handlers' / f'{category}.py', _render_handlers_module),
        ):
            target.write_text(renderer(category, methods), encoding='utf-8')
            generated.append(target)
    print(f'已生成 {len(generated)} 个文件、{sum(len(m) for m in CATEGORIES.values())} 个方法：')
    for path in generated:
        print(f'  - {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

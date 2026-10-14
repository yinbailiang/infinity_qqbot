"""自动生成：messages RPC —— 请求 / 响应模型、事件声明与强类型客户端。

请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

from typing import Any

from infinity_bus import EventBus, EventDeclaration
from infinity_bus.templates import request
from infinity_bus.templates.request import RequestProtocol, ResponseProtocol

from ..api import QQBotAPIError
from ..events import qqbot_events
from ..models import (
    FileUploadResponse,
    InputNotify,
    Keyboard,
    MediaInfo,
    MessageMarkdown,
    MessageReference,
    MessageResponse,
    StreamMessageResponse,
    UploadPrepareResponse,
)

__all__ = [
    'C2CUploadPartFinishRequest',
    'C2CUploadPartFinishRequestEvent',
    'C2CUploadPartFinishResponse',
    'C2CUploadPartFinishResponseEvent',
    'C2CUploadPrepareRequest',
    'C2CUploadPrepareRequestEvent',
    'C2CUploadPrepareResponse',
    'C2CUploadPrepareResponseEvent',
    'GroupUploadPartFinishRequest',
    'GroupUploadPartFinishRequestEvent',
    'GroupUploadPartFinishResponse',
    'GroupUploadPartFinishResponseEvent',
    'GroupUploadPrepareRequest',
    'GroupUploadPrepareRequestEvent',
    'GroupUploadPrepareResponse',
    'GroupUploadPrepareResponseEvent',
    'RecallC2CMessageRequest',
    'RecallC2CMessageRequestEvent',
    'RecallC2CMessageResponse',
    'RecallC2CMessageResponseEvent',
    'RecallGroupMessageRequest',
    'RecallGroupMessageRequestEvent',
    'RecallGroupMessageResponse',
    'RecallGroupMessageResponseEvent',
    'SendC2CMessageRequest',
    'SendC2CMessageRequestEvent',
    'SendC2CMessageResponse',
    'SendC2CMessageResponseEvent',
    'SendC2CStreamMessageRequest',
    'SendC2CStreamMessageRequestEvent',
    'SendC2CStreamMessageResponse',
    'SendC2CStreamMessageResponseEvent',
    'SendGroupMessageRequest',
    'SendGroupMessageRequestEvent',
    'SendGroupMessageResponse',
    'SendGroupMessageResponseEvent',
    'UploadC2CFileRequest',
    'UploadC2CFileRequestEvent',
    'UploadC2CFileResponse',
    'UploadC2CFileResponseEvent',
    'UploadGroupFileRequest',
    'UploadGroupFileRequestEvent',
    'UploadGroupFileResponse',
    'UploadGroupFileResponseEvent',
    'c2c_upload_part_finish',
    'c2c_upload_prepare',
    'group_upload_part_finish',
    'group_upload_prepare',
    'recall_c2c_message',
    'recall_group_message',
    'send_c2c_message',
    'send_c2c_stream_message',
    'send_group_message',
    'upload_c2c_file',
    'upload_group_file',
]


# ======================================================================
# send_c2c_message —— 发送单聊消息
# ======================================================================


class SendC2CMessageRequest(RequestProtocol):
    """发送单聊消息（``QQBotAPI.send_c2c_message`` 请求参数）。"""

    user_openid: str
    content: str | None = None
    msg_type: int | None = None
    markdown: MessageMarkdown | None = None
    keyboard: Keyboard | None = None
    msg_id: str | None = None
    event_id: str | None = None
    msg_seq: int | None = None
    media: MediaInfo | None = None
    message_reference: MessageReference | None = None
    is_wakeup: bool | None = None
    input_notify: InputNotify | None = None
    force_verify_image_resource: bool | None = None


class SendC2CMessageResponse(ResponseProtocol):
    """发送单聊消息响应。"""

    result: MessageResponse | None = None


@qqbot_events.event
class SendC2CMessageRequestEvent(EventDeclaration):
    """发送单聊消息（请求事件 ``qqbot.api.send_c2c_message.request``）。"""

    name = 'qqbot.api.send_c2c_message.request'
    payload_type = SendC2CMessageRequest


@qqbot_events.event
class SendC2CMessageResponseEvent(EventDeclaration):
    """发送单聊消息（响应事件 ``qqbot.api.send_c2c_message.response``）。"""

    name = 'qqbot.api.send_c2c_message.response'
    payload_type = SendC2CMessageResponse


async def send_c2c_message(
    bus_proxy: EventBus.Proxy,
    *,
    user_openid: str,
    content: str | None = None,
    msg_type: int | None = None,
    markdown: MessageMarkdown | None = None,
    keyboard: Keyboard | None = None,
    msg_id: str | None = None,
    event_id: str | None = None,
    msg_seq: int | None = None,
    media: MediaInfo | None = None,
    message_reference: MessageReference | None = None,
    is_wakeup: bool | None = None,
    input_notify: InputNotify | None = None,
    force_verify_image_resource: bool | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> MessageResponse:
    """发送单聊消息（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'user_openid': user_openid,
        'content': content,
        'msg_type': msg_type,
        'markdown': markdown,
        'keyboard': keyboard,
        'msg_id': msg_id,
        'event_id': event_id,
        'msg_seq': msg_seq,
        'media': media,
        'message_reference': message_reference,
        'is_wakeup': is_wakeup,
        'input_notify': input_notify,
        'force_verify_image_resource': force_verify_image_resource,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=SendC2CMessageRequestEvent.name,
        req_data=req_data,
        resp_event=SendC2CMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, SendC2CMessageResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# send_c2c_stream_message —— 流式发送单聊消息
# ======================================================================


class SendC2CStreamMessageRequest(RequestProtocol):
    """流式发送单聊消息（``QQBotAPI.send_c2c_stream_message`` 请求参数）。"""

    user_openid: str
    input_state: int
    index: int
    content_raw: str | None = None
    input_mode: str | None = None
    content_type: str | None = None
    msg_id: str | None = None
    event_id: str | None = None
    stream_msg_id: str | None = None
    msg_seq: int | None = None
    is_wakeup: bool | None = None


class SendC2CStreamMessageResponse(ResponseProtocol):
    """流式发送单聊消息响应。"""

    result: StreamMessageResponse | None = None


@qqbot_events.event
class SendC2CStreamMessageRequestEvent(EventDeclaration):
    """流式发送单聊消息（请求事件 ``qqbot.api.send_c2c_stream_message.request``）。"""

    name = 'qqbot.api.send_c2c_stream_message.request'
    payload_type = SendC2CStreamMessageRequest


@qqbot_events.event
class SendC2CStreamMessageResponseEvent(EventDeclaration):
    """流式发送单聊消息（响应事件 ``qqbot.api.send_c2c_stream_message.response``）。"""

    name = 'qqbot.api.send_c2c_stream_message.response'
    payload_type = SendC2CStreamMessageResponse


async def send_c2c_stream_message(
    bus_proxy: EventBus.Proxy,
    *,
    user_openid: str,
    input_state: int,
    index: int,
    content_raw: str | None = None,
    input_mode: str | None = None,
    content_type: str | None = None,
    msg_id: str | None = None,
    event_id: str | None = None,
    stream_msg_id: str | None = None,
    msg_seq: int | None = None,
    is_wakeup: bool | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> StreamMessageResponse:
    """流式发送单聊消息（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'user_openid': user_openid,
        'input_state': input_state,
        'index': index,
        'content_raw': content_raw,
        'input_mode': input_mode,
        'content_type': content_type,
        'msg_id': msg_id,
        'event_id': event_id,
        'stream_msg_id': stream_msg_id,
        'msg_seq': msg_seq,
        'is_wakeup': is_wakeup,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=SendC2CStreamMessageRequestEvent.name,
        req_data=req_data,
        resp_event=SendC2CStreamMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, SendC2CStreamMessageResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# recall_c2c_message —— 撤回单聊消息
# ======================================================================


class RecallC2CMessageRequest(RequestProtocol):
    """撤回单聊消息（``QQBotAPI.recall_c2c_message`` 请求参数）。"""

    user_openid: str
    message_id: str


class RecallC2CMessageResponse(ResponseProtocol):
    """撤回单聊消息响应。"""

    result: None = None


@qqbot_events.event
class RecallC2CMessageRequestEvent(EventDeclaration):
    """撤回单聊消息（请求事件 ``qqbot.api.recall_c2c_message.request``）。"""

    name = 'qqbot.api.recall_c2c_message.request'
    payload_type = RecallC2CMessageRequest


@qqbot_events.event
class RecallC2CMessageResponseEvent(EventDeclaration):
    """撤回单聊消息（响应事件 ``qqbot.api.recall_c2c_message.response``）。"""

    name = 'qqbot.api.recall_c2c_message.response'
    payload_type = RecallC2CMessageResponse


async def recall_c2c_message(
    bus_proxy: EventBus.Proxy,
    *,
    user_openid: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """撤回单聊消息（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'user_openid': user_openid,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RecallC2CMessageRequestEvent.name,
        req_data=req_data,
        resp_event=RecallC2CMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RecallC2CMessageResponse)
    return response.result


# ======================================================================
# upload_c2c_file —— 单聊富媒体上传
# ======================================================================


class UploadC2CFileRequest(RequestProtocol):
    """单聊富媒体上传（``QQBotAPI.upload_c2c_file`` 请求参数）。"""

    user_openid: str
    file_type: int
    url: str | None = None
    file_name: str | None = None
    srv_send_msg: bool | None = None
    upload_id: str | None = None


class UploadC2CFileResponse(ResponseProtocol):
    """单聊富媒体上传响应。"""

    result: FileUploadResponse | None = None


@qqbot_events.event
class UploadC2CFileRequestEvent(EventDeclaration):
    """单聊富媒体上传（请求事件 ``qqbot.api.upload_c2c_file.request``）。"""

    name = 'qqbot.api.upload_c2c_file.request'
    payload_type = UploadC2CFileRequest


@qqbot_events.event
class UploadC2CFileResponseEvent(EventDeclaration):
    """单聊富媒体上传（响应事件 ``qqbot.api.upload_c2c_file.response``）。"""

    name = 'qqbot.api.upload_c2c_file.response'
    payload_type = UploadC2CFileResponse


async def upload_c2c_file(
    bus_proxy: EventBus.Proxy,
    *,
    user_openid: str,
    file_type: int,
    url: str | None = None,
    file_name: str | None = None,
    srv_send_msg: bool | None = None,
    upload_id: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> FileUploadResponse:
    """单聊富媒体上传（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'user_openid': user_openid,
        'file_type': file_type,
        'url': url,
        'file_name': file_name,
        'srv_send_msg': srv_send_msg,
        'upload_id': upload_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UploadC2CFileRequestEvent.name,
        req_data=req_data,
        resp_event=UploadC2CFileResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UploadC2CFileResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# c2c_upload_prepare —— 单聊富媒体预上传
# ======================================================================


class C2CUploadPrepareRequest(RequestProtocol):
    """单聊富媒体预上传（``QQBotAPI.c2c_upload_prepare`` 请求参数）。"""

    user_openid: str
    file_type: int
    file_size: int | str
    file_name: str
    md5: str
    sha1: str
    md5_10m: str


class C2CUploadPrepareResponse(ResponseProtocol):
    """单聊富媒体预上传响应。"""

    result: UploadPrepareResponse | None = None


@qqbot_events.event
class C2CUploadPrepareRequestEvent(EventDeclaration):
    """单聊富媒体预上传（请求事件 ``qqbot.api.c2c_upload_prepare.request``）。"""

    name = 'qqbot.api.c2c_upload_prepare.request'
    payload_type = C2CUploadPrepareRequest


@qqbot_events.event
class C2CUploadPrepareResponseEvent(EventDeclaration):
    """单聊富媒体预上传（响应事件 ``qqbot.api.c2c_upload_prepare.response``）。"""

    name = 'qqbot.api.c2c_upload_prepare.response'
    payload_type = C2CUploadPrepareResponse


async def c2c_upload_prepare(
    bus_proxy: EventBus.Proxy,
    *,
    user_openid: str,
    file_type: int,
    file_size: int | str,
    file_name: str,
    md5: str,
    sha1: str,
    md5_10m: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> UploadPrepareResponse:
    """单聊富媒体预上传（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'user_openid': user_openid,
        'file_type': file_type,
        'file_size': file_size,
        'file_name': file_name,
        'md5': md5,
        'sha1': sha1,
        'md5_10m': md5_10m,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=C2CUploadPrepareRequestEvent.name,
        req_data=req_data,
        resp_event=C2CUploadPrepareResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, C2CUploadPrepareResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# c2c_upload_part_finish —— 单聊分片上传完成
# ======================================================================


class C2CUploadPartFinishRequest(RequestProtocol):
    """单聊分片上传完成（``QQBotAPI.c2c_upload_part_finish`` 请求参数）。"""

    user_openid: str
    upload_id: str | None = None
    part_index: int | None = None
    block_size: str | None = None
    md5: str | None = None


class C2CUploadPartFinishResponse(ResponseProtocol):
    """单聊分片上传完成响应。"""

    result: None = None


@qqbot_events.event
class C2CUploadPartFinishRequestEvent(EventDeclaration):
    """单聊分片上传完成（请求事件 ``qqbot.api.c2c_upload_part_finish.request``）。"""

    name = 'qqbot.api.c2c_upload_part_finish.request'
    payload_type = C2CUploadPartFinishRequest


@qqbot_events.event
class C2CUploadPartFinishResponseEvent(EventDeclaration):
    """单聊分片上传完成（响应事件 ``qqbot.api.c2c_upload_part_finish.response``）。"""

    name = 'qqbot.api.c2c_upload_part_finish.response'
    payload_type = C2CUploadPartFinishResponse


async def c2c_upload_part_finish(
    bus_proxy: EventBus.Proxy,
    *,
    user_openid: str,
    upload_id: str | None = None,
    part_index: int | None = None,
    block_size: str | None = None,
    md5: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """单聊分片上传完成（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'user_openid': user_openid,
        'upload_id': upload_id,
        'part_index': part_index,
        'block_size': block_size,
        'md5': md5,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=C2CUploadPartFinishRequestEvent.name,
        req_data=req_data,
        resp_event=C2CUploadPartFinishResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, C2CUploadPartFinishResponse)
    return response.result


# ======================================================================
# send_group_message —— 发送群聊消息
# ======================================================================


class SendGroupMessageRequest(RequestProtocol):
    """发送群聊消息（``QQBotAPI.send_group_message`` 请求参数）。"""

    group_openid: str
    content: str | None = None
    msg_type: int | None = None
    markdown: MessageMarkdown | None = None
    keyboard: Keyboard | None = None
    msg_id: str | None = None
    event_id: str | None = None
    msg_seq: int | None = None
    media: MediaInfo | None = None
    message_reference: MessageReference | None = None
    is_wakeup: bool | None = None
    input_notify: InputNotify | None = None
    force_verify_image_resource: bool | None = None


class SendGroupMessageResponse(ResponseProtocol):
    """发送群聊消息响应。"""

    result: MessageResponse | None = None


@qqbot_events.event
class SendGroupMessageRequestEvent(EventDeclaration):
    """发送群聊消息（请求事件 ``qqbot.api.send_group_message.request``）。"""

    name = 'qqbot.api.send_group_message.request'
    payload_type = SendGroupMessageRequest


@qqbot_events.event
class SendGroupMessageResponseEvent(EventDeclaration):
    """发送群聊消息（响应事件 ``qqbot.api.send_group_message.response``）。"""

    name = 'qqbot.api.send_group_message.response'
    payload_type = SendGroupMessageResponse


async def send_group_message(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    content: str | None = None,
    msg_type: int | None = None,
    markdown: MessageMarkdown | None = None,
    keyboard: Keyboard | None = None,
    msg_id: str | None = None,
    event_id: str | None = None,
    msg_seq: int | None = None,
    media: MediaInfo | None = None,
    message_reference: MessageReference | None = None,
    is_wakeup: bool | None = None,
    input_notify: InputNotify | None = None,
    force_verify_image_resource: bool | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> MessageResponse:
    """发送群聊消息（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'content': content,
        'msg_type': msg_type,
        'markdown': markdown,
        'keyboard': keyboard,
        'msg_id': msg_id,
        'event_id': event_id,
        'msg_seq': msg_seq,
        'media': media,
        'message_reference': message_reference,
        'is_wakeup': is_wakeup,
        'input_notify': input_notify,
        'force_verify_image_resource': force_verify_image_resource,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=SendGroupMessageRequestEvent.name,
        req_data=req_data,
        resp_event=SendGroupMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, SendGroupMessageResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# recall_group_message —— 撤回群聊消息
# ======================================================================


class RecallGroupMessageRequest(RequestProtocol):
    """撤回群聊消息（``QQBotAPI.recall_group_message`` 请求参数）。"""

    group_openid: str
    message_id: str


class RecallGroupMessageResponse(ResponseProtocol):
    """撤回群聊消息响应。"""

    result: None = None


@qqbot_events.event
class RecallGroupMessageRequestEvent(EventDeclaration):
    """撤回群聊消息（请求事件 ``qqbot.api.recall_group_message.request``）。"""

    name = 'qqbot.api.recall_group_message.request'
    payload_type = RecallGroupMessageRequest


@qqbot_events.event
class RecallGroupMessageResponseEvent(EventDeclaration):
    """撤回群聊消息（响应事件 ``qqbot.api.recall_group_message.response``）。"""

    name = 'qqbot.api.recall_group_message.response'
    payload_type = RecallGroupMessageResponse


async def recall_group_message(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    message_id: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """撤回群聊消息（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'message_id': message_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=RecallGroupMessageRequestEvent.name,
        req_data=req_data,
        resp_event=RecallGroupMessageResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, RecallGroupMessageResponse)
    return response.result


# ======================================================================
# upload_group_file —— 群聊富媒体上传
# ======================================================================


class UploadGroupFileRequest(RequestProtocol):
    """群聊富媒体上传（``QQBotAPI.upload_group_file`` 请求参数）。"""

    group_openid: str
    file_type: int
    url: str | None = None
    file_name: str | None = None
    srv_send_msg: bool | None = None
    upload_id: str | None = None


class UploadGroupFileResponse(ResponseProtocol):
    """群聊富媒体上传响应。"""

    result: FileUploadResponse | None = None


@qqbot_events.event
class UploadGroupFileRequestEvent(EventDeclaration):
    """群聊富媒体上传（请求事件 ``qqbot.api.upload_group_file.request``）。"""

    name = 'qqbot.api.upload_group_file.request'
    payload_type = UploadGroupFileRequest


@qqbot_events.event
class UploadGroupFileResponseEvent(EventDeclaration):
    """群聊富媒体上传（响应事件 ``qqbot.api.upload_group_file.response``）。"""

    name = 'qqbot.api.upload_group_file.response'
    payload_type = UploadGroupFileResponse


async def upload_group_file(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    file_type: int,
    url: str | None = None,
    file_name: str | None = None,
    srv_send_msg: bool | None = None,
    upload_id: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> FileUploadResponse:
    """群聊富媒体上传（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'file_type': file_type,
        'url': url,
        'file_name': file_name,
        'srv_send_msg': srv_send_msg,
        'upload_id': upload_id,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=UploadGroupFileRequestEvent.name,
        req_data=req_data,
        resp_event=UploadGroupFileResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, UploadGroupFileResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# group_upload_prepare —— 群聊富媒体预上传
# ======================================================================


class GroupUploadPrepareRequest(RequestProtocol):
    """群聊富媒体预上传（``QQBotAPI.group_upload_prepare`` 请求参数）。"""

    group_openid: str
    file_type: int
    file_size: int | str
    file_name: str
    md5: str
    sha1: str
    md5_10m: str


class GroupUploadPrepareResponse(ResponseProtocol):
    """群聊富媒体预上传响应。"""

    result: UploadPrepareResponse | None = None


@qqbot_events.event
class GroupUploadPrepareRequestEvent(EventDeclaration):
    """群聊富媒体预上传（请求事件 ``qqbot.api.group_upload_prepare.request``）。"""

    name = 'qqbot.api.group_upload_prepare.request'
    payload_type = GroupUploadPrepareRequest


@qqbot_events.event
class GroupUploadPrepareResponseEvent(EventDeclaration):
    """群聊富媒体预上传（响应事件 ``qqbot.api.group_upload_prepare.response``）。"""

    name = 'qqbot.api.group_upload_prepare.response'
    payload_type = GroupUploadPrepareResponse


async def group_upload_prepare(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    file_type: int,
    file_size: int | str,
    file_name: str,
    md5: str,
    sha1: str,
    md5_10m: str,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> UploadPrepareResponse:
    """群聊富媒体预上传（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'file_type': file_type,
        'file_size': file_size,
        'file_name': file_name,
        'md5': md5,
        'sha1': sha1,
        'md5_10m': md5_10m,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GroupUploadPrepareRequestEvent.name,
        req_data=req_data,
        resp_event=GroupUploadPrepareResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GroupUploadPrepareResponse)
    assert response.result is not None, '响应缺少 result（success=True 时不应发生）'
    return response.result


# ======================================================================
# group_upload_part_finish —— 群聊分片上传完成
# ======================================================================


class GroupUploadPartFinishRequest(RequestProtocol):
    """群聊分片上传完成（``QQBotAPI.group_upload_part_finish`` 请求参数）。"""

    group_openid: str
    upload_id: str | None = None
    part_index: int | None = None
    block_size: str | None = None
    md5: str | None = None


class GroupUploadPartFinishResponse(ResponseProtocol):
    """群聊分片上传完成响应。"""

    result: None = None


@qqbot_events.event
class GroupUploadPartFinishRequestEvent(EventDeclaration):
    """群聊分片上传完成（请求事件 ``qqbot.api.group_upload_part_finish.request``）。"""

    name = 'qqbot.api.group_upload_part_finish.request'
    payload_type = GroupUploadPartFinishRequest


@qqbot_events.event
class GroupUploadPartFinishResponseEvent(EventDeclaration):
    """群聊分片上传完成（响应事件 ``qqbot.api.group_upload_part_finish.response``）。"""

    name = 'qqbot.api.group_upload_part_finish.response'
    payload_type = GroupUploadPartFinishResponse


async def group_upload_part_finish(
    bus_proxy: EventBus.Proxy,
    *,
    group_openid: str,
    upload_id: str | None = None,
    part_index: int | None = None,
    block_size: str | None = None,
    md5: str | None = None,
    session_id: str | None = None,
    timeout: float | None = 60.0,
) -> None:
    """群聊分片上传完成（强类型 RPC 客户端，底层为 ``infinity_bus.templates.request``）。"""
    req_data: dict[str, Any] = {
        'group_openid': group_openid,
        'upload_id': upload_id,
        'part_index': part_index,
        'block_size': block_size,
        'md5': md5,
    }
    response = await request(
        bus_proxy=bus_proxy,
        req_event=GroupUploadPartFinishRequestEvent.name,
        req_data=req_data,
        resp_event=GroupUploadPartFinishResponseEvent.name,
        session_id=session_id,
        timeout=timeout,
    )
    if not response.success:
        raise QQBotAPIError(None, response.error_msg or 'RPC 调用失败')
    assert isinstance(response, GroupUploadPartFinishResponse)
    return response.result

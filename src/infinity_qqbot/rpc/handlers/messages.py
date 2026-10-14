"""自动生成：messages RPC 处理器（显式关键字调用 ``QQBotAPI``）。

请勿手改本文件；修改 ``tools/gen_rpc.py`` 中的规格后运行::

    uv run python tools/gen_rpc.py
    uv run ruff check --fix src
"""

from __future__ import annotations

from typing import Any

from infinity_bus import Event, EventBus
from infinity_bus.templates import ServiceHandler, process

from ...api import QQBotAPI
from ..messages import (
    C2CUploadPartFinishRequest,
    C2CUploadPartFinishRequestEvent,
    C2CUploadPartFinishResponseEvent,
    C2CUploadPrepareRequest,
    C2CUploadPrepareRequestEvent,
    C2CUploadPrepareResponseEvent,
    GroupUploadPartFinishRequest,
    GroupUploadPartFinishRequestEvent,
    GroupUploadPartFinishResponseEvent,
    GroupUploadPrepareRequest,
    GroupUploadPrepareRequestEvent,
    GroupUploadPrepareResponseEvent,
    RecallC2CMessageRequest,
    RecallC2CMessageRequestEvent,
    RecallC2CMessageResponseEvent,
    RecallGroupMessageRequest,
    RecallGroupMessageRequestEvent,
    RecallGroupMessageResponseEvent,
    SendC2CMessageRequest,
    SendC2CMessageRequestEvent,
    SendC2CMessageResponseEvent,
    SendC2CStreamMessageRequest,
    SendC2CStreamMessageRequestEvent,
    SendC2CStreamMessageResponseEvent,
    SendGroupMessageRequest,
    SendGroupMessageRequestEvent,
    SendGroupMessageResponseEvent,
    UploadC2CFileRequest,
    UploadC2CFileRequestEvent,
    UploadC2CFileResponseEvent,
    UploadGroupFileRequest,
    UploadGroupFileRequestEvent,
    UploadGroupFileResponseEvent,
)

__all__ = ['MessageHandlersMixin']


class MessageHandlersMixin(ServiceHandler):
    """messages RPC 处理器 mixin。"""

    _api: QQBotAPI

    @process(SendC2CMessageRequestEvent, SendC2CMessageResponseEvent)
    async def send_c2c_message(
        self,
        payload: SendC2CMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """发送单聊消息。"""
        result = await self._api.send_c2c_message(
            user_openid=payload.user_openid,
            content=payload.content,
            msg_type=payload.msg_type,
            markdown=payload.markdown,
            keyboard=payload.keyboard,
            msg_id=payload.msg_id,
            event_id=payload.event_id,
            msg_seq=payload.msg_seq,
            media=payload.media,
            message_reference=payload.message_reference,
            is_wakeup=payload.is_wakeup,
            input_notify=payload.input_notify,
            force_verify_image_resource=payload.force_verify_image_resource,
        )
        return {'result': result}

    @process(SendC2CStreamMessageRequestEvent, SendC2CStreamMessageResponseEvent)
    async def send_c2c_stream_message(
        self,
        payload: SendC2CStreamMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """流式发送单聊消息。"""
        result = await self._api.send_c2c_stream_message(
            user_openid=payload.user_openid,
            input_state=payload.input_state,
            index=payload.index,
            content_raw=payload.content_raw,
            input_mode=payload.input_mode,
            content_type=payload.content_type,
            msg_id=payload.msg_id,
            event_id=payload.event_id,
            stream_msg_id=payload.stream_msg_id,
            msg_seq=payload.msg_seq,
            is_wakeup=payload.is_wakeup,
        )
        return {'result': result}

    @process(RecallC2CMessageRequestEvent, RecallC2CMessageResponseEvent)
    async def recall_c2c_message(
        self,
        payload: RecallC2CMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """撤回单聊消息。"""
        await self._api.recall_c2c_message(
            user_openid=payload.user_openid,
            message_id=payload.message_id,
        )
        return {'result': None}

    @process(UploadC2CFileRequestEvent, UploadC2CFileResponseEvent)
    async def upload_c2c_file(
        self,
        payload: UploadC2CFileRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """单聊富媒体上传。"""
        result = await self._api.upload_c2c_file(
            user_openid=payload.user_openid,
            file_type=payload.file_type,
            url=payload.url,
            file_name=payload.file_name,
            srv_send_msg=payload.srv_send_msg,
            upload_id=payload.upload_id,
        )
        return {'result': result}

    @process(C2CUploadPrepareRequestEvent, C2CUploadPrepareResponseEvent)
    async def c2c_upload_prepare(
        self,
        payload: C2CUploadPrepareRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """单聊富媒体预上传。"""
        result = await self._api.c2c_upload_prepare(
            user_openid=payload.user_openid,
            file_type=payload.file_type,
            file_size=payload.file_size,
            file_name=payload.file_name,
            md5=payload.md5,
            sha1=payload.sha1,
            md5_10m=payload.md5_10m,
        )
        return {'result': result}

    @process(C2CUploadPartFinishRequestEvent, C2CUploadPartFinishResponseEvent)
    async def c2c_upload_part_finish(
        self,
        payload: C2CUploadPartFinishRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """单聊分片上传完成。"""
        await self._api.c2c_upload_part_finish(
            user_openid=payload.user_openid,
            upload_id=payload.upload_id,
            part_index=payload.part_index,
            block_size=payload.block_size,
            md5=payload.md5,
        )
        return {'result': None}

    @process(SendGroupMessageRequestEvent, SendGroupMessageResponseEvent)
    async def send_group_message(
        self,
        payload: SendGroupMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """发送群聊消息。"""
        result = await self._api.send_group_message(
            group_openid=payload.group_openid,
            content=payload.content,
            msg_type=payload.msg_type,
            markdown=payload.markdown,
            keyboard=payload.keyboard,
            msg_id=payload.msg_id,
            event_id=payload.event_id,
            msg_seq=payload.msg_seq,
            media=payload.media,
            message_reference=payload.message_reference,
            is_wakeup=payload.is_wakeup,
            input_notify=payload.input_notify,
            force_verify_image_resource=payload.force_verify_image_resource,
        )
        return {'result': result}

    @process(RecallGroupMessageRequestEvent, RecallGroupMessageResponseEvent)
    async def recall_group_message(
        self,
        payload: RecallGroupMessageRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """撤回群聊消息。"""
        await self._api.recall_group_message(
            group_openid=payload.group_openid,
            message_id=payload.message_id,
        )
        return {'result': None}

    @process(UploadGroupFileRequestEvent, UploadGroupFileResponseEvent)
    async def upload_group_file(
        self,
        payload: UploadGroupFileRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """群聊富媒体上传。"""
        result = await self._api.upload_group_file(
            group_openid=payload.group_openid,
            file_type=payload.file_type,
            url=payload.url,
            file_name=payload.file_name,
            srv_send_msg=payload.srv_send_msg,
            upload_id=payload.upload_id,
        )
        return {'result': result}

    @process(GroupUploadPrepareRequestEvent, GroupUploadPrepareResponseEvent)
    async def group_upload_prepare(
        self,
        payload: GroupUploadPrepareRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """群聊富媒体预上传。"""
        result = await self._api.group_upload_prepare(
            group_openid=payload.group_openid,
            file_type=payload.file_type,
            file_size=payload.file_size,
            file_name=payload.file_name,
            md5=payload.md5,
            sha1=payload.sha1,
            md5_10m=payload.md5_10m,
        )
        return {'result': result}

    @process(GroupUploadPartFinishRequestEvent, GroupUploadPartFinishResponseEvent)
    async def group_upload_part_finish(
        self,
        payload: GroupUploadPartFinishRequest,
        bus_proxy: EventBus.Proxy,
        raw_event: Event,
    ) -> dict[str, Any]:
        """群聊分片上传完成。"""
        await self._api.group_upload_part_finish(
            group_openid=payload.group_openid,
            upload_id=payload.upload_id,
            part_index=payload.part_index,
            block_size=payload.block_size,
            md5=payload.md5,
        )
        return {'result': None}

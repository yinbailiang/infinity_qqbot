"""模型基类。"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ['QQModel']


class QQModel(BaseModel):
    """QQBot 模型基类：允许平台新增字段，兼容别名填充。"""

    model_config = ConfigDict(extra='allow', populate_by_name=True)

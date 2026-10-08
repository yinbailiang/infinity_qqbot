"""强类型 RPC 子包：请求 / 响应模型、事件声明、客户端与处理器。

- ``messages`` / ``groups`` / ``channels`` / ``interactions``：由
  ``tools/gen_rpc.py`` 生成的显式代码（每方法：请求模型、响应模型、
  请求 / 响应事件声明、强类型客户端函数）；
- ``handlers``：``QQBotAPIHandler``（按类别 mixin 组装，显式关键字调用 ``QQBotAPI``）。

生成的客户端底层直接使用 ``event_bus.templates.request`` 模板发起调用，
失败（``success=False``）时抛出 :class:`~infinity_qqbot.api.QQBotAPIError`。

使用示例::

    from infinity_qqbot import send_c2c_message

    message = await send_c2c_message(
        bus.proxy('app'),
        user_openid=openid,
        content='hello',
        msg_id=msg_id,
    )
"""

from .channels import *
from .groups import *
from .handlers import *
from .interactions import *
from .messages import *

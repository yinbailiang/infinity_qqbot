# infinity-qqbot

基于 [infinity_bus](https://github.com/yinbailiang/infinity_bus) 的 QQ 机器人引擎。

- **`QQBotAPI`**：使用 `aiohttp` + `certifi` 完整封装 QQ 机器人开放平台 v2 接口
  （消息收发、富媒体上传、群管理、频道管理（子频道权限、禁言、论坛、音频等）、
  互动回调、菜单面板等；HTTP 429 自动退避重试、201/202 异步受理语义）；
- **`QQBotGateway` / `QQBot`**：WebSocket 网关客户端（心跳、Identify/Resume、
  自动重连、断线补发），输出类型化事件流；
- **`QQBotEventHandler`**：接受 `QQBotAPI`，随总线激活自动连接网关，
  并把每个事件自动发布为 `qqbot.event.<type>`（如 `qqbot.event.group_at_message_create`）；
- **`QQBotAPIHandler` + 强类型客户端**：集成 `ServiceHandler`，95 个 API 方法逐一暴露为
  总线 RPC（请求 / 响应模型、事件声明、客户端函数由 `tools/gen_rpc.py` 从规格生成，
  运行期零元编程），调用 `await send_c2c_message(...)` 即完成一次强类型 RPC；
- 数据模型按域拆分在 `models/` 包；事件声明采用嵌套 `Payload` 风格，全部由 Pydantic 校验。

## 安装

```bash
uv sync
```

## 快速开始

```python
import asyncio

from infinity_bus import EventBus, EventHandler, EventHandlerRegistry, EventRegistry, Regex

from infinity_qqbot import (
    QQBotAPI,
    qqbot_events,
    register_handlers,
    send_c2c_message,
)


class Echo(EventHandler):
    """订阅单聊消息，通过总线 RPC 回复。"""

    def __init__(self) -> None:
        super().__init__(subscriptions=[Regex(r'qqbot\.event\.c2c_message_create')])

    async def handle(self, payload, bus_proxy, raw_event) -> None:
        await send_c2c_message(
            bus_proxy,
            user_openid=payload.user_openid,
            content=f'收到：{payload.content}',
            msg_id=payload.id,  # 被动回复（也可使用 event_id）
        )


async def main() -> None:
    api = QQBotAPI('你的AppID', '你的AppSecret')

    registry = EventRegistry()
    qqbot_events.register_all_events(registry)  # 注册全部事件声明（ModuleEventRegister）

    handlers = EventHandlerRegistry()
    await handlers.register(Echo())
    await register_handlers(handlers, api)  # 入站：网关事件 -> 总线；出站：总线 RPC -> OpenAPI

    async with EventBus(registry, handlers):
        await asyncio.Event().wait()  # 常驻运行


asyncio.run(main())
```

## 事件订阅

总线事件名 = `qqbot.event.` + 平台事件名小写，例如：

| 平台事件 | 总线事件 | 声明类 |
| - | - | - |
| `C2C_MESSAGE_CREATE` | `qqbot.event.c2c_message_create` | `C2CMessageCreateEvent` |
| `GROUP_AT_MESSAGE_CREATE` | `qqbot.event.group_at_message_create` | `GroupAtMessageCreateEvent` |
| `AT_MESSAGE_CREATE` | `qqbot.event.at_message_create` | `MessageCreateEvent` 系列 |
| `INTERACTION_CREATE` | `qqbot.event.interaction_create` | `InteractionCreateEvent` |
| `GROUP_ADD_ROBOT` | `qqbot.event.group_add_robot` | `GroupAddRobotEvent` |
| …（共 58 个平台事件） | | |

订阅方式二选一：

- 精确订阅：`super().__init__(subscriptions=['qqbot.event.c2c_message_create'])`；
- 通配订阅：`super().__init__(subscriptions=[Regex(r'qqbot\.event\..*')])`。

未建模的新事件会被兜底发布到 `qqbot.event.unknown`（负载含 `type` 与原始 `data`），
不会导致引擎崩溃。

事件声明在定义时由 `ModuleEventRegister` 自动收集（`infinity_qqbot.qqbot_events`），
注册时直接调用 `qqbot_events.register_all_events(registry)`，新增声明无需手工维护清单。

## 强类型 RPC 调用 API

每个 API 方法都有生成的**请求模型、响应模型、事件声明与强类型客户端**
（`tools/gen_rpc.py` 从方法规格生成，纯显式代码、运行期零元编程）：

```python
from infinity_qqbot import send_group_message

message = await send_group_message(
    bus_proxy,
    group_openid=group_openid,
    content='hello',
    msg_id=message_id,  # 被动回复（也可使用 event_id）
)
print(message.id)  # MessageResponse（类型由客户端签名给出）
```

- 客户端底层**直接使用** `infinity_bus.templates.request` 模板，自动以
  `session_id + request_id` 关联请求与响应；
- 事件名：`qqbot.api.<method>.request` / `qqbot.api.<method>.response`，
  可直接订阅任意方法的请求 / 响应事件；
- 请求 / 响应模型**直接继承**库的 `RequestProtocol` / `ResponseProtocol`；
- 失败时抛出 `QQBotAPIError`（`error_msg` 含平台错误码，跨总线保留）；
- 需要修改 / 新增方法时，编辑 `tools/gen_rpc.py` 中的规格并重新生成：

  ```bash
  uv run python tools/gen_rpc.py
  uv run ruff check --fix src
  ```

链路：客户端 → `request()` 模板 → `qqbot.api.<method>.request`
→ `QQBotAPIHandler.<method>` → `QQBotAPI.<method>` → `qqbot.api.<method>.response`。

## 模板能力（infinity_bus.templates）

本项目尽可能复用了 `infinity_bus` 的模板能力，业务侧也可直接使用：

- **批量处理器注册**：`await register_handlers(handlers, api)` 基于 `ModuleHandlerRegister`
  一次性注册入站 / 出站处理器；
- **幂等去重**：QQ 可能重复推送同一事件，注入 `IdempotencyRecorder` 即可按事件 ID 去重
  （发布成功才记录）：

  ```python
  from infinity_bus.templates import InMemoryIdempotencyRecorder

  from infinity_qqbot import register_handlers

  await register_handlers(
      handlers,
      api,
      dedup_recorder=InMemoryIdempotencyRecorder(),  # 或 SqliteIdempotencyRecorder('bot.db')
  )
  ```

- **等待事件**：`wait_for_event()` 基于 `expect` 模板注册一次性监听：

  ```python
  from infinity_qqbot import ReadyEvent, wait_for_event

  await wait_for_event(bus.proxy('app'), ReadyEvent.name, timeout=30)
  ```

- **中间件**：`infinity_bus.templates.middlewares` 提供的日志（JSONL / SQLite）、限流、
  递归防护、事件转换等中间件可直接挂到总线：

  ```python
  from infinity_bus.templates import RecursionGuardMiddleware

  await bus.proxy('app').middleware.add(RecursionGuardMiddleware())
  ```

- **简化处理器**：`infinity_bus.templates.handler` 可把普通异步函数直接包装为处理器类：

  ```python
  from infinity_bus.templates import handler

  @handler(C2CMessageCreateEvent)
  async def echo(payload: C2CMessageCreateEvent.Payload) -> None:
      ...

  await handlers.register(echo())
  ```

- **其他模板**：`expect` / `temporary_handler` / `pipe` / `request` 等均可按需组合
  （本库的 RPC 客户端直接使用 `request` 模板，`wait_for_event` 使用 `expect`）。

## 独立使用引擎（不经总线）

```python
from infinity_qqbot import QQBot, QQBotAPI

async with QQBot(QQBotAPI(app_id, secret)) as bot:
    async for event in bot.stream():
        print(event.type, event.payload)
```

## API 覆盖范围

| 分类 | 代表接口 |
| - | - |
| 凭证 / 网关 | `get_access_token`、`fetch_access_token`、`get_gateway`、`get_gateway_bot` |
| 机器人 | `get_me`、`get_my_guilds`、`generate_url_link` |
| 单聊 | 发送 / 流式发送 / 撤回 / 富媒体上传（URL、分片预上传、分片完成） |
| 群聊 | 发送 / 撤回 / 富媒体上传 / 群信息 / 群成员 / 入群申请 / 自动审批策略 / 黑名单 / 禁言 |
| 互动 | `respond_interaction`、自定义菜单、指令面板 CRUD |
| 频道 | 子频道 CRUD、消息发送 / 查询 / 撤回、私信、成员、身份组、禁言、公告、API 权限、表情表态、精华消息、日程 |

> 少数接口的请求体字段会随平台更新（如入群自动审批策略、黑名单操作等），
> 相应的请求模型声明 `extra='allow'`，生成客户端的 `**extra` 可透传任意字段。

## 说明

- **证书**：始终使用 `certifi` 的 CA 包（`ssl.create_default_context(cafile=certifi.where())`），
  也支持注入自定义 `aiohttp.ClientSession` / `SSLContext`；
- **token**：`access_token` 自动缓存，有效期前 60 秒自动刷新，并发安全（`asyncio.Lock`）；
- **重连**：网关断线指数退避重连，优先 `Resume` 补发遗漏事件；
  致命关闭码（4001/4002/401x/4914/4915 等）抛出 `QQBotGatewayClosed` 停止重试；
- **停机**：总线 `stop()` 会注销处理器，事件泵随之取消并断开网关。

## 开发

```bash
uv sync --extra dev             # 安装开发依赖（ruff / pyright / interrogate / pre-commit / agent-kit）
uv run pre-commit install       # 挂载提交钩子（一次性）

uv run python tools/gen_rpc.py  # 生成 RPC 模型 / 事件 / 客户端 / 处理器
uv run ruff check . --fix       # 静态检查（含 RUF022：`__all__` 自动排序）
uv run ruff format .            # 代码格式化
uv run pyright                  # 类型检查（strict 模式，零错误门禁）
uv run python tests/smoke.py    # 冒烟测试（不联网：事件收集 / token 缓存 / 强类型 RPC / 去重）

uv run pre-commit run --all-files   # 全量质量门（lint / 格式化 / pyright / docstring 覆盖 / 冒烟 / 规则防漂移）
```

- **质量门**（`.pre-commit-config.yaml`）：ruff、pyright（strict）、interrogate（docstring ≥ 90%）、
  冒烟测试、agent-kit 漂移检查；CI（`.github/workflows/test.yml`）在三平台复跑同一把门；
  推送 `v*` 标签触发 `publish.yml` 构建并发布（PyPI Trusted Publisher）。
- **智能体规则**（`AGENT.md` + `.agents/`）：由 [agent-kit](https://pypi.org/project/infinity-agent-kit/)
  统一同步（`uv run agent-kit update`），提交前检查见 `.agents/SKILLS/pre-commit-check.md`。

Ruff 配置见 `pyproject.toml`：`select = ["B", "C4", "E", "F", "I", "RUF", "SIM", "UP", "W"]`，
其中 `RUF022` 负责 `__all__` 的自动排序（`uv run ruff check --fix .` 直接修复）。

## 目录结构

```
src/infinity_qqbot/
├── __init__.py     # 公开导出
├── models/         # Pydantic 数据模型（按域拆分：common / message / group / menu / responses / payloads……）
├── rpc/            # 强类型 RPC（生成代码：模型 / 事件 / 客户端；handlers/ 为处理器）
├── events.py       # QQ 网关事件声明（嵌套 Payload 风格，定义即自动收集）
├── api.py          # QQBotAPI（aiohttp + certifi）
├── gateway.py      # QQBotGateway（WebSocket 心跳 / resume / 重连）
├── engine.py       # QQBot 引擎
└── handlers.py     # QQBotEventHandler / register_handlers / wait_for_event

tools/
└── gen_rpc.py      # RPC 代码生成器（方法规格 + 模板）

tests/
└── smoke.py        # 冒烟测试
```

工程化资产（家族标准，见 `AGENT.md` 与 `.agents/`）：

```text
AGENT.md                    # 智能体引导入口（agent-kit 渲染）
.agents/                    # 智能体静态规则（SKILLS / MEMORY / TEMP_FILES）
.github/workflows/          # CI/CD：test.yml（质量门 + 冒烟矩阵）、publish.yml（v* 标签发布）
.pre-commit-config.yaml     # 本地质量门（ruff / pyright / interrogate / 冒烟 / 规则防漂移）
```

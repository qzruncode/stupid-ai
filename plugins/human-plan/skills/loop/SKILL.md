---
name: loop
description: Use when the user invokes /human-plan:loop to run, tick, inspect, or stop the Human Plan background batch loop.
---

# Loop

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`loop` 负责把 `human-plan` 从单个 Plan 闭环提升为后台批次循环。它不是新的开发模式，也不是让 AI 无限改代码；它只负责维护一轮 batch 的状态、账本和 gate，并在安全边界内反复推进。

## 核心模型

一轮 loop 的边界是 batch，不是单次 `code-scan`：

```text
batch-code-scan
  -> batch-index
  -> 按顺序串行处理候选 Plan
  -> gated 时暂停当前 batch，等待人类批准/确认当前 Plan
  -> 所有 Plan complete
  -> 代码状态固化后生成 batch report
  -> 下一轮 loop 再基于最新代码执行新的 batch-code-scan
```

不要在 batch 内反复全量扫描项目。只有当前 batch 的所有 Plan 都已 `complete`，且实现、审计、提交或用户指定的固化策略完成后，才允许开始下一轮 `batch-code-scan`。`gated` 或 `blocked` 不是 batch 结束状态；它们只表示当前 batch 还有事项不能自动解决。

## 账本文件

所有 loop 运行状态写入当前项目：

```text
docs/human-plans/.loop/
  state.json
  batch-index.md
  run-log.md
  gates.md
  changelog.md
  token-ledger.md
  batches/
  STOP
```

字段和含义：

- `state.json`：runner 状态、Batch ID、`batch_status`、max ticks、used ticks、active Plan、token 估算、最近错误。
- `batch-index.md`：本轮 batch 的扫描范围、候选 Plan、优先级、状态、依赖和串行处理顺序。
- `run-log.md`：每个 tick 实际做了什么。
- `gates.md`：等待人的事项，包含 Plan Ref、原因和精确命令。
- `changelog.md`：本轮已经解决的问题、改动范围、验证结果和剩余风险。
- `token-ledger.md`：每个 tick 的 input/output/total token 估算或真实 usage。
- `batches/<Batch ID>.md`：batch 全部解决后归档，说明发现了什么、解决了什么、代码状态如何固化、下一轮扫描基线是什么。
- `STOP`：runner 检测到该文件后，在当前 tick 结束后停止。

AI 每做一个动作，都必须能回答三件事：这轮发现了什么、已经解决了什么、现在卡在哪里需要人做什么。

## 命令

### `/human-plan:loop start [max_ticks]`

启动本地 runner。`max_ticks` 是本次最多执行多少个 tick，缺省为 `3`。如果 Claude Code 允许执行 shell，直接运行：

```bash
node plugins/human-plan/loop/runner.js start <max_ticks>
```

如果当前项目没有这个脚本，停止并提示安装或更新 `human-plan` plugin。

### `/human-plan:loop tick`

执行一个 loop tick。tick 必须是幂等的：读取 `.loop/state.json`、`.loop/batch-index.md` 和当前 git 状态，然后只推进一个明确动作。

按顺序决策：

1. 如果存在 `.loop/STOP`，记录停止并返回。
2. 如果没有 active batch，或 `state.json.batch_status` 为 `ready-for-scan`，运行 `/human-plan:batch-code-scan` 创建新 batch，并把 `batch_status` 设为 `active`。
3. 如果存在 active batch 且 `state.json.active_plan_ref` 指向未 `complete` 的 Plan，继续推进这个 Plan；如果 active batch 缺少 `active_plan_ref`，先从 `gates.md` 的当前 gate、`batch-index.md` 中的 `gated`/`blocked` 当前项、或最近 run-log 里的当前 Plan 恢复 active Plan；只有确认不存在未完成 active Plan 时，才按 `batch-index.md` 顺序选择第一个 `pending` 且依赖满足的 Plan，并写入 `state.json.active_plan_ref`。
4. 对 active Plan 自动推进：`dev` 或 `bug-fix` -> `plan-check` -> `design-check` -> `approve gate`。
5. 已到 `approve`、`confirm`、人类决策、版本冲突或前置条件不满足时，把事项写入 `gates.md`，把该 Plan 标为 `gated`，保持它为 active Plan，并暂停当前 batch；不得跳过它去处理后续 pending Plan。
6. 如果 Plan 已经 approve 并实现，自动进入 `audit`；audit 通过则标为 `complete`，清除 `state.json.active_plan_ref` 后，下一个 tick 才能选择后续 Plan；audit 返工且无需人类决策则继续返工链路，audit 需要人类决策则标为 `gated`。
7. 如果当前 batch 所有 Plan 都是 `complete`，且代码状态已固化，生成 `batches/<Batch ID>.md`，更新 `changelog.md`，把 `batch_status` 设为 `archived`，并清除 `state.json.active_plan_ref`；下一轮 loop 才能分配新 Batch ID，并基于最新代码重新执行 `batch-code-scan`。
8. 如果 active Plan 是 `gated` 或 `blocked`，只汇总 `gates.md` 和阻塞原因，保持当前 batch active，不得处理后续 Plan，不得归档，也不得开始下一轮扫描。

每个 tick 最多处理一个 Plan 的一个推进片段，避免一次调用无限展开。

batch 内 Plan 必须串行推进。选择 Plan 时只能在没有 active Plan，或 active Plan 已 `complete` 并已清除 `state.json.active_plan_ref` 后，才选择下一个 `pending` 且依赖满足的 Plan。某个 Plan 到达 approve/confirm gate 后，整个 batch 暂停在这个 Plan；不得跳过 gated Plan 去推进后续 pending Plan。遇到旧账本缺少 `active_plan_ref` 时，必须先恢复当前 gated/blocked Plan，不能直接选择后续 pending Plan。

tick 输出必须区分两类停止：

- **人工 gate**：active Plan 需要用户输入精确 `approve` / `confirm` / `replan`，写入 `gates.md`，并暂停当前 batch；后续 Plan 仍保持 pending。
- **runner 配额结束**：`max_ticks` 用尽时只说明本次 runner 停止；如果 active Plan 未 complete，明确写“下一次 `/human-plan:loop start <N>` 会继续当前 active Plan”，不得写成“跳过当前 gated Plan 继续下一个 pending Plan”。
- **batch 完成**：只有所有 Plan 都 `complete` 且代码状态已固化时才归档；归档后下一轮 loop 才重新 `batch-code-scan`，扫描最新代码。

### `/human-plan:loop status`

读取并展示 `state.json`、`batch-index.md` 摘要、`gates.md` 摘要和 `token-ledger.md` totals。不得扫描项目或改源码。

### `/human-plan:loop stop`

创建 `docs/human-plans/.loop/STOP`，并把 `state.json.status` 设为 `stopping`。不得删除已有账本。

## 自动与停止边界

loop 可以自动做：

- `batch-code-scan`
- 选择或继续 batch 中的 active Plan
- 生成或更新 Plan
- `dev` / `bug-fix` 规划
- `plan-check`
- `design-check`
- `audit`
- 无需人类决策的 replan / audit replan
- 账本、gate、changelog、batch 完成报告维护

loop 必须停止或挂当前 Plan 的 gate：

- `approve` 前
- `confirm` 前
- 需要业务、产品、合规、数据口径或破坏性变更决策
- Plan Ref 版本不匹配
- Owner/Status 前置条件不满足
- 连续失败、工作区异常、token 或 tick 达到上限
- 用户放置 `.loop/STOP`

不要因为一个 Plan gated 就结束 batch；把它写入 `gates.md` 后暂停当前 batch，等待人类处理这个 active Plan。

# Human Plan Protocol

所有 `human-plan` skill 都遵守本协议。各 skill 的 `SKILL.md` 只写本 skill 的专业职责、判断方法和命令差异；状态机、字段和确认规则以本文件为准。

## 输出语言

- 所有产出使用简体中文。
- 代码标识、路径、API 名称、组件名、命令、错误信息、仓库名、链接和必须保留的用户原文不翻译。
- 聊天输出只展示结论摘要、真实 Plan Ref、自动推进状态和人工输入要求，不重复完整 Plan。

## Plan 文件

- Human Plan 写入当前项目的 `docs/human-plans/`。
- Plan Ref 固定为 `<Plan 文件路径>@v<Version>`。
- 引用版本和当前 Version 不一致时停止且不写入，并返回当前真实 Plan Ref。
- 一个事项始终沿用同一个 Plan 文件和 Plan ID；只有无 Plan Ref 的新事项才创建文件。
- 固定字段必须保留：Plan ID、Version、Owner Skill、Status、Frontend Impact、Requirement Baseline、Confirmed Decisions、Current Plan、Changes Since Last Plan、Unchanged Scope、Needs Reconfirmation、Review Status、Delivery Status、Revision Notes。
- 不适用字段写 `无`；短状态字段不要展开成报告。
- Human Plan 是人类与 AI 的需求对齐凭据，不是聊天总结、调研报告、设计规范全文、审计报告、技术方案、任务清单或实现说明。

## Plan 内容标准

- Requirement Baseline 写人类要解决的问题、目标结果和已接受的来源基线。
- Confirmed Decisions 写人类已确认的业务、产品、体验、技术契约或修复取舍。
- Current Plan 写最终需求提示词：人类和 AI 已对齐后，AI 可按它执行。
- Unchanged Scope 写明确不做的事、不能顺手扩大的边界和兼容要求。
- Needs Reconfirmation 只写当前未解决的人类决策问题，不写分析过程或 replan 草稿。
- Changes Since Last Plan 只写本轮需求变化一句话，不保留多轮历史。
- Review Status、Delivery Status 和 Revision Notes 只写当前 Version 的短状态。
- Plan 只回答：为什么做、做成什么样、明确不做什么、怎么验收。
- 默认不写文件路径、函数名、行号、内部实现步骤、测试命令、搜索过程或技术排查过程；只有它们本身是用户要审核的契约时才保留。
- AI 后续执行时可自行推导技术步骤；这些步骤不写回 Human Plan，除非出现新的需求决策。

## 权限

- 除 `worktree` 外，未进入精确 `approve` 命令前，只允许读取项目并写入当前 Human Plan 或批次索引。
- `idea`、`design`、`code-scan`、`batch-code-scan`、`arch-check` 只产出 draft Plan，不修改源码。
- `dev`、`bug-fix`、`audit` 只有当前消息精确为对应 `approve <当前 Plan Ref>` 时才允许修改源码。
- 自然语言中的“好”“可以”“按这个做”“直接改”“修复”“实现”都不是 approve 或 confirm。
- 默认自动 loop：除非进入人工 gate、真实阻塞、流程完成、`worktree` 隔离准备，或手动 `batch-code-scan` 只建库存，当前 skill 完成后必须直接读取下一阶段 skill 的 `SKILL.md`，沿用同一个 Plan Ref 在同一会话继续执行，不要求用户复制下一步命令。
- 自动跳转只允许在 `idea/design/code-scan/arch-check -> dev -> plan-check -> design-check -> approval gate`、`loop 调用的 batch-code-scan -> dev -> plan-check -> design-check -> approval gate`、`手动 batch-code-scan 且用户明确要求继续推进 -> dev -> plan-check -> design-check -> approval gate`、`approve -> implementation -> audit`、`audit-fixes-required -> audit replan -> plan-check -> design-check -> approval gate` 这些协议路径内发生。
- 人工 gate 必须停止：Needs Reconfirmation 非空、Status 为 `reconfirmation-pending`、即将执行 `approve`、Plan Ref 版本不匹配、Owner/Status 前置条件不满足、需要人类业务/产品/合规/破坏性变更决策、或用户明确要求暂停。
- 到达人工 gate 时只输出：为什么停、真实 Plan Ref、必须由用户输入的精确 `confirm` / `approve` / `replan` 命令。不要继续尝试执行下一阶段。

## Reconfirmation

Needs Reconfirmation 非空时，`replan` 只能准备待提交 Replan，不能直接更新正式 Plan：

- 使用当前消息中的人类答复，不从更早对话猜测。
- 在 Needs Reconfirmation 中用短句保留人类问题、AI 理解和拟变更点。
- 不清除确认项，不修改正式 Plan，不增加 Version，不恢复检查状态。
- Status 设为 `reconfirmation-pending`，只展示待提交 Replan 的理解摘要和拟变更点后停止，等待用户精确 `confirm` 或继续 `replan`。

当前消息没有可用于对应确认项的答复时，不写入任何内容，只展示待确认事项，并要求用户用当前 Owner 的 `replan <当前 Plan Ref>` 补充答复。

只有当前消息精确为对应 Owner 的 `confirm <当前 Plan Ref>` 才能提交待提交 Replan。confirm 只提交 Replan，不代表开发、修复或返工批准。confirm 后若所有确认项已解决，继续按默认自动 loop 推进到下一检查阶段；若仍有未解决项，停止并要求继续 replan。

## Owner 与状态

- `idea`、`code-scan`、`batch-code-scan`、`arch-check`：Status 只使用 `draft` 或 `reconfirmation-pending`。
- `design`：Status 只使用 `review-pending`、`replan-required`、`reconfirmation-pending` 或 `draft`。
- `dev`、`bug-fix`：Status 只使用 `review-pending`、`replan-required`、`reconfirmation-pending`、`ready-for-approval` 或 `implemented`。
- `audit`：返工阶段 Status 只使用 `audit-fixes-required`、`review-pending`、`replan-required`、`reconfirmation-pending`、`ready-for-approval`、`implemented` 或 `complete`。
- Frontend Impact 只使用 `yes`、`no` 或 `unknown`；`design` 固定为 `yes`。
- 任一命令的 Owner、Status、Version 或前置条件不满足时停止且不写入，并根据当前 Plan 返回唯一合法人工输入或自动恢复路径。

## 检查与批准

- `plan-check` 通过后：Frontend Impact 为 `yes` 或 `unknown` 时自动进入 `design-check`；为 `no` 时记录 design-check 不适用，Status 设为 `ready-for-approval`，在对应 Owner 的 `approve` gate 停止。
- `design-check` 通过后：Owner 为 `design` 时 Status 设为 `draft` 并自动进入 `dev`；Owner 为 `dev`、`bug-fix` 或 `audit` 时 Status 设为 `ready-for-approval`，在对应 Owner 的 `approve` gate 停止。
- `approve` 前必须满足：Owner 与命令匹配、Status 为 `ready-for-approval`、Needs Reconfirmation 为空、当前 Version 的 plan-check 已通过、Frontend Impact 已明确，且前端影响为 `yes` 时当前 Version 的 design-check 已通过。
- `approve` 执行前再次核对 Requirement Baseline、Current Plan 和 Unchanged Scope。若实现需要新增决策、改变基线或扩大范围，停止写入，把决策点写入 Needs Reconfirmation，Status 设为 `replan-required`，返回 Owner 的 `replan`。
- `approve` 执行完成并写入 implementation 记录后，自动进入 `audit <当前 Plan Ref>`。
- `audit` 通过后 Status 设为 `complete` 并结束 loop；`audit` 发现返工且无需人类决策时，自动进入 `audit replan -> plan-check -> design-check -> audit approve gate`；需要人类决策时停止在 Reconfirmation gate。

## 后台批次 Loop

- 后台 loop 的入口是 `batch-code-scan`，不是反复执行 `code-scan`。
- 本节只约束 `/human-plan:loop` 驱动的后台批次；用户手动调用 `/human-plan:batch-code-scan` 时，它可以只建立库存并给出 worktree 分发建议，不必进入串行 loop。
- 一个 batch 内只做一次全量扫描，生成候选 Plan 库后按索引顺序串行推进；当前 batch 未全部解决并固化前不得重新全量扫描。
- 一个 batch 同一时间只能有一个 active Plan，并记录在 `.loop/state.json.active_plan_ref`。只有 active Plan `complete` 且该字段清除后，才能选择下一个 `pending` 且依赖满足的 Plan。
- 兼容旧账本：如果已有 active batch 但缺少 `active_plan_ref`，必须先从 `gates.md` 的当前 gate、`batch-index.md` 中的 `gated`/`blocked` 当前项、或最近 run-log 里的当前 Plan 恢复 active Plan；只有确认不存在未完成 active Plan 时，才按顺序选择第一个 `pending`。
- batch 生命周期必须记录在 `.loop/state.json.batch_status`：`ready-for-scan` 表示下一 tick 可创建新 batch，`active` 表示当前 batch 未结束，`archived` 表示本 batch 已全部解决并固化。
- 一个 Plan 到达 `approve`、`confirm`、人类决策或阻塞状态时，写入 `.loop/gates.md`，在批次索引中把该 Plan 标为 `gated` 或 `blocked`，并暂停当前 batch；不得跳过它处理后续 `pending` Plan。
- 只有一个 batch 的全部 Plan 都进入 `complete`，且代码状态已按用户策略固化后，才能生成 `.loop/batches/<Batch ID>.md` 归档，并把 `batch_status` 设为 `archived`；归档后的下一轮 loop 必须分配新 Batch ID，并基于最新代码重新执行 `batch-code-scan`。
- 如果 active Plan 是 `gated` 或 `blocked`，只能汇总等待事项并保持当前 batch active；不得归档，也不得启动下一轮 `batch-code-scan`。
- loop 必须维护 `.loop/state.json`、`.loop/batch-index.md`、`.loop/run-log.md`、`.loop/gates.md`、`.loop/changelog.md` 和 `.loop/token-ledger.md`。
- loop 必须尊重 `max_ticks`，达到次数后停止；不得为了完成 batch 而突破 tick 限制。`max_ticks` 用尽只代表本次 runner 配额结束，不是人工 gate；下一次 loop start/tick 必须保留并继续当前 active Plan，或在 active Plan 已 complete 后选择下一个 Plan。
- token 统计默认开启；拿不到 Claude CLI 真实 usage 时，按输入输出字符数做估算，并在 `token-ledger.md` 标记为 `estimated`。
- 用户创建 `.loop/STOP` 或执行 `/human-plan:loop stop` 后，runner 必须在当前 tick 结束后停止。

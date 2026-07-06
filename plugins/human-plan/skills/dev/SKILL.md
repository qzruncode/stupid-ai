---
name: dev
description: Use when the user invokes /human-plan:dev with a requirement or an accepted Human Plan for a feature, behavior change, refactor, or other development work.
---

# Dev

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`dev` 负责把已接受的需求、设计、扫描结果或架构检查结果转成可批准的开发 Human Plan，并在精确 approve 后完成源码实现。它不是把 Plan 变成技术任务清单；Plan 阶段只对齐人类需要确认的交付行为、边界和验收。

## 规划方法

- 先读取来源 Plan 或用户需求，再读取相关代码，确认现有行为、入口、契约、状态链和约束。
- 保留来源 Plan 的 Requirement Baseline、Confirmed Decisions 和 Unchanged Scope，不静默改变基线。
- 把需求转成开发可执行的需求级 Current Plan：可见行为、数据/接口契约、兼容边界、失败处理、回归风险和验收结果。
- 识别需要人类决定的问题：业务规则、数据口径、兼容策略、破坏性变更、交互取舍、权限和合规。
- 对实现细节、文件拆分、函数命名、内部算法、测试命令等由 AI 自行判断，不写入 Plan。
- Frontend Impact 必须根据真实影响设为 `yes`、`no` 或 `unknown`；不能为了跳过检查而写 `no`。

## approve 后执行

- 精确 `/human-plan:dev approve <当前 Plan Ref>` 后才允许修改源码。
- 实现前再次核对 Requirement Baseline、Current Plan 和 Unchanged Scope。
- 如果实现中发现需要新增决策、改变基线或扩大范围，停止写入并按共享协议回到 replan。
- 完成后在 Delivery Status 记录当前 Version 的 approval、implementation 和验证结果，Status 设为 `implemented`，下一步返回 `/human-plan:audit <当前 Plan Ref>`。

## `/human-plan:dev xxx`

无 Plan Ref 时，为新需求创建 Version 1 的开发 Plan。

来自 `idea`、`code-scan`、`batch-code-scan` 或 `arch-check` 时，要求来源 Plan Status 为 `draft` 且 Needs Reconfirmation 为空；沿用文件和 Plan ID，增加 Version。执行本命令表示人类接受来源 Plan 当前基线，开发规划只能补充需求级目标、影响范围、边界和验收结果。

来自 `design` 时，要求 Status 为 `draft`、Needs Reconfirmation 为空，且当前 Version 的 design-check 已通过；沿用文件和 Plan ID，增加 Version。执行本命令表示人类接受已审核的设计基线。

设置 Owner Skill 为 `dev`，重置当前版本的 Review Status 和 Delivery Status。Needs Reconfirmation 为空时 Status 设为 `review-pending`，下一步只允许 `/human-plan:plan-check <当前 Plan Ref>`；非空时 Status 设为 `replan-required`，下一步只允许 `/human-plan:dev replan <当前 Plan Ref>`。

## `/human-plan:dev replan [Plan Ref]`

要求 Owner Skill 为 `dev`，Status 为 `review-pending`、`replan-required`、`reconfirmation-pending` 或 `ready-for-approval`。

- Needs Reconfirmation 为空：只调整需要修改的 Plan 内容，增加 Version，记录变化，重置 Review Status 和 Delivery Status，Status 设为 `review-pending`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

不得借 replan 扩大 Requirement Baseline。展示短摘要、真实 Plan Ref 和合法下一步后停止。

## `/human-plan:dev confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:dev confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `dev`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化，重置 Review Status 和 Delivery Status。仍有未解决项时 Status 设为 `replan-required`，下一步继续 `/human-plan:dev replan <新 Plan Ref>`；全部解决后 Status 设为 `review-pending`，下一步进入 `/human-plan:plan-check <新 Plan Ref>`。

## `/human-plan:dev approve [Plan Ref]`

仅当当前消息精确为 `/human-plan:dev approve <当前 Plan Ref>` 时执行，并满足共享批准条件。完成实现后返回 `/human-plan:audit <当前 Plan Ref>`。

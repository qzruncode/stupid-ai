---
name: audit
description: Use when the user invokes /human-plan:audit or asks to review completed AI-written changes against the approved requirement, existing codebase, and engineering quality.
---

# Audit

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`audit` 负责审查已实现代码是否真正满足批准的 Human Plan，并判断实现质量是否足以结束闭环。它不是普通代码评审，也不是发现问题后顺手修；审计阶段只确认、记录阻塞问题，并在需要返工时生成返工 Plan。

## 审计方法

- 读取当前 Plan、Delivery Status、相关源码、差异、验证结果和必要运行证据。
- 对照 Requirement Baseline、Confirmed Decisions、Current Plan 和 Unchanged Scope，逐项判断是否交付、是否越界、是否遗漏。
- 检查正确性、边界、兼容性、回归、架构融入、抽象与重复、性能、交互、后端契约、数据一致性、安全、重试、超时、降级、可用性和必要验证。
- 区分阻塞问题、非阻塞观察和风格偏好。只把会影响需求一致性、质量或安全的阻塞问题写入 Plan。
- 如果需要返工，把 Owner Skill 设为 `audit`，将问题压缩成需求级返工范围，不写审计报告或逐文件修复步骤。
- 如果需要人类决策，把明确决策点写入 Needs Reconfirmation，不得替人作答。

## 通过标准

- 当前 Version 的批准需求全部实现。
- 没有违反 Unchanged Scope 或静默扩大范围。
- 验证结果与风险相称；关键路径有真实检查或可解释的人工确认。
- 代码融入现有结构，没有引入明显脆弱耦合、重复抽象或不可维护分叉。
- 前端变化满足已通过的 design-check；无明显状态、响应式、可访问性或交互回归。

## `/human-plan:audit [Plan Ref]`

要求 Status 为 `implemented`，且 Delivery Status 存在当前 Version 的 approval 和 implementation 记录。否则停止并返回当前合法下一步。

- 通过且 Needs Reconfirmation 为空：Status 设为 `complete`，记录当前 Version 的 Audit 通过，明确流程结束。
- 需要返工：Owner Skill 设为 `audit`，Status 设为 `audit-fixes-required`，记录阻塞问题和缺失验证，返回 `/human-plan:audit replan <当前 Plan Ref>`。
- 需要人类决策：同时把明确决策点写入 Needs Reconfirmation，后续必须经过 Audit Reconfirmation。

Needs Reconfirmation 非空时不得判定通过或设为 `complete`。只输出阻塞问题，不罗列无关小问题。

## `/human-plan:audit replan [Plan Ref]`

首次调用要求 Status 为 `audit-fixes-required`；后续要求 Owner Skill 为 `audit`，Status 为 `review-pending`、`replan-required`、`reconfirmation-pending` 或 `ready-for-approval`。

- Needs Reconfirmation 为空：把 Current Plan 更新为精简返工范围，增加 Version，记录变化，重置 Review Status 和 Delivery Status，Owner Skill 设为 `audit`、Status 设为 `review-pending`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

展示短摘要、真实 Plan Ref 和合法下一步后停止。普通 replan 下一步进入 `/human-plan:plan-check <当前 Plan Ref>`。

## `/human-plan:audit confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:audit confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `audit`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化，重置 Review Status 和 Delivery Status。仍有未解决项时 Status 设为 `replan-required`，下一步继续 `/human-plan:audit replan <新 Plan Ref>`；全部解决后 Status 设为 `review-pending`，下一步进入 `/human-plan:plan-check <新 Plan Ref>`。

## `/human-plan:audit approve [Plan Ref]`

仅当当前消息精确为 `/human-plan:audit approve <当前 Plan Ref>` 时执行，并满足共享批准条件。完成返工后 Status 设为 `implemented`，记录当前 Version 的 approval、implementation 和验证结果，返回 `/human-plan:audit <当前 Plan Ref>`。

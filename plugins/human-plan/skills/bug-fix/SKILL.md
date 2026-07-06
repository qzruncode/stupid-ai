---
name: bug-fix
description: Use when the user invokes /human-plan:bug-fix after a concrete bug and its affected behavior have already been identified.
---

# Bug Fix

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`bug-fix` 负责把已定位 bug 转成可批准的修复 Plan，并在精确 approve 后修复源码。它适合“问题已经明确”的场景；如果只是泛泛怀疑代码有风险，使用 `code-scan`。

## 修复规划方法

- 确认预期行为、实际异常、触发条件、影响范围、已知根因和回归风险。
- 区分根因、症状和相邻改进；Plan 只覆盖修复当前 bug 所需范围。
- 如果根因未成立或用户只提供现象，先通过读取代码验证，不要编造根因。
- 修复方向写成需求级结果：错的行为会怎样恢复、哪些边界保持兼容、如何验证不回归。
- 把需要人类决定的问题写入 Needs Reconfirmation：例如兼容旧错误数据、是否保留异常输入、是否改变用户可见文案。
- 不夹带重构、性能优化、UI 美化或其他事项。

## approve 后执行

- 精确 `/human-plan:bug-fix approve <当前 Plan Ref>` 后才允许修改源码。
- 实现前再次核对预期行为、异常行为、根因、Current Plan 和 Unchanged Scope。
- 若根因不成立、修复会扩大范围或需要新增决策，停止写入并回到 replan。
- 完成后在 Delivery Status 记录当前 Version 的 approval、implementation、根因和验证结果，Status 设为 `implemented`，下一步返回 `/human-plan:audit <当前 Plan Ref>`。

## `/human-plan:bug-fix xxx`

为已定位问题创建 Version 1 的 Human Plan。Owner Skill 设为 `bug-fix`，重置 Review Status 和 Delivery Status。

命令中出现已有 Plan Ref 时不得接管该 Plan；停止且根据其 Owner Skill 和 Status 返回合法下一步。

Needs Reconfirmation 为空时 Status 设为 `review-pending`，下一步只允许 `/human-plan:plan-check <当前 Plan Ref>`；非空时 Status 设为 `replan-required`，下一步只允许 `/human-plan:bug-fix replan <当前 Plan Ref>`。

## `/human-plan:bug-fix replan [Plan Ref]`

要求 Owner Skill 为 `bug-fix`，Status 为 `review-pending`、`replan-required`、`reconfirmation-pending` 或 `ready-for-approval`。

- Needs Reconfirmation 为空：只调整当前修复范围，增加 Version，记录变化，重置 Review Status 和 Delivery Status，Status 设为 `review-pending`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

不得改变预期行为或扩大事项范围。展示短摘要、真实 Plan Ref 和合法下一步后停止。

## `/human-plan:bug-fix confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:bug-fix confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `bug-fix`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化，重置 Review Status 和 Delivery Status。仍有未解决项时 Status 设为 `replan-required`，下一步继续 `/human-plan:bug-fix replan <新 Plan Ref>`；全部解决后 Status 设为 `review-pending`，下一步进入 `/human-plan:plan-check <新 Plan Ref>`。

## `/human-plan:bug-fix approve [Plan Ref]`

仅当当前消息精确为 `/human-plan:bug-fix approve <当前 Plan Ref>` 时执行，并满足共享批准条件。完成修复后返回 `/human-plan:audit <当前 Plan Ref>`。

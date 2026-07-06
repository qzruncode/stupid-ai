---
name: plan-check
description: Use when the user invokes /human-plan:plan-check or asks for architectural and code-impact review of a Human Plan before implementation.
---

# Plan Check

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`plan-check` 负责在实现前审查 Human Plan 是否能融入现有系统，并确认人类即将批准的内容足够清楚、边界足够稳。它不是字段格式检查器；要做真正的架构、代码影响和需求完整性评审。

Owner Skill 决定后续命令前缀：`dev` 对应 `/human-plan:dev`，`bug-fix` 对应 `/human-plan:bug-fix`，`audit` 对应 `/human-plan:audit`。

## 检查方法

- 先读取 Plan，再读取相关代码、接口、配置、状态流、数据模型和相邻模块。
- 检查 Requirement Baseline、Confirmed Decisions 和 Unchanged Scope 是否被保留，没有被 Current Plan 静默改变。
- 判断 Current Plan 是否是最终需求提示词，而不是技术方案、排查记录、任务清单或聊天摘要。
- 判断实现是否能融入现有代码结构：模块归属、已有抽象、复用边界、数据契约、状态流、错误处理和兼容层。
- 检查用户行为、业务边界、兼容性、性能、安全、可靠性、数据一致性和回归风险中需要人类决策的部分。
- 如果发现技术风险，只把需求层影响或需要人类决策的取舍写入 Plan，不要求 Plan 展开内部实现。
- 检查 Plan 是否一屏可审；如果长成报告或实现说明，要求对应 Owner replan 压缩。

## 阻塞标准

- 目标行为不清楚，无法判断交付是否完成。
- 范围边界不清楚，容易顺手改到无关事项。
- 与现有契约冲突，但 Plan 没有说明兼容策略。
- 涉及数据、安全、权限、迁移、破坏性变更或用户流程改变，但缺少人类决策。
- Current Plan 写了大量文件路径、函数名、步骤或测试命令，导致人类审核的不是需求而是 AI 的实现猜测。
- Frontend Impact 与实际影响不一致或仍为 `unknown` 且无法进入设计检查。

## `/human-plan:plan-check [Plan Ref]`

Plan Ref 必须匹配当前 Version，否则停止且不写入。

按以下顺序检查前置状态：

1. Owner Skill 必须是 `dev`、`bug-fix` 或 `audit`。
2. Status 为 `reconfirmation-pending` 时停止检查：理解正确返回对应 Owner 的 `confirm`，理解不正确返回对应 Owner 的 `replan`。
3. Needs Reconfirmation 非空时停止检查，返回对应 Owner 的 `replan`。
4. Status 必须是 `review-pending`，否则根据 Owner Skill 和 Status 返回当前合法下一步。

输出仅包含结论、阻塞问题、必须修改的 Plan 内容和需要人类决策的事项。通过时不重复完整 Plan。

## 结果

- 需要 AI 调整且无需人类决策：写入当前 Version 的 Review Status，把 Status 设为 `replan-required`，返回对应 Owner 的 `replan`。
- 需要人类决策：把明确决策点写入 Needs Reconfirmation，不得替人作答或只写在聊天中；Status 设为 `replan-required`，返回对应 Owner 的 `replan`。
- 通过且 Frontend Impact 为 `yes` 或 `unknown`：记录当前 Version 通过，Status 保持 `review-pending`，返回 `/human-plan:design-check <当前 Plan Ref>`。
- 通过且 Frontend Impact 为 `no`：记录 plan-check 通过和 design-check 不适用，Status 设为 `ready-for-approval`，返回对应 Owner 的 `approve`。

Review Status 必须绑定当前 Version，旧版本结果无效。展示结论、真实 Plan Ref 和完整下一步命令后停止。

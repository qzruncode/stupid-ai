---
name: batch-code-scan
description: Use when the user invokes /human-plan:batch-code-scan or asks to scan the whole current project once, build a complete inventory of actionable code risks, split all discovered problems into independent draft Human Plans, and let different sessions continue each plan through the normal dev, check, approve, and audit loop without repeated rescans.
---

# Batch Code Scan

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`batch-code-scan` 负责一次性建立当前项目的可行动问题库存，并把问题拆成多个可以独立推进的 draft Human Plan。它不是“找一个最严重问题”，也不是无限展开审计报告；重点是完整覆盖、清晰分组、避免重复扫描，让后续多个会话可以按 Plan 并行处理。

## 扫描策略

- 先建立覆盖面：主要目录、入口、页面、接口、数据流、状态管理、配置、构建、部署、脚本和关键依赖。
- 按风险类型扫描：正确性、数据一致性、兼容性、权限安全、性能、错误恢复、重试超时、缓存、并发、可维护性、重复抽象和前端体验风险。
- 不在发现一两个严重问题后停止；必须继续覆盖其他主要模块。
- 记录跳过范围和原因，避免库存被误认为全覆盖。
- 如果存在未完成批次索引，先读取并复用；除非用户明确要求刷新，或代码已在批次扫描后发生明显变化，不重新全量扫描。

## 问题库存

- 每个库存项必须有短标题、证据位置、严重级别、影响面和归属 Plan Ref。
- 严重级别按用户影响、数据风险、触达频率、恢复成本和修改确定性判断。
- 低优先级但真实可行动的问题也进入库存；无证据的猜测不进入库存。
- 批次索引只保存分发所需信息，不展开完整分析过程。

## 拆分 Plan

- 一个候选 Plan 只覆盖一个连贯修复范围。
- 共享根因、共享契约或必须一起改才有意义的问题可以合并。
- 无共同边界、可能并行处理的问题必须拆开。
- 会互相冲突、共享同一抽象或依赖前置改造的计划在索引中标为串行。
- 每个候选 Plan 只写问题价值、目标结果、边界、依赖和验收结果，不写实现步骤。

## 批次索引必须包含

- Batch ID、扫描范围和扫描时间。
- 扫描覆盖面、跳过项及原因。
- 完整问题库存。
- 每个候选 Plan 的标题、包含问题、严重级别、影响面、Plan Ref、是否适合并行。
- 计划之间的依赖、冲突和建议执行顺序。
- 下一步命令：单会话使用 `/human-plan:dev <Plan Ref>`；并行处理使用 `/human-plan:worktree <Plan Ref>`。

## `/human-plan:batch-code-scan`

创建或复用批次索引，并为所有可行动问题创建候选 Human Plan。每个候选 Plan 的 Owner Skill 设为 `batch-code-scan`，Status 设为 `draft`。

输出索引摘要、每个真实 Plan Ref、建议并行分组和下一步命令。并行分组里的每个 Plan 给出可直接复制的 `/human-plan:worktree <Plan Ref>`。随后停止。

## `/human-plan:batch-code-scan replan [Plan Ref]`

要求 Owner Skill 为 `batch-code-scan`，Status 为 `draft` 或 `reconfirmation-pending`。

- Needs Reconfirmation 为空：按人类反馈调整该候选 Plan 的优先级、范围、依赖、边界或验收结果，增加 Version，Status 保持 `draft`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

只更新当前 Plan；如需调整批次索引，只同步该 Plan 的标题、状态、Plan Ref、依赖、问题归属或并行建议。不重新扫描全项目。展示短摘要、真实 Plan Ref 和合法下一步后停止。

## `/human-plan:batch-code-scan confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:batch-code-scan confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `batch-code-scan`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化。仍有未解决项时 Status 设为 `draft`，下一步继续 `/human-plan:batch-code-scan replan <新 Plan Ref>`；全部解决后 Status 设为 `draft`，下一步进入 `/human-plan:dev <新 Plan Ref>`。

---
name: arch-check
description: Use when the user invokes /human-plan:arch-check or asks whether current business logic, product behavior, code, or architecture is reinventing wheels or diverging from mature solutions.
---

# Arch Check

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`arch-check` 负责判断当前业务、产品行为、代码结构或架构方案是否在重复造轮子、偏离成熟做法，或缺少行业常见的边界。它的产物不是外部调研报告，而是把成熟方案的启发压缩成一个可进入开发闭环的需求级 Plan。

## 研究方法

- 先读本地代码和产品行为，确认现有目标、真实约束、历史包袱、调用链和用户可见结果。
- 再查成熟方案：官方文档、主流框架实践、成熟开源项目、行业通用产品模式或协议约定。
- 只比较与当前决策有关的差异：能力边界、状态模型、错误恢复、扩展点、数据契约、权限、安全、可观测性、迁移和维护成本。
- 判断“成熟方案”是否真的适配当前项目；不要把大厂架构或流行库当成默认答案。
- 输出目标状态和关键取舍，而不是搜索过程、链接堆叠或改造步骤。

## 判断标准

- 当前方案是否用项目私有逻辑重做了已有稳定抽象。
- 当前行为是否违背用户熟悉的产品心智或平台约定。
- 当前架构是否把临时需求固化成长期耦合。
- 是否缺少成熟方案通常会保护的失败模式、兼容层、扩展边界或可观测性。
- 引入成熟方案的收益是否超过迁移成本和复杂度。

## 好的 Arch Check Plan

- Requirement Baseline 写清当前方案的问题价值和成熟方案启发。
- Confirmed Decisions 写保留、放弃或采纳的关键取舍。
- Current Plan 写目标状态、行为边界、兼容要求和验收结果。
- Unchanged Scope 明确不做平台化、全量迁移、重写或无关抽象。

## `/human-plan:arch-check`

识别当前方案与成熟方案的差距，创建 Version 1 的 Human Plan。Owner Skill 设为 `arch-check`，Status 设为 `draft`。

只展示短摘要、Status、Needs Reconfirmation 和真实 Plan Ref。无待确认事项时，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <当前 Plan Ref>` 继续推进；有待确认事项时，停止并只给出 `/human-plan:arch-check replan <当前 Plan Ref>`。

## `/human-plan:arch-check replan [Plan Ref]`

要求 Owner Skill 为 `arch-check`，Status 为 `draft` 或 `reconfirmation-pending`。

- Needs Reconfirmation 为空：按人类反馈调整目标状态、采用范围、成熟方案取舍或验收结果，增加 Version，Status 保持 `draft`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

不重复完整外部调研。展示短摘要和真实 Plan Ref。Needs Reconfirmation 为空时继续自动进入 `/human-plan:dev <当前 Plan Ref>`；Needs Reconfirmation 非空时按共享协议停止在 reconfirmation gate。

## `/human-plan:arch-check confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:arch-check confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `arch-check`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化。仍有未解决项时 Status 设为 `draft`，停止并要求 `/human-plan:arch-check replan <新 Plan Ref>`；全部解决后 Status 设为 `draft`，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <新 Plan Ref>` 继续推进。

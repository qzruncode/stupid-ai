---
name: design-check
description: Use when the user invokes /human-plan:design-check or a proposed frontend change needs senior UX/UI review for product fit, task flow, interaction model, visual system, responsive behavior, and usability before implementation.
---

# Design Check

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`design-check` 负责在实现前审查前端体验方案是否足够专业、完整、可用和可验收。它不是美观打分；要检查用户任务、信息架构、交互模型、状态体验、响应式和可访问性是否真的能支撑需求。

Owner Skill 决定后续命令前缀：`design` 对应 `/human-plan:design`，`dev` 对应 `/human-plan:dev`，`bug-fix` 对应 `/human-plan:bug-fix`，`audit` 对应 `/human-plan:audit`。

## 检查方法

- 先读取 Plan，再读取相关页面、组件、路由、状态、样式系统和相似页面。
- 判断 Frontend Impact：为 `unknown` 时必须先判定 `yes` 或 `no`；确认无前端影响时可判定不适用。
- 检查体验目标、目标用户、核心任务、成功标准和产品类型是否清楚。
- 检查设计主张是否明确：优先什么、弱化什么、第一眼理解什么、关键操作如何完成。
- 检查信息架构、页面层级、核心路径、关键决策点、密度、扫描路径和阅读节奏。
- 检查交互模型、操作效率、状态反馈、错误恢复、快捷能力和感知性能。
- 检查 loading、empty、error、disabled、success、partial data、permission denied 和长内容状态。
- 检查桌面端、移动端、键盘、焦点、可访问性和文本溢出风险。
- 检查视觉系统方向、层级、对比、控件表达、品牌感和复用边界。
- 检查是否引入一次性 CSS、脆弱布局、重复组件、视觉混乱或和现有系统冲突的体验。

## 阻塞标准

- 人类无法从 Plan 判断用户会看到什么、如何操作、如何获得反馈、如何判断任务完成。
- Plan 只写“优化 UI”“更美观”“提升体验”，没有具体体验主张。
- 缺少关键状态、响应式、错误恢复或可访问性要求。
- 把现有视觉缺陷当成必须保留的约束，或无视现有组件能力和业务入口。
- Needs Reconfirmation 包含设计师可自行判断的普通体验选择；应要求 Owner replan 直接作出设计决策。

## `/human-plan:design-check [Plan Ref]`

Plan Ref 必须匹配当前 Version，否则停止且不写入。

按以下顺序检查前置状态：

1. Owner Skill 必须是 `design`、`dev`、`bug-fix` 或 `audit`。
2. Status 为 `reconfirmation-pending` 时停止检查：理解正确返回对应 Owner 的 `confirm`，理解不正确返回对应 Owner 的 `replan`。
3. Needs Reconfirmation 非空时停止检查，返回对应 Owner 的 `replan`。
4. Status 必须是 `review-pending`；Owner 为 `dev`、`bug-fix` 或 `audit` 时还要求当前 Version 的 plan-check 已通过。

输出仅包含结论、阻塞体验问题、必须修改的设计要求和需要人类决策的事项。

## 结果

- 需要 AI 调整且无需人类决策：记录当前 Version 结果，把 Status 设为 `replan-required`，直接读取对应 Owner 的 `SKILL.md` 并以 `<owner> replan <当前 Plan Ref>` 继续推进。
- 需要人类决策：把明确决策点写入 Needs Reconfirmation，不得替人作答或只写在聊天中；Status 设为 `replan-required`，停止并返回对应 Owner 的 `replan`。
- Owner 为 `design` 且通过：记录当前 Version 结果，Status 设为 `draft`，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <当前 Plan Ref>` 继续推进。
- Owner 为 `dev`、`bug-fix` 或 `audit` 且通过或不适用：记录当前 Version 结果，Status 设为 `ready-for-approval`，停止在对应 Owner 的 `approve` gate。

只有进入人工 gate 时才展示完整下一步命令；否则展示结论和真实 Plan Ref 后自动继续下一阶段。

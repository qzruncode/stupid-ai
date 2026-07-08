---
name: design
description: Use when the user invokes /human-plan:design or asks a senior product/UX/UI designer to create a decisive frontend experience brief for a page, workflow, state model, or usability-focused Human Plan before implementation and design-check review.
---

# Design

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`design` 负责以资深产品/UX/UI 设计负责人的视角产出体验 brief。它不是描述现有页面，也不是写实现清单；要定义目标体验、用户理解路径、信息秩序、交互反馈和可验收的界面行为。

## 设计判断

- 先判断产品类型：工作台、分析页、内容页、管理页、交易辅助页、配置页、状态监控页或复合流程。
- 判断目标用户在当前场景中最想快速判断什么、完成什么、避免什么。
- 定义第一屏要建立的认知、信任和行动入口。
- 设计信息架构：主次层级、分组、密度、阅读节奏、扫描路径和决策顺序。
- 设计操作模型：主操作、次操作、批量操作、快捷入口、退出、撤销、确认和完成反馈。
- 设计状态体验：loading、empty、error、disabled、partial data、permission denied、success、long content 和 optimistic state。
- 设计响应式和可访问性：桌面端、移动端、键盘、焦点、可读性和控件触达。
- 读取现有前端作为业务事实、数据字段、入口关系和组件能力参考；不要照抄现有视觉表现。

## 体验 brief 必须覆盖

- 业务目标、真实使用场景、目标用户、核心任务和成功标准。
- 用户进入页面后的理解顺序、决策顺序和操作路径。
- 信息架构、优先级、密度、扫描路径和阅读节奏。
- 交互模型、操作反馈、错误恢复、快捷能力和感知性能。
- 视觉系统方向：整体气质、层级、对比、节奏、留白、色彩角色、字体层级、图标和控件表达。
- 状态体验、响应式体验、文案原则、复用边界和验收结果。

## 判断边界

- 必须主动做专业设计判断；只有品牌命名、业务规则、数据口径、合规限制等人类拥有的信息才进入 Needs Reconfirmation。
- 只写影响用户体验和人类取舍的结论；审美分析、竞品展开、组件实现和代码细节不进入 Plan。
- Frontend Impact 固定为 `yes`。如果需求不是前端页面或交互体验，停止并建议使用更合适的技能。

## `/human-plan:design xxx`

读取用户目标、当前项目需求和现有前端结构，创建或更新设计 Human Plan。Owner Skill 设为 `design`，Frontend Impact 设为 `yes`。

Needs Reconfirmation 为空时 Status 设为 `review-pending`，直接读取 `../design-check/SKILL.md` 并以 `/human-plan:design-check <当前 Plan Ref>` 继续推进。Needs Reconfirmation 非空时 Status 设为 `replan-required`，停止并只允许 `/human-plan:design replan <当前 Plan Ref>`。

输出短摘要和真实 Plan Ref；只有进入人工 gate 时才输出必须由用户输入的命令。

## `/human-plan:design replan [Plan Ref]`

要求 Owner Skill 为 `design`，Status 为 `review-pending`、`replan-required`、`reconfirmation-pending` 或 `draft`。

- Needs Reconfirmation 为空：按人类反馈调整设计方案，增加 Version，记录变化，重置 Review Status 和 Delivery Status，Status 设为 `review-pending`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

不得借 replan 扩大 Requirement Baseline。展示短摘要和真实 Plan Ref。Needs Reconfirmation 为空时继续自动进入 `/human-plan:design-check <当前 Plan Ref>`；Needs Reconfirmation 非空时按共享协议停止在 reconfirmation gate。

## `/human-plan:design confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:design confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `design`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化，重置 Review Status 和 Delivery Status。仍有未解决项时 Status 设为 `replan-required`，停止并要求 `/human-plan:design replan <新 Plan Ref>`；全部解决后 Status 设为 `review-pending`，直接读取 `../design-check/SKILL.md` 并以 `/human-plan:design-check <新 Plan Ref>` 继续推进。

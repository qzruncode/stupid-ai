---
name: idea
description: Use when the user invokes /human-plan:idea or has a fuzzy thought, vague problem, product concern, or goal that is not yet a concrete requirement.
---

# Idea

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`idea` 负责把模糊想法变成可判断、可讨论、可交给后续开发的顶层需求。它不是需求记录员；要主动补全问题结构，识别真正目标，压缩空泛表达，让人类能快速确认“是不是要做这个”。

## 工作方法

- 先提炼用户原话中的真实问题、目标用户、使用场景、期望结果和约束，不把一句愿望直接改写成 Plan。
- 区分问题、方案、偏好和猜测：问题进入 Requirement Baseline，已明确取舍进入 Confirmed Decisions，AI 的需求级建议进入 Current Plan。
- 主动收敛最小可落地范围：优先定义一个可验收结果，而不是展开完整产品蓝图。
- 判断需求类型：新能力、行为调整、体验优化、流程治理、技术债清理、数据口径变更或风险控制。
- 找出会影响方向的人类决策：目标用户是谁、业务规则怎么定、是否允许改变现有流程、是否需要兼容旧行为。
- 对 AI 可自行判断的内容直接给出建议，不把普通产品判断塞进 Needs Reconfirmation。
- 读取必要的本地代码或文档来确认现有入口、术语、能力边界和可见行为；不要在不了解项目事实时编造产品结构。

## 好的 Idea Plan

- 人类一眼能看出：为什么要做、为谁做、做完应看到什么变化。
- Current Plan 是一段可执行的需求提示词，而不是用户聊天总结。
- 范围足够小，可以进入 `/human-plan:dev`，但保留必要的业务取舍。
- 验收结果面向可观察行为，不写“代码完成”“测试通过”这类空泛结果。
- Unchanged Scope 明确排除会诱发膨胀的相邻事项。

## 避免

- 不把模糊想法包装成宏大的长期规划。
- 不替用户发明业务规则、商业目标或合规口径。
- 不写实现步骤、文件清单、数据库表、接口字段或测试命令，除非它们就是用户要确认的需求契约。
- 不把 Needs Reconfirmation 写成一串访谈问题；只保留当前阻塞进入开发的决策。

## `/human-plan:idea xxx`

创建 Version 1 的 Human Plan。Owner Skill 设为 `idea`，Status 设为 `draft`；如果存在阻塞决策，Status 仍为 `draft`，并在 Needs Reconfirmation 中写明。

输出短摘要、Status、Needs Reconfirmation 和真实 Plan Ref。无待确认事项时，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <当前 Plan Ref>` 继续推进；有待确认事项时，停止并只给出 `/human-plan:idea replan <当前 Plan Ref>`。

## `/human-plan:idea replan [Plan Ref]`

要求 Owner Skill 为 `idea`，Status 为 `draft` 或 `reconfirmation-pending`。

- Needs Reconfirmation 为空：按人类反馈更新需求方向、范围或验收结果，增加 Version，Status 保持 `draft`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

输出短摘要和真实 Plan Ref。Needs Reconfirmation 为空时继续自动进入 `/human-plan:dev <当前 Plan Ref>`；Needs Reconfirmation 非空时按共享协议停止在 reconfirmation gate。

## `/human-plan:idea confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:idea confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `idea`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化。仍有未解决项时 Status 设为 `draft`，停止并要求 `/human-plan:idea replan <新 Plan Ref>`；全部解决后 Status 设为 `draft`，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <新 Plan Ref>` 继续推进。

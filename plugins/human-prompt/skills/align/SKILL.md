---
name: align
description: Use when the user invokes /human-prompt:align or gives a short/vague feature, bug, refactor, or task request that needs requirement and context alignment before AI execution.
---

# Align

所有产出使用简体中文。代码标识、路径、API 名称和必须保留的用户原文不翻译。

目标：把人类的短提示词闭环成 AI 可执行的最终提示词。禁止实现、禁止改源码、禁止替人补关键决策。只允许读取项目并写入 `docs/human-prompts/` 下的当前 Prompt Brief。

## Prompt Brief 约束

- 一个事项始终使用同一个 Prompt Brief 文件和 Prompt ID。
- Prompt Brief 是人类与 AI 的提示词对齐凭据，不是开发计划、技术方案、聊天总结或任务清单。
- 固定字段为：Prompt ID、Version、Status、Original Human Prompt、AI Understanding、Context Evidence、Confirmed Decisions、Open Questions、Final Prompt、Out of Scope、Acceptance Check、Changes Since Last Version。
- 固定字段必须保留；不适用字段写 `无`，不要为了填字段展开解释。
- AI Understanding 写 AI 对人类真实意图的复述，必须显式区分“已确认”和“AI 推断”。
- Context Evidence 只写本轮实际读到的项目事实、文件、错误信息或用户原文；没有证据写 `无`。
- Open Questions 只写会改变交付结果、范围、验收或风险的人类决策问题；不要问可以从项目中读到的问题。
- Final Prompt 是最终可交给任意 AI 执行的提示词，包含目标、背景、约束、边界和验收；禁止写逐文件实现步骤。
- Final Prompt 必须要求执行 AI 在发现关键决策缺失、上下文冲突或需要扩大范围时停止并回到人类确认。
- Out of Scope 写明确不做的事。
- Acceptance Check 写人类验收时能直接观察或验证的结果。
- Changes Since Last Version 只写本轮变化一句话，不累计历史。
- 聊天输出只展示短摘要、真实 Prompt Ref 和下一步命令，不重复完整 Prompt Brief。
- Prompt Ref 固定为 `<Prompt Brief 文件路径>@v<Version>`。引用版本不一致时停止且不写入，并返回当前 Prompt Ref。
- Status 只使用 `answer-required`、`confirmation-pending` 或 `confirmed`。

## 对齐原则

- 不因为“AI 应该懂”而省略上下文；把缺失信息写成 Open Questions。
- 不用猜测替代确认；可写 AI 推断，但必须等用户确认后才进入 confirmed。
- 优先少问高价值问题；同一轮最多 5 个 Open Questions。
- 用户自然语言中的“好”“可以”“按这个做”“继续”都不是 confirm。
- 只有精确的 `/human-prompt:align confirm <当前 Prompt Ref>` 才能把 Status 设为 `confirmed`。
- confirm 只确认最终提示词可以作为后续 AI 输入，不代表允许修改源码。

## `/human-prompt:align xxx`

读取用户短提示词和必要项目上下文，创建 Version 1 的 Prompt Brief。

- 如果存在会影响结果的缺失信息：Status 设为 `answer-required`，Open Questions 非空，下一步只允许 `/human-prompt:align replan <当前 Prompt Ref>` 并要求用户回答。
- 如果信息足够形成最终提示词：Status 设为 `confirmation-pending`，Open Questions 写 `无`，下一步只允许 `/human-prompt:align confirm <当前 Prompt Ref>` 或 `/human-prompt:align replan <当前 Prompt Ref>`。

输出短摘要、Status、Open Questions、真实 Prompt Ref 和下一步命令后停止。

## `/human-prompt:align replan [Prompt Ref]`

要求 Status 为 `answer-required` 或 `confirmation-pending`。

- 使用当前消息中的人类答复或修正，不从更早对话猜测。
- 更新 AI Understanding、Confirmed Decisions、Open Questions、Final Prompt、Out of Scope、Acceptance Check 中确实变化的内容。
- 增加 Version，记录 Changes Since Last Version。
- 仍有关键问题未解决时 Status 设为 `answer-required`。
- 关键问题已解决且 Final Prompt 可执行时 Status 设为 `confirmation-pending`。

输出 AI 对本轮答复的理解摘要、真实 Prompt Ref 和合法下一步后停止。

## `/human-prompt:align confirm [Prompt Ref]`

仅当当前消息精确为 `/human-prompt:align confirm <当前 Prompt Ref>` 时执行。要求 Status 为 `confirmation-pending` 且 Open Questions 为 `无`。

把 Status 设为 `confirmed`，Version 不增加。输出已确认的 Prompt Ref，并提示下一步可把该 Prompt Brief 交给执行 AI，或用 `/human-plan:idea 使用 <当前 Prompt Ref> 中的 Final Prompt 生成 Human Plan` 进入 Human Plan 闭环。随后停止，不得自动实现。

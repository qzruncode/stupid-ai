---
name: align
description: Use when the user invokes /human-prompt:align or gives a short/vague task request that should become an aligned prompt before any AI starts work.
---

# Align

所有产出使用简体中文。代码标识、路径、API 名称和必须保留的用户原文不翻译。

这个 skill 只做 prompt 对齐：读懂人类短请求，复述理解，必要时让人类修正，最后产出一段可交给执行 AI 的 Prompt。禁止实现，禁止写开发计划，禁止修改源码。

只允许写当前 `docs/human-prompts/` Prompt Brief。

## Prompt Brief

Prompt Brief 只保留：

```md
# <短标题>

- Prompt ID: <id>
- Version: <n>
- Status: aligning | confirmed | approved

## Human
<用户原文或等价短句>

## Understanding
<AI 对用户真实意图的复述>

## Need Human
<需要用户修正或补充的关键点；没有就写 无>

## Prompt
<交给执行 AI 的最终提示词；未对齐前写 待确认>
```

不要写代码调查报告、文件清单、行号、代码片段、实现步骤、验收长清单、历史记录。

## 命令

`/human-prompt:align <短请求>`

创建或复用 Prompt Brief，Status 设为 `aligning`。如果理解已经明确，写出 Prompt；如果不明确，Prompt 写 `待确认`，Need Human 写需要用户修正或补充的点。输出 Prompt Ref 和下一步：`confirm` 或 `realign`。

`/human-prompt:align realign <Prompt Ref> <用户修正或补充>`

根据当前消息更新 Understanding、Need Human 和 Prompt，Version 增加，Status 保持 `aligning`。输出 Prompt Ref 和下一步：`confirm` 或继续 `realign`。

`/human-prompt:align confirm <Prompt Ref>`

只有当前消息精确匹配该命令才执行。表示用户确认 AI 的理解和 Prompt 正确。要求 Status 为 `aligning` 且 Need Human 为 `无`。执行后 Status 设为 `confirmed`，Version 不增加。输出下一步：`approve` 或 `realign`。

`/human-prompt:align approve <Prompt Ref>`

只有当前消息精确匹配该命令才执行。表示用户批准这段 Prompt 可以交给后续执行 AI。要求 Status 为 `confirmed`。执行后 Status 设为 `approved`，Version 不增加，并输出最终 Prompt Ref。

自然语言的“好”“可以”“继续”“按这个做”都不是 `confirm` 或 `approve`。

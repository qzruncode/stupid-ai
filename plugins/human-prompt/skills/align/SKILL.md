---
name: align
description: Use when the user invokes /human-prompt:align or gives a short/vague feature, bug, refactor, or task request that should be aligned into an execution prompt before any AI starts work.
---

# Align

所有产出使用简体中文。代码标识、路径、API 名称和必须保留的用户原文不翻译。

这个 skill 只解决一件事：把人类的短请求变成执行 AI 能直接使用的提示词。不要实现，不要写开发计划，不要把调研过程写成文档。

只允许读取项目和写入当前 `docs/human-prompts/` Prompt Brief；禁止修改源码。

## Prompt Brief

Prompt Brief 不是需求文档，也不是代码审计报告。它只保留对齐所必需的信息：

```md
# <短标题>

- Prompt ID: <id>
- Version: <n>
- Status: needs-answer | ready | confirmed

## Human
<用户原文或等价短句>

## Understanding
<AI 对真实意图的复述；只写会影响执行结果的理解>

## Need Human
<仍需要人类补充或确认的关键缺口；没有就写 无>

## Prompt
<确认后交给执行 AI 的最终提示词>
```

不要在 Brief 里写这些东西：文件清单、行号、代码片段、上下文证据、AI 推断列表、实现步骤、验收长清单、历史记录、排查过程、风险报告。

如果某个路径、字段名、接口名或错误信息是用户原文的一部分，或不写会导致执行 AI 明显做错，可以写进 `Prompt`；否则留给执行 AI 自己读代码。

`Prompt` 要像人类本来应该写给 AI 的那段话：目标、关键背景、明确边界、遇到不确定时回到人类确认。不要把它拆成一堆报告字段。

## 命令

`/human-prompt:align <短请求>`

- 创建或复用一个 Prompt Brief。
- 如果信息明显不够执行，把 Status 设为 `needs-answer`，`Need Human` 写需要人类补充的关键缺口，`Prompt` 写 `待确认`。
- 如果已经足够执行，把 Status 设为 `ready`，`Need Human` 写 `无`，`Prompt` 写最终提示词。
- 输出只给摘要、Prompt Ref 和下一步命令。

`/human-prompt:align replan <Prompt Ref> <人类补充或修正>`

- 只根据当前消息更新 Brief，不从旧对话补脑。
- 仍缺关键上下文则保持 `needs-answer`；已经能执行则设为 `ready`。
- Version 增加。
- 输出只给更新后的理解、Prompt Ref 和下一步命令。

`/human-prompt:align confirm <Prompt Ref>`

- 只有当前消息精确匹配该命令才执行。
- 要求 Status 为 `ready` 且 `Need Human` 为 `无`。
- 把 Status 设为 `confirmed`，Version 不增加。
- confirm 只表示这个 Prompt 可以交给后续 AI，不表示批准改源码。

自然语言的“好”“可以”“继续”“按这个做”都不是 confirm。

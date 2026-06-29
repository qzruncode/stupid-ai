# human-prompt

> A prompt-alignment loop for Claude Code. Part of the [stupid-ai](../../) marketplace.

## 这是什么

`human-prompt` 解决的是“人类提示词太短，AI 没理解就开干”的问题。它不做实现，也不产出开发计划；它只把人类的一句话变成一段可确认、可批准的最终 Prompt。

核心路线：

```
align -> realign -> confirm -> approve
```

## Skills

| Skill | 作用 |
|-------|------|
| `/human-prompt:align` | 把短需求、短 bug 描述或模糊任务闭环成已批准的最终 Prompt |

## 使用

```
/plugin marketplace add qzruncode/stupid-ai
/plugin install human-prompt@stupid-ai
```

本地开发/测试：

```
/plugin marketplace add /path/to/stupid-ai
/plugin install human-prompt@stupid-ai
```

示例：

```
/human-prompt:align 帮我实现收藏功能
/human-prompt:align realign docs/human-prompts/favorite-feature.md@v1 用户只能收藏文章，列表页和详情页都要显示状态
/human-prompt:align confirm docs/human-prompts/favorite-feature.md@v2
/human-prompt:align approve docs/human-prompts/favorite-feature.md@v2
```

## 约定

- Prompt Brief 写在项目内 `docs/human-prompts/` 下，只保留 `Human`、`Understanding`、`Need Human`、`Prompt`
- Prompt Ref 格式：`<Prompt Brief 文件路径>@v<Version>`
- `confirm` 确认 AI 理解正确，`approve` 批准 Prompt 可以交给后续执行 AI
- 自然语言的“好/可以/继续/按这个做”不算 `confirm` 或 `approve`
- 文件清单、代码片段、调研证据、实现步骤和长篇验收不要写进 Prompt Brief

## 结构

```
plugins/human-prompt/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── align/
│       ├── SKILL.md
│       └── agents/openai.yaml
└── README.md
```

## License

MIT © yejiawei

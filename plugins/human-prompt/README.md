# human-prompt

> A prompt-alignment loop for Claude Code. Part of the [stupid-ai](../../) marketplace.

## 这是什么

`human-prompt` 解决的是“人类提示词太短，AI 没理解就开干”的问题。它不做实现，也不产出开发计划；它只把人类的一句话变成一段可确认的最终提示词，缺信息就先问，确认后再交给后续 AI 执行。

核心路线：

```
align -> replan -> confirm -> human-plan / 任意执行 AI
```

## Skills

| Skill | 作用 |
|-------|------|
| `/human-prompt:align` | 把短需求、短 bug 描述或模糊任务闭环成已确认的最终提示词 |

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
/human-prompt:align replan docs/human-prompts/favorite-feature.md@v1 用户只能收藏文章，列表页和详情页都要显示状态
/human-prompt:align confirm docs/human-prompts/favorite-feature.md@v2
/human-plan:idea 使用 docs/human-prompts/favorite-feature.md@v2 中的 Final Prompt 生成 Human Plan
```

## 约定

- Prompt Brief 写在项目内 `docs/human-prompts/` 下，只保留 `Human`、`Understanding`、`Need Human`、`Prompt`
- Prompt Ref 格式：`<Prompt Brief 文件路径>@v<Version>`
- `confirm` 只确认最终提示词，不批准改源码
- 自然语言的“好/可以/继续/按这个做”不算确认
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

# stupid-ai

> A Claude Code plugin marketplace. We trust LLMs less than we trust a written plan a human can read.

为什么叫"愚蠢 AI"？因为我们相信：与其信任 LLM 一次到位，不如把开发流程切成一个个**人类可审核的 Plan**，让 AI 在每一步都先写计划、等人确认、再动手。AI 越"蠢"，流程越稳。

## Plugins

| Plugin | 作用 |
|--------|------|
| [human-plan-flow](./plugins/human-plan-flow) | Human-Plan-driven 开发工作流：idea → design → design-check → plan-check → worktree → dev → bug-fix → audit，加 arch-check / code-scan / batch-code-scan 持续健康度扫描 |

## 安装 marketplace

```
/plugin marketplace add yejiawei/stupid-ai
```

然后装其中的 plugin：

```
/plugin install human-plan-flow@stupid-ai
```

本地开发/测试：

```
/plugin marketplace add /path/to/stupid-ai
/plugin install human-plan-flow@stupid-ai
```

## 结构

```
stupid-ai/                              # marketplace 仓库
├── .claude-plugin/
│   └── marketplace.json                # marketplace 清单，列出所有 plugin
├── plugins/
│   └── human-plan-flow/                # 单个 plugin（有自己的 README）
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       └── README.md
├── LICENSE
└── README.md                           # 本文件（marketplace 层）
```

## 加新 plugin

1. 在 `plugins/<new-plugin-name>/` 下建目录，按 plugin 规范放 `.claude-plugin/plugin.json` + `skills/` 等
2. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组追加一条：
   ```json
   {
     "name": "<new-plugin-name>",
     "source": "./plugins/<new-plugin-name>",
     "description": "..."
   }
   ```
3. 跑 `claude plugin validate .` 确认 marketplace 通过
4. 给新 plugin 写自己的 `README.md`（参考 `plugins/human-plan-flow/README.md`）

## License

MIT © yejiawei

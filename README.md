# stupid-ai

> A Claude Code plugin marketplace for Human Prompt and Human Plan gated AI development.

`stupid-ai` 不追求让 AI 一口气把代码写完，而是把 AI 开发拆成可审核、可回滚、可复用的 Human Prompt / Human Plan 流程。短提示词先被对齐成最终执行提示词；动代码前，AI 必须先把需求说清楚；每次有疑问，AI 必须先复述理解并等人确认；每次实现后，再用 audit 把代码拉回已批准的需求。

它解决的是纯 AI 项目里最常见的几个坑：短提示词没对齐、需求漂移、越改越乱、直接动代码、重复扫描浪费 token、前端越改越丑、多个修复互相串分支。

## Plugins

| Plugin | 作用 |
|--------|------|
| [human-plan](./plugins/human-plan) | Human Plan 驱动的 AI 开发闭环：idea / design / scan 产出顶层需求，dev 执行前必须 plan-check + design-check，approve 后才写代码，audit 负责验收和返工 |
| [human-prompt](./plugins/human-prompt) | Human Prompt 对齐闭环：把人类的一句话短需求变成已批准的 Prompt Brief，作为后续执行上下文 |

## 特色

- **Human Plan 是最终提示词**：Plan 面向人类审核，只保留需求、边界、取舍和验收，不写逐文件实现清单。
- **Human Prompt 先对齐**：短需求先变成 Prompt Brief，AI 复述理解，用户 `confirm` 后再 `approve` 这份 Brief，并以它作为后续执行上下文。
- **硬确认门禁**：自然语言的“可以/按这个做”不算批准；在 `human-plan` 中只有 approve 才允许改源码。
- **不让需求漂移**：同一个事项始终沿用同一个 Plan Ref，所有 replan 都绑定版本、基线和未变范围。
- **设计和架构双检查**：`plan-check` 看系统影响和代码融入，`design-check` 看交互、视觉、状态和响应式体验。
- **批量扫描不重复烧 token**：`batch-code-scan` 一次扫完整项目，拆出多个独立 Plan，再用 worktree 并行推进。
- **一个 Plan 一个 worktree**：每个 Plan 创建独立分支和工作区，避免多个 AI 会话互相污染。

## 安装 marketplace

```
/plugin marketplace add qzruncode/stupid-ai
```

然后装其中的 plugin：

```
/plugin install human-plan@stupid-ai
/plugin install human-prompt@stupid-ai
```

本地开发/测试：

```
/plugin marketplace add /path/to/stupid-ai
/plugin install human-plan@stupid-ai
/plugin install human-prompt@stupid-ai
```

## 结构

```
stupid-ai/                              # marketplace 仓库
├── .claude-plugin/
│   └── marketplace.json                # marketplace 清单，列出所有 plugin
├── plugins/
│   ├── human-plan/                     # Human Plan 闭环 plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   └── README.md
│   └── human-prompt/                   # Human Prompt 对齐 plugin
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
4. 给新 plugin 写自己的 `README.md`（参考 `plugins/human-plan/README.md`）

## License

MIT © yejiawei

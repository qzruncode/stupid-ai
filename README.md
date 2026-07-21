# stupid-ai

> Claude Code plugins for AI work that should not drift: auto-loop plans, explicit human gates, and auditable execution.

`stupid-ai` 不追求让 AI “凭感觉一直写”。它把 Claude Code 的开发过程变成一条可读、可停、可审计的闭环：用户给一句诉求，插件自动整理 Human Plan、检查架构和设计、停在人工 approve gate；也可以启动后台 batch loop，让 AI 按次数上限扫描、推进、记账和挂 gate。

它解决的是纯 AI 项目里最常见的几个坑：短提示词没对齐、需求漂移、越改越乱、直接动代码、重复扫描浪费 token、前端越改越丑、多个修复互相串分支。

## Why Star

- **One request, one loop**：不用复制一串命令，`human-plan` 会自动推进到下一个安全阶段。
- **One batch, many plans**：后台 loop 默认先 `batch-code-scan`，再逐个处理 Plan，不反复全量扫描项目。
- **Only humans approve risk**：自然语言的“可以/按这个做”不算批准，只有精确 `approve` 才能改源码。
- **Plans stay readable**：Human Plan 只写需求、边界、取舍和验收，不把人类拖进逐文件实现清单。
- **Checks before code, audit after code**：动手前做 `plan-check` / `design-check`，实现后用 `audit` 拉回已批准需求。
- **Built for real repos**：支持 code scan、batch scan、worktree 隔离和返工闭环。
- **Govern the whole repo, not just one change**：`repo-guardian` 先用证据确认问题，再实际完成治理和验证，也能基于项目目标与当前生态决定下一步。

## Plugins

| Plugin | 作用 |
|--------|------|
| [human-plan](./plugins/human-plan) | 自动 loop 的 Human Plan 开发闭环：单诉求自动到 approve gate，后台 batch loop 可按 tick 上限扫描、推进、记录 gate 和 token |
| [human-prompt](./plugins/human-prompt) | Human Prompt 对齐闭环：把人类的一句话短需求变成已批准的 Prompt Brief，作为后续执行上下文 |
| [code-cleanup](./plugins/code-cleanup) | 先建立声明范围内完整的无代码功能基准，再以 100% 文件覆盖和持久批次计划系统清理业务迭代后越来越乱的实现 |
| [repo-guardian](./plugins/repo-guardian) | 独立的仓库治理插件：审计真实问题、完成并验证改进、决定项目下一步 |

## Human Plan Loop

```text
one request
  -> Human Plan
  -> plan-check
  -> design-check when needed
  -> approve gate
  -> implementation
  -> audit
  -> complete or rework gate

loop start 5
  -> batch-code-scan once
  -> process plans one by one
  -> gates / changelog / token-ledger
  -> stop after 5 ticks
```

## Functional Baseline & Cleanup

```text
/code-cleanup:feature-list [已确认的业务变化]
  -> 初始化、更新或核查唯一功能基准

/code-cleanup:cleanup [功能 ID 或范围]
  -> 全量技术扫描后，以 ready 基准持续执行全部清理批次
```

两个过程互不自动调用。功能清单不得包含任何代码或实现信息，未指定范围时必须覆盖完整产品，明确指定 CodeBench 等范围时则完整覆盖该范围。cleanup 未另传范围时继承清单范围，先建立逐文件清理计划并达到 100% 扫描覆盖，再连续处理全部候选；删一个文件不能代表系统清理完成。

## 特色

- **Human Plan 是最终提示词**：Plan 面向人类审核，只保留需求、边界、取舍和验收，不写逐文件实现清单。
- **Human Prompt 先对齐**：短需求先变成 Prompt Brief，AI 复述理解，用户 `confirm` 后再 `approve` 这份 Brief，并以它作为后续执行上下文。
- **自动推进，人工门禁**：无风险阶段自动继续；遇到 `confirm`、`approve`、版本不匹配或人类决策才停止。
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
/plugin install code-cleanup@stupid-ai
/plugin install repo-guardian@stupid-ai
```

最短使用方式：

```text
/human-plan:idea 我想把搜索体验改到用户一眼知道结果是否可靠

# 插件自动推进到 approve gate 后，再由用户显式批准：
/human-plan:dev approve docs/human-plans/search-revamp.md@v3
```

仓库治理（独立插件，不进入 `human-plan` loop）：

```text
# 全面或定向审计，只报告有证据的问题
/repo-guardian:audit

# 只看项目下一步该做什么
/repo-guardian:roadmap

# 直接完成一个已确认问题的治理并验证结果
/repo-guardian:improve RG-003
```

后台循环：

```bash
node plugins/human-plan/loop/runner.js start 5
```

本地开发/测试：

```
/plugin marketplace add /path/to/stupid-ai
/plugin install human-plan@stupid-ai
/plugin install human-prompt@stupid-ai
/plugin install code-cleanup@stupid-ai
/plugin install repo-guardian@stupid-ai
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
│   ├── human-prompt/                   # Human Prompt 对齐 plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   └── README.md
│   ├── code-cleanup/                   # 功能基准与 cleanup 分离 plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   └── README.md
│   └── repo-guardian/                  # 独立仓库治理 plugin
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

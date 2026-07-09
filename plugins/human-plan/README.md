# human-plan

> One request in Claude Code, one Human Plan loop: auto-check what can be checked, stop only when a human must decide.

## 这是什么

`human-plan` 是一套 Human Plan 驱动的 AI 开发闭环。用户可以输入单个诉求，也可以启动后台 batch loop：先全量扫描出一批 Plan，再逐个推进、记录 gate、统计 token、归档 batch。AI 会自动做能做的检查和维护，到人工 approve / confirm / 决策时才停。Human Plan 写在项目内 `docs/human-plans/` 下，只保存人类要审核的需求、边界、取舍和验收，不写代码、不写逐文件步骤。

## 适合谁

- 你经常让 Claude Code 改真实项目，但怕需求漂移、越改越乱。
- 你希望 AI 自己跑完检查链路，但不允许它绕过人工批准直接改源码。
- 你要把模糊想法、bug、代码扫描结果或体验方案变成可审的交付凭据。
- 你想先扫出完整问题库存，再选择手动分发 worktree 或用 loop 串行治理。
- 你想让 AI 在后台循环处理一批问题，同时知道它解决了什么、卡在哪里、花了多少 token。

核心路线：

```
idea / code-scan / arch-check
  → dev → plan-check → design-check → dev approve gate → implement → audit

batch-code-scan
  → inventory / worktree suggestions
  → loop or explicit continue → dev → plan-check → design-check → dev approve gate → implement → audit

design → design-check → dev → plan-check → design-check → dev approve gate → implement → audit

bug-fix → plan-check → design-check → bug-fix approve gate → fix → audit

loop start N
  → batch-code-scan → batch-index
  → process plans one by one
  → gates / changelog / token-ledger
  → all plans complete
  → batch report
  → next loop scans latest code
```

所有下一步都由当前 Plan 的 Owner Skill、Status、Needs Reconfirmation 和 Version 决定。无人工 gate 时，当前 skill 会直接读取下一阶段 skill 的 `SKILL.md` 并在同一会话继续推进，不要求用户复制命令；任一步有待确认事项，都必须回到 Owner Skill replan，再由用户显式 confirm。到达 approve gate 时必须停止，只有精确 `/human-plan:<owner> approve <Plan Ref>` 才能改源码。

插件内部把共享状态机放在 `shared/human-plan-protocol.md`；每个 skill 的 `SKILL.md` 只保留自己的专业职责、判断方法、产出标准和命令差异，避免把 Human Plan 闭环写成空壳流程。

## Skills

| 类型 | Skill | 作用 |
|------|-------|------|
| 需求成形 | `/human-plan:idea` | 把模糊想法整理成可落地的顶层需求 Plan |
| 体验设计 | `/human-plan:design` | 资深 UX/UI 角色产出体验 brief Plan |
| 开发执行 | `/human-plan:dev <Plan Ref>` | 把已接受的 Plan 转成开发 Plan，并自动推进检查直到 approve gate |
| Bug 修复 | `/human-plan:bug-fix` | 已定位 bug 先写修复 Plan，再自动走检查到 approve gate |
| 架构检查 | `/human-plan:plan-check <Plan Ref>` | 检查需求是否能融入现有系统、代码结构和边界，通过后自动进入下一检查或 approve gate |
| 设计检查 | `/human-plan:design-check <Plan Ref>` | 检查交互、视觉、状态、响应式和可用性，通过后自动进入 dev 或 approve gate |
| 审计闭环 | `/human-plan:audit <Plan Ref>` | 对已实现代码做需求一致性和质量审计，通过后结束；返工无需人工决策时自动推进到下一 approve gate |
| 隔离执行 | `/human-plan:worktree <Plan Ref>` | 为一个 Plan 创建一个独立 worktree 和分支 |
| 持续扫描 | `/human-plan:code-scan` | 扫描当前项目，产出一个优先处理 Plan |
| 批量扫描 | `/human-plan:batch-code-scan` | 一次扫完整项目，拆出多个 Plan，可手动分发或交给 loop 串行推进 |
| 成熟方案 | `/human-plan:arch-check` | 检查业务/代码/架构是否在重复造轮子或偏离成熟方案 |
| 后台循环 | `/human-plan:loop start 5` | 一次 batch 扫描，多 Plan 按顺序串行推进；单个 Plan 到 gate 后暂停当前 batch |

## 安装

先加 marketplace，再装本 plugin：

```
/plugin marketplace add qzruncode/stupid-ai
/plugin install human-plan@stupid-ai
```

本地开发/测试：

```
/plugin marketplace add /path/to/stupid-ai
/plugin install human-plan@stupid-ai
```

## 快速开始

安装后 11 个 skill 会按描述自动触发，也可以显式调用。插件命令使用 `/human-plan:<skill>` 命名空间。日常使用优先输入一个诉求，让插件自己 loop 到人工 gate：

```
/human-plan:idea 我觉得搜索体验不太对劲

# 到 approve gate 后，由用户精确批准。只有这一步之后才允许改源码。
/human-plan:dev approve docs/human-plans/search-revamp.md@v3
```

做前端体验方案时：

```
/human-plan:design 为搜索结果页生成体验 Plan
/human-plan:dev approve docs/human-plans/search-experience.md@v3
```

批量治理时：

```
/human-plan:batch-code-scan
/human-plan:worktree docs/human-plans/BCS-001-cache-contract.md@v1
```

后台循环时：

```bash
node plugins/human-plan/loop/runner.js start 5
node plugins/human-plan/loop/runner.js status
node plugins/human-plan/loop/runner.js stop
```

在 Claude Code 里也可以用：

```text
/human-plan:loop start 5
/human-plan:loop status
/human-plan:loop stop
```

`5` 表示本次 runner 最多执行 5 个 tick。每个 tick 只推进 active Plan 的一个明确片段，避免 token 失控。某个 Plan 到 approve / confirm gate 后会暂停当前 batch；下一 tick 必须继续这个 active Plan，不能跳过它处理后续 Plan。当前 batch 的所有 Plan 都 complete 并固化后，下一轮 loop 才会基于最新代码重新扫描。

## Batch 账本

后台 loop 会维护：

```text
docs/human-plans/.loop/
  state.json
  batch-index.md
  run-log.md
  gates.md
  changelog.md
  token-ledger.md
  batches/
  STOP
```

- `batch-index.md` 记录本轮扫出了哪些问题、优先级和处理状态。
- `gates.md` 记录等待用户 `approve` / `confirm` / 决策的事项。
- `changelog.md` 记录本轮实际解决了什么、改动了哪些模块、验证结果如何。
- `token-ledger.md` 记录每个 tick 的 token 估算或真实 usage。
- `batches/` 归档已全部解决并固化的 batch 总结。

## 自动 loop 停在哪里

`human-plan` 会自动推进安全阶段，但这些情况必须停止：

- `Needs Reconfirmation` 非空，需要用户补充业务、产品、合规或破坏性变更决策
- Status 为 `reconfirmation-pending`，等待用户精确 `confirm`
- 已到 `approve gate`，等待用户精确 `approve`
- Plan Ref 版本不匹配、Owner/Status 前置条件不满足
- `worktree` 已创建，需要用户进入新 worktree 会话

后台 batch loop 中，上述停止会暂停当前 batch。loop 会把 active Plan 写入 `gates.md`，等待用户处理这个 Plan；后续 Plan 保持 pending，不会被跳过执行。只有 batch 内所有 Plan 都 complete 且代码状态已固化，才归档本轮 batch。

## 约定

- Human Plan 写在项目内 `docs/human-plans/` 下，文件名即 Plan ID
- Plan Ref 格式：`<Plan 文件路径>@v<Version>`
- 需要隔离执行时，一个 Plan 一个 worktree，避免分支串味
- 所有产出使用简体中文（代码标识、路径、命令不翻译）
- 默认自动推进可安全执行的 loop 阶段；只有 `confirm`、`approve`、人类决策、版本不匹配、前置条件不满足或 `worktree` 创建完成时停止
- 后台 loop 默认从 `batch-code-scan` 开始；一个 batch 内不反复全量扫描项目，只有本 batch 全部解决并固化后，下一轮 loop 才基于最新代码重新扫描
- 后台 loop 必须指定或使用默认 tick 上限，并记录 token 账本
- `worktree` skill 会用相对符号链接把 Plan 文件和必要本地配置带进新 worktree；若项目本身存在 `.claude/skills`，才同步该目录

## 结构

```
plugins/human-plan/
├── .claude-plugin/
│   └── plugin.json
├── shared/
│   └── human-plan-protocol.md
├── skills/
│   ├── idea/           { SKILL.md, agents/openai.yaml }
│   ├── design/         { SKILL.md, agents/openai.yaml }
│   ├── design-check/   { SKILL.md, agents/openai.yaml }
│   ├── plan-check/     { SKILL.md, agents/openai.yaml }
│   ├── worktree/       { SKILL.md, agents/openai.yaml }
│   ├── dev/            { SKILL.md, agents/openai.yaml }
│   ├── bug-fix/        { SKILL.md, agents/openai.yaml }
│   ├── audit/          { SKILL.md, agents/openai.yaml }
│   ├── arch-check/     { SKILL.md, agents/openai.yaml }
│   ├── code-scan/      { SKILL.md, agents/openai.yaml }
│   └── batch-code-scan/{ SKILL.md, agents/openai.yaml }
└── README.md
```

每个 skill 目录下：
- `SKILL.md` — Claude Code 标准 skill 定义（`name` + `description` frontmatter + 指令正文）
- `agents/openai.yaml` — OpenAI Codex 接口描述（跨工具兼容，可选）

## License

MIT © yejiawei

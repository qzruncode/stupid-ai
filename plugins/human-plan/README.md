# human-plan

> A Human-Plan-driven development workflow plugin for Claude Code. Part of the [stupid-ai](../../) marketplace.

## 这是什么

`human-plan` 是一套 Human Plan 驱动的 AI 开发闭环。它把“让 AI 写代码”拆成：先对齐需求，再检查架构和设计，再人工 approve，最后实现和 audit。Human Plan 写在项目内 `docs/human-plans/` 下，只保存人类要审核的需求、边界、取舍和验收，不写代码、不写逐文件步骤。

核心路线：

```
idea / code-scan / arch-check / batch-code-scan
  → dev → plan-check → design-check → dev approve → audit

design → design-check → dev → plan-check → design-check → dev approve → audit

bug-fix → plan-check → design-check → bug-fix approve → audit
```

所有下一步都由当前 Plan 的 Owner Skill、Status、Needs Reconfirmation 和 Version 决定；任一步有待确认事项，都必须回到 Owner Skill replan，再由用户显式 confirm。

## Skills

| 类型 | Skill | 作用 |
|------|-------|------|
| 需求成形 | `/human-plan:idea` | 把模糊想法整理成可落地的顶层需求 Plan |
| 体验设计 | `/human-plan:design` | 资深 UX/UI 角色产出体验 brief Plan |
| 开发执行 | `/human-plan:dev <Plan Ref>` | 把已接受的 Plan 转成开发 Plan；approve 后才允许改源码 |
| Bug 修复 | `/human-plan:bug-fix` | 已定位 bug 先写修复 Plan，再走检查和 approve |
| 架构检查 | `/human-plan:plan-check <Plan Ref>` | 检查需求是否能融入现有系统、代码结构和边界 |
| 设计检查 | `/human-plan:design-check <Plan Ref>` | 检查交互、视觉、状态、响应式和可用性 |
| 审计闭环 | `/human-plan:audit <Plan Ref>` | 对已实现代码做需求一致性和质量审计 |
| 隔离执行 | `/human-plan:worktree <Plan Ref>` | 为一个 Plan 创建一个独立 worktree 和分支 |
| 持续扫描 | `/human-plan:code-scan` | 扫描当前项目，产出一个优先处理 Plan |
| 批量扫描 | `/human-plan:batch-code-scan` | 一次扫完整项目，拆出多个可并行推进的 Plan |
| 成熟方案 | `/human-plan:arch-check` | 检查业务/代码/架构是否在重复造轮子或偏离成熟方案 |

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

## 使用

安装后 11 个 skill 会按描述自动触发，也可以显式调用。插件命令使用 `/human-plan:<skill>` 命名空间。

```
/human-plan:idea 我觉得搜索体验不太对劲
/human-plan:dev docs/human-plans/search-revamp.md@v2
/human-plan:plan-check docs/human-plans/search-revamp.md@v3
/human-plan:design-check docs/human-plans/search-revamp.md@v3
/human-plan:dev approve docs/human-plans/search-revamp.md@v3
/human-plan:audit docs/human-plans/search-revamp.md@v3
```

做前端体验方案时：

```
/human-plan:design 为搜索结果页生成体验 Plan
/human-plan:design-check docs/human-plans/search-experience.md@v1
/human-plan:dev docs/human-plans/search-experience.md@v2
```

批量治理时：

```
/human-plan:batch-code-scan
/human-plan:worktree docs/human-plans/BCS-001-cache-contract.md@v1
```

## 约定

- Human Plan 写在项目内 `docs/human-plans/` 下，文件名即 Plan ID
- Plan Ref 格式：`<Plan 文件路径>@v<Version>`
- 每个 Plan 一个 worktree，避免分支串味
- 所有产出使用简体中文（代码标识、路径、命令不翻译）
- `worktree` skill 会用相对符号链接把 Plan 文件和必要本地配置带进新 worktree；若项目本身存在 `.claude/skills`，才同步该目录

## 结构

```
plugins/human-plan/
├── .claude-plugin/
│   └── plugin.json
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

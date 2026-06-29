# human-plan-flow

> A Human-Plan-driven development workflow plugin for Claude Code. Part of the [stupid-ai](../../) marketplace.

## 这是什么

`human-plan-flow` 把一次开发拆成 8 个有人类审核关卡的阶段，加上 3 个持续健康度扫描。每个阶段的核心产物是一份 **Human Plan**——写在项目内 `docs/human-plans/` 下、面向人类审核的计划文档（不写代码、不写执行步骤）。AI 先写 Plan，人确认，再动手。

整条链路：

```
idea → design → design-check → plan-check → worktree → dev → bug-fix → audit
                                    ↑
                        arch-check / code-scan / batch-code-scan（持续健康度）
```

## Skills

| 阶段 | Skill | 作用 |
|------|-------|------|
| 0. 模糊想法 | `/idea` | 把模糊的产品担忧/目标理清成具体需求 |
| 1. 体验设计 | `/design` | 资深 UX/UI 角色产出体验主张 Human Plan |
| 2. 设计评审 | `/design-check` | 对设计做产品/交互/视觉评审 |
| 3. 架构评审 | `/plan-check` | 对 Human Plan 做架构与代码影响评审 |
| 4. 隔离环境 | `/worktree <Plan Ref>` | 一个 Plan 一个 worktree，隔离执行 |
| 5. 开发 | `/dev <Plan Ref>` | 按通过的 Plan 执行开发 |
| 6. 修 bug | `/bug-fix` | 已定位的 bug 先写修复 Plan 再改 |
| 7. 审计 | `/audit` | 对 AI 写的变更做需求/质量审计 |
| 持续 | `/arch-check` | 检查是否在重复造轮子、偏离成熟方案 |
| 持续 | `/code-scan` | 扫描当前项目的 bug/低效/冗余/可维护性 |
| 持续 | `/batch-code-scan` | 全项目一次性扫描，拆成多个独立 Human Plan |

## 安装

先加 marketplace，再装本 plugin：

```
/plugin marketplace add yejiawei/stupid-ai
/plugin install human-plan-flow@stupid-ai
```

本地开发/测试：

```
/plugin marketplace add /path/to/stupid-ai
/plugin install human-plan-flow@stupid-ai
```

## 使用

安装后 11 个 skill 会按描述自动触发，也可以显式调用：

```
/idea 我觉得搜索体验不太对劲
/design 为搜索结果页生成体验 Plan
/design-check
/plan-check
/worktree docs/human-plans/search-revamp@v1
/dev docs/human-plans/search-revamp@v1
/audit
```

Plugin skills 会带命名空间前缀，例如 `/human-plan-flow:design`。

## 约定

- Human Plan 写在项目内 `docs/human-plans/` 下，文件名即 Plan ID
- Plan Ref 格式：`<Plan 文件路径>@v<Version>`
- 每个 Plan 一个 worktree，避免分支串味
- 所有产出使用简体中文（代码标识、路径、命令不翻译）
- `worktree` skill 会用相对符号链接把 `.claude/skills`、`settings.local.json` 等上下文带进新 worktree，假设类 Unix 文件系统（macOS/Linux）；Windows 下未验证

## 结构

```
plugins/human-plan-flow/
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

---
name: worktree
description: Use when the user invokes /human-plan:worktree with a Plan Ref or needs a project-local git worktree paired one-to-one with a Human Plan so one plan can be executed in an isolated branch/session with the required local workflow context available.
---

# Worktree

`worktree` 是操作型技能：只创建或复用一个与 Human Plan 一一对应的本地 git worktree，并准备继续执行该 Plan 所需的本地上下文。它不产出、不修改 Human Plan，不执行开发、检查或审计；创建完成后按协议停止，让用户进入新 worktree 会话。

所有产出使用简体中文。代码标识、路径、分支名、命令和错误信息不翻译。

## 职责

- 读取 Plan Ref，确认 Version、Plan ID、Status 和 Needs Reconfirmation 是否允许进入独立执行。
- 为同一个 Plan 稳定生成同一个 worktree 路径和分支名。
- 复用已有 worktree，避免一个 Plan 对应多个分支。
- 把 Plan 文件和项目本地 workflow 上下文带进 worktree，保证新会话能继续使用同一套 Human Plan 协议。
- 不复制未提交源码改动，不执行破坏性 git 操作。

## 命令

`/human-plan:worktree <Plan Ref>`

`Plan Ref` 格式必须是 `<Plan 文件路径>@v<Version>`。

## 校验

- 在当前 git 仓库内执行。
- 读取 `Plan Ref` 指向的文件；Version 必须匹配，`Plan ID` 必须非空。
- `Needs Reconfirmation` 非空或 `Status` 为 `reconfirmation-pending` 时停止，并返回当前合法下一步。
- 路径或分支已被其他 Plan 占用时停止。

## 命名

- 从 `Plan ID` 生成 slug：小写，只保留 `a-z`、`0-9`、`-`，合并连续 `-`，去掉首尾 `-`。
- 如果 slug 为空，使用 `plan-<Plan Ref 的 12 位稳定哈希>`。
- Worktree 路径固定为 `.claude/worktrees/<slug>`。
- 分支名固定为 `worktree/<slug>`。

## 创建与上下文

- 创建前确保 `.git/info/exclude` 包含 `.claude/worktrees/`。
- 从当前 `HEAD` 创建 worktree；不复制未提交代码改动。
- 同一 Plan 复用已有 worktree。
- 在目标 worktree 的同相对路径创建 Plan 文件符号链接，指向原 `Plan Ref` 文件；保留 `@v<Version>` 作为后续命令参数。
- 如果当前项目存在 `.claude/skills` 且目标 worktree 缺少 `.claude/skills`，创建指向当前项目 `.claude/skills` 的相对符号链接；不存在时跳过。
- 如果当前项目存在 `.claude/settings.local.json`，在目标 worktree 创建同路径相对符号链接。
- 已存在且指向相同目标时复用；已存在但不是同一目标时停止。
- 不复制 Plan 文件、批次索引、产品代码改动、worktree 目录、缓存或日志。

## 输出

成功后只输出：

- Worktree 路径
- 分支名
- 是否复用已有 worktree
- Plan Ref
- 下一步命令

下一步命令格式：

```bash
cd <Worktree 路径>
/human-plan:dev <Plan Ref>
```

`worktree` 是自动 loop 的边界：输出后立即停止。

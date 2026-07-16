---
name: dep-audit
description: Use when the user invokes /repo-guardian:dep-audit or asks to audit dependencies — outdated packages, known vulnerabilities, wheel-reinvention detection, better alternatives.
---

# Dependency Audit

审查项目所有三方依赖的健康度：过时、漏洞、冗余、重复造轮子、生态替代方案。

## 工作步骤

### 1. 列出所有依赖

读 `package.json`（以及其他语言对应的 `Cargo.toml` / `go.mod` / `requirements.txt`），区分直接依赖和间接依赖。

### 2. 逐项检查

每项检查以下维度，附证据：

| 维度 | 检查方式 |
|---|---|
| 版本过时 | 比最新版落后 ≥2 个 major，或 ≥5 个 minor，或最后发布超 2 年 |
| 已知漏洞 | 查 GitHub Advisory 看有无未修复的 CVE |
| 维护状态 | GitHub 仓库是否归档、是否长期无人维护 |
| 冗余重复 | 项目被引入了两个以上功能重复的包 |
| 造轮子 | 项目自己实现了这个包的已有能力 |
| 无用依赖 | 声明了但代码里没用到 |
| 太重 | 只用 1% 功能却引入了全量 |

### 3. 使用 GitHub MCP 做生态比对

对每项值得关注的依赖，用 GitHub MCP 搜索：
- **有没有更好的替代**：搜对应技术栈的当前推荐方案
- **对比活跃度**：stars、最近 release、社区趋势
- **是否被淘汰**：社区是否正在迁移到替代方案

### 4. 输出结果

按状态分组：

- 🔴 **严重** — 有漏洞 / 已停维 / 有明确更优替代
- 🟡 **预警** — 版本严重滞后 / 轻量替代明显 / 有造轮子嫌疑
- 🟢 **可提升** — 略落后但不紧急
- ⚪ **健康** — 版本合理，维护正常

每个依赖给：
- 当前版本 → 推荐版本/替代依赖
- 问题说明
- 迁移成本（涉及多少文件、有无 breaking change）
- 具体迁移步骤

## 造轮子检测

特别留意项目里**自己实现的通用能力**：

- 自己写工具函数：`utils/deepClone.ts`、`utils/formatDate.ts` 等
- 自己写组件库：和已有组件库重复的手写组件
- 自己写基础设施：HTTP 封装、状态管理、缓存层

发现后必须搜索对应的成熟方案，在报告中给出替换建议。

## 运行方式

`/repo-guardian:dep-audit` — 全量审计

`/repo-guardian:dep-audit lodash` — 只查某个依赖
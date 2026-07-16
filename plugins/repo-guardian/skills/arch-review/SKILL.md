---
name: arch-review
description: Use when the user invokes /repo-guardian:arch-review or asks to review a repository's architecture — module boundaries, layering, dependency direction, circular dependencies, extensibility.
---

# Architecture Review

审查仓库的**架构健康度**：分层是否合理、模块边界是否清晰、依赖方向是否正确、扩展性是否够用。

## 工作步骤

### 1. 画出架构地图

- 读 `package.json`、`tsconfig`、构建配置，确定技术栈
- 标注顶层模块/目录划分
- 识别分层：展示层、领域层、基础设施层、共享层
- 记录模块间的依赖方向

### 2. 扫描问题

以下每个问题必须附**具体证据**（文件路径、引用关系）：

| 问题 | 说明 |
|---|---|
| 分层侵蚀 | 展示层直接操作 DB / 原始 API 客户端 |
| 边界模糊 | 模块直接 import 另一模块的内部文件而非公开出口 |
| 依赖倒置 | 底层模块依赖上层模块 |
| 循环依赖 | A→B→A，导致初始化死锁 |
| 上帝模块 | 单文件超 500 行，一个模块管了 N 件不相关的事 |
| 幽灵依赖 | 用了未在 package.json 声明的包 |
| 扩展性问题 | 加个功能要改 5+ 个文件 |

每个问题标注等级：
- **阻塞**：当前已经导致构建失败或严重阻碍开发
- **高危**：短期内会引发问题
- **值得关注**：增加维护成本但不紧急
- **观察**：暂时没问题但趋势不好

### 3. 输出治理建议

针对每个问题给出：
- **一句话摘要**
- **证据位置**：具体文件路径
- **问题影响**：现在和未来会有什么成本
- **治理方案**：具体的迁移/重构步骤（必须安全可回滚）
- **风险**：治理过程中可能出什么问题

## 运行方式

`/repo-guardian:arch-review` — 全仓库扫描

`/repo-guardian:arch-review src/modules/order` — 只看指定模块

结束时列出所有发现，标记哪些值得立刻治理，哪些先观察。没有严重问题就明确说"这个范围内架构健康"。
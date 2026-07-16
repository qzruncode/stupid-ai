---
name: code-quality
description: Use when the user invokes /repo-guardian:code-quality or asks to audit code quality — redundancy, duplication, complexity, maintainability, error handling, and concrete bug risks.
---

# Code Quality

审查代码实现质量：冗余、重复、复杂度、错误处理、可维护性。

## 工作步骤

### 1. 扫一遍代码

按以下类别扫描，**每个发现必须给出具体文件路径和代码位置**：

| 类别 | 检查点 |
|---|---|
| 重复代码 | 同一段逻辑出现在 3+ 个地方 |
| 高复杂度 | 单函数超 100 行、嵌套超 4 层、圈复杂度 > 15 |
| 脆弱错误处理 | catch 是空的、Promise 错误没处理、异常被静默吞掉 |
| 魔法值 | URL、超时、阈值直接硬编码，不在配置里 |
| 类型安全 | 大量 `any`、无脑 `as` 转换、`@ts-ignore` 成堆 |
| 死代码 | 无调用的导出函数、废弃参数、注释掉的代码 |
| 反模式 | 副作用泄漏、异步回调地狱、不安全的字符串拼接 |
| 安全风险 | SQL 拼接、`eval`、敏感信息暴露 |

### 2. 用 GitHub MCP 查替代生态

如果发现项目在**自己实现生态中已有的能力**，搜一下 GitHub 看看标准做法：

- 手写深拷贝 → 搜 `structuredClone` / `lodash.cloneDeep`
- 自建状态管理 → 搜 React Context / zustand / valtio
- 自建 HTTP 封装 → 搜 axios / ky / ofetch
- 手写日期工具 → 搜 dayjs / date-fns

在报告中给出：当前做法 → 推荐做法 → 迁移成本评估

### 3. 输出治理条目

每个问题：
- **问题**：一句话
- **证据**：文件:行号
- **影响**：为什么不健康
- **建议**：怎么修
- **验证**：修完怎么确认没问题

## 运行方式

`/repo-guardian:code-quality` — 全仓库扫描

`/repo-guardian:code-quality src/components` — 只看指定路径

结束后按"严重→一般→建议"列出发现。
---
name: roadmap
description: Use when the user invokes /repo-guardian:roadmap or asks where the project should go next — analysis of improvement directions, feature opportunities, technical evolution, and a phased development roadmap.
---

# Roadmap

综合项目现状和 GitHub 生态趋势，回答"这个项目下一步应该做什么"。

这是一个**汇聚 skill**：它会先调用其他 skill 收集各维度的数据（如果还没跑过就跑一次精简版），然后综合输出分阶段路线图。

## 工作步骤

### 1. 收集信息

- 读 `README`、`CLAUDE.md`、`CHANGELOG`、git log 了解项目目标和发展阶段
- 读各治理维度的已有输出
- 如果 arch-review / code-quality / dep-audit / perf-audit / design-review 还没跑过，先跑感知版收集数据

### 2. 交叉分析——找根因

综合各维度发现，寻找**共同根因**：

- 多个重复实现 → 可能缺开发规范
- 架构侵蚀 + 测试缺失 → 快速迭代积累的技术债
- 依赖过时 + 造轮子 → 缺依赖管理习惯
- 多个小问题指向同一原因 → 合并成一件治理事项

### 3. GitHub 生态趋势分析

用 GitHub MCP 探索（每条有搜索依据）：

- 项目的核心技术栈正在往哪个方向演进？
- 项目现在遇到的问题，社区有没有更成熟的解法？
- 项目当前依赖中有哪些正在被社区淘汰？
- 同类项目的功能覆盖面哪些是项目还没有的？

### 4. 输出分阶段路线图

#### 现在（1-4 周）——止血
- 修复严重安全问题
- 解决当前阻塞开发的瓶颈
- 确定不做什么

#### 中期（1-3 月）——治理
- 架构调整和模块重组
- 依赖升级和替换
- 代码质量批次治理
- 性能优化

#### 长期（3-6 月）——进化
- 新架构/新能力落地
- 技术栈升级
- 功能方向探索

每个阶段至少包含：做什么、为什么、怎么做、怎么算做完。

## 运行方式

`/repo-guardian:roadmap` — 输出完整路线图

`/repo-guardian:roadmap 前端` — 只针对某个方向

关键要求：路线图必须是可直接执行的行动方案，不是空泛的"加强质量"、"优化性能"。如果数据不够做有效路线图，直接说缺什么，不编造通用建议。
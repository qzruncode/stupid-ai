---
name: feature-list
description: Initialize, maintain, update, or audit a complete code-free functional baseline at docs/product-spec/feature-list.md. Use when the user invokes /code-cleanup:feature-list, wants an exhaustive product feature list that any AI can use to reproduce the full product without seeing its code, provides an approved business change that must update the baseline, or asks whether the existing baseline is complete and current.
---

# Maintain Feature List

维护 `docs/product-spec/feature-list.md` 这一份唯一功能基准。最终文件必须完全脱离原代码库：任意 AI 只读取它，就能复刻并验收完整产品。

本 skill 只修改功能清单，不修改源码、测试、配置或工程文档，也不自动执行 `/code-cleanup:cleanup`。

## 开始前

完整读取 `../../references/feature-list-contract.md`，然后根据目标文件状态选择模式：

- 文件不存在：执行初始化。
- 文件存在且用户提供已确认业务变化：执行更新。
- 文件存在且用户要求补全、核查或刷新：执行完整性审计，只吸收有权威业务依据的内容。

## 初始化

1. 盘点所有产品入口、页面、导航、角色、公开接口、任务、通知和外部集成；阅读产品资料、测试和运行行为，并按需实际操作产品。
2. 建立临时证据矩阵，追踪每项行为的来源、冲突和缺口。证据矩阵只用于分析，不能写入最终清单。
3. 先恢复产品边界、体验规范、全局规则和功能索引，再逐项补齐功能详述、跨功能旅程、公开契约、数据生命周期和质量属性。
4. 从产品使用者和复刻者视角描述“产品做什么”，删除全部实现信息。
5. 对无法确认且会影响复刻的内容标为 `draft`，提出精确业务问题；继续补齐其他范围。没有解决阻塞项时不得把整体标为 `ready`。

初始化是唯一允许以现有产品和代码行为恢复初始事实的阶段。基准建立后，代码不再拥有定义功能的权力。

## 更新

1. 只接受用户确认、产品决策、正式需求或等价权威来源作为业务变化。
2. 把变化写成可判定的前后差异，并检查角色、体验、规则、上下游功能、公开契约、数据生命周期和质量属性的连锁影响。
3. 保持功能 ID 稳定；新增功能分配新 ID；废弃功能保留 ID，标记 `deprecated` 并说明替代和兼容边界。
4. 同步修改索引、详述、旅程和所有关联章节，更新语义化版本与变更记录。
5. 更新后的 `ready` 内容立即成为代码必须达到的新基准，不要求当前实现已经完成。

当前代码只能帮助发现影响范围。代码与基准不同时，不得依据代码反向修改基准；没有已确认业务变化时，应把差异留给实现或 `/code-cleanup:cleanup` 修正。

## 无代码内容

最终功能清单不得出现：

- 源码、伪代码、代码块、文件或目录路径。
- 函数、类、方法、模块、组件等实现符号。
- 框架、库、依赖包、构建工具、配置项或环境变量。
- 数据库表、字段、索引、迁移脚本或内部存储结构。
- 调用链、实现证据、测试文件或“当前代码如何完成”。

公开页面、用户操作、公开 API、事件、文件格式和外部集成属于产品行为，必须完整描述，但使用自然语言和表格表达，不附实现代码或内部设计。

## 完成检查

1. 运行插件校验器。
2. 隐藏原仓库，进行盲复刻审读：逐项检查另一个 AI 是否还需要猜产品范围、页面结构、视觉与文案、角色权限、输入校验、业务规则、状态、异常、数据语义、公开协议或验收结果。
3. 检查本次 diff，确认唯一持久化变更是功能清单，且没有任何实现内容。
4. 用户要求完整产品清单时，不得把部分覆盖包装成完成；持续补齐到 `ready`，或明确列出真正需要业务决策的阻塞项。

结束时报告模式、规格版本、覆盖范围、功能总数及状态分布、已解决和剩余缺口、盲复刻审读结论与校验结果。不开始清理代码。

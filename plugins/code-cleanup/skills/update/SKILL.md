---
name: update
description: Update the canonical code-free functional baseline from an approved business change without implementing or refactoring code. Use when the user invokes /code-cleanup:update, changes a business rule or product behavior, or wants to evolve docs/product-spec/feature-list.md before code implementation while keeping baseline management separate from development and optimization.
---

# Update Feature List

只根据已确认的业务变化更新 `docs/product-spec/feature-list.md`。本流程不实现业务、不优化代码、不改测试或工程配置，也不自动调用其他 `code-cleanup` 流程。更新后的 `ready` 内容立即成为代码必须达到的新基准，不要求当前代码已经实现。

## 开始前

完整读取 `../../references/feature-list-contract.md`。目标文件不存在时停止更新，要求先运行 `/code-cleanup:generate`，不能凭一句变更描述伪造完整基线。

## 基准权威

- 只把用户确认、产品决策或等价的权威业务输入写入基准。
- 当前代码只能用于发现影响范围，不能证明“需求就是这样”。代码与基准不同而没有业务变更时，不更新清单；应让后续实现或 `/code-cleanup:optimize` 修正代码。
- 业务描述含糊或规则冲突时，把相关功能降为 `draft` 并记录精确问题，不从现有代码猜答案。
- 先更新基准，再由独立开发流程实现业务变化；不得为了匹配尚未更新的代码而削弱新基准。

## 更新流程

1. 读取当前版本、覆盖范围、功能索引、相关功能详述、全局规则、旅程、外部契约和变更记录。
2. 把已确认的业务输入改写成可判定的行为差异：谁在什么条件下，输入什么，系统如何响应，状态和副作用如何变化。
3. 做影响分析，检查角色、业务对象、全局规则、上下游功能、公开协议、数据生命周期和非功能约束。
4. 保持现有功能 ID；新增功能分配新 ID；废弃功能保留记录并标记 `deprecated`，说明替代功能和兼容窗口。
5. 同步修改索引、详述、跨功能旅程、契约总表及其他受影响章节，避免只改一处造成自相矛盾。
6. 按语义化版本更新规格版本：破坏性行为变更升主版本，向后兼容的新能力升次版本，澄清和无行为变化修订升补丁版本。
7. 在变更记录中写日期、变更类型、功能 ID、行为差异和兼容影响。
8. 运行结构校验和复刻审读，确认修改后仍无需代码背景。

## 完成标准

- diff 只包含功能清单。
- 新旧行为边界、迁移或兼容语义完整，关联章节一致。
- 新基准表达业务目标，不受当前代码是否已经实现影响。
- 没有把未经确认的代码差异写成需求。
- 没有实现代码、补测试或启动优化。

结束时报告规格版本变化、受影响功能 ID、关键行为差异、兼容影响、未决事项和校验结果。

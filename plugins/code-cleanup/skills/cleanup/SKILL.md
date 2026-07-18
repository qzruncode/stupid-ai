---
name: cleanup
description: Continuously clean up, simplify, refactor, or rewrite an AI-evolved codebase while using docs/product-spec/feature-list.md as the sole functional baseline. Use when the user invokes /code-cleanup:cleanup, says business iteration has made the code messy, wants to reduce duplication, complexity, inconsistent patterns, dead paths, dependencies, or performance waste, or needs the implementation made easier and more efficient without losing any baseline feature.
---

# Cleanup Against Feature Baseline

以 `docs/product-spec/feature-list.md` 为唯一功能基准，持续收敛业务迭代和 AI 生成造成的代码混乱。可以重构或彻底重写实现，但不得修改功能清单；最终实现必须满足目标范围内全部 `ready` 功能。

## 开始前

完整读取 `../../references/feature-list-contract.md`，再读取功能清单并运行结构校验。

只有以下情况阻塞目标范围：

- 功能清单不存在。
- 目标功能不是 `ready`，或基准自相矛盾，无法形成唯一验收结果。
- 涉及不可逆数据操作，而基准没有定义保留、迁移或恢复语义。

当前代码、旧测试或旧文档与基准冲突不是阻塞项。基准胜出：修正实现和错误测试，不修改清单迁就现状。代码里存在但基准没有定义的行为不具备基准地位。

## 清理闭环

1. **锁定基准**：确定目标功能 ID，提取角色、输入、流程、状态、权限、输出、副作用、公开协议、质量约束和验收场景，形成可执行验收矩阵。
2. **恢复实现地图**：定位目标行为的入口、调用方、状态和数据流，把当前实现映射到验收矩阵；实现地图只用于本次清理，不写入功能清单。
3. **盘点混乱点**：检查重复业务规则、分叉实现、过度抽象、透传包装、冗余状态、无效转换、死代码、兼容残留、不一致模式、无用依赖、自制基础设施、低效算法、重复 I/O、N+1 请求和无效渲染。
4. **建立清理前证据**：运行基准验收并记录当前偏差；按目标记录可复查指标，例如重复实现数量、维护触点、复杂度、依赖数、延迟、CPU、内存、I/O、查询数、构建时间或产物体积。
5. **按语义批次清理**：每次处理一个边界明确的混乱簇，选择唯一规范实现，迁移全部调用方，删除被替代路径。允许在基准边界内重新设计或重写，不保留“以防万一”的双实现。
6. **修正基准偏差**：代码缺失、错误或多出与 `ready` 基准冲突的行为时，把代码修到基准；现有测试固定了错误行为时同步修正测试。
7. **验证功能完整**：运行验收矩阵、受影响测试和公开协议检查。任一目标功能不符合清单，本批次就没有完成。
8. **验证清理收益**：对比清理前后证据，确认维护概念、重复路径、复杂度或资源消耗真实下降，且没有关键指标明显退化。没有收益或证据不足时继续调整或撤销方案。
9. **防止重新变乱**：在已有测试、lint、benchmark、Agent 规则或 CI 中增加最小护栏，优先阻止同一规则再次出现平行实现和已消除的低效模式。
10. **继续推进**：完成一个安全批次后继续下一个高价值批次，直到用户范围清理完成、没有验证充分的候选或遇到真实基准阻塞。

## 写入边界

- 允许修改实现、测试和必要工程护栏。
- 禁止修改功能清单；业务变化必须单独运行 `/code-cleanup:feature-list`。
- 不建立第二套功能文档或 cleanup ledger。
- 不覆盖范围外用户改动；除非用户明确要求，不提交、不推送、不部署。

结束时报告：目标功能 ID、修正的基准偏差、保留的规范实现、删除的混乱路径、清理前后证据、功能验收、护栏和剩余候选。代码行数只能作为附带信息，不能代替功能完整性和清理收益。

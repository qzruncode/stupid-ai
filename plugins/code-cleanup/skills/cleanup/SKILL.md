---
name: cleanup
description: Systematically rescan, simplify, refactor, or rewrite the full product scope declared by docs/product-spec/feature-list.md, with mandatory file coverage and a persistent cleanup plan. Use when the user invokes /code-cleanup:cleanup, says repeated business iteration has created messy code, wants a scope-wide cleanup rather than one dead-file deletion, or needs duplication, complexity, oversized modules, inconsistent patterns, legacy paths, dependencies, and performance waste removed without losing any ready feature.
---

# Systematic Cleanup

以 `docs/product-spec/feature-list.md` 为唯一功能基准，系统性重新扫描并收敛业务迭代和 AI 生成造成的代码混乱。允许重构或彻底重写实现，但不得修改功能清单。

## 开始前

完整读取 `../../references/feature-list-contract.md` 和 `../../references/cleanup-plan-contract.md`，校验功能清单，然后按以下优先级确定范围：

- 用户在本次 cleanup 明确指定功能、模块或应用：以用户指定范围为准，但必须落在功能清单已声明的覆盖范围内。
- 用户未另行指定：完整继承功能清单的“覆盖范围”。清单只覆盖 CodeBench 时就系统清理全部 CodeBench；清单覆盖完整仓库产品时才清理完整仓库。
- 不得根据当前页面、最近对话、最近 diff、单个错误或最容易处理的目录隐式缩小范围。

功能清单缺失或目标范围超出清单时不得修改代码。目标范围含 `draft`，或不可逆数据操作缺少保留与恢复语义时，仍须完成全量技术盘点；只执行完全关联 `ready` 功能且不受缺口影响的候选，把依赖未决语义的文件和候选标为 `blocked`。这不会阻塞其他独立的安全批次，但范围内功能全部 `ready` 前不得把整个 cleanup 标为完成。同步报告基准缺口，并运行 `/code-cleanup:feature-list` 补齐。

当前代码、旧测试或旧文档与 `ready` 基准冲突不是阻塞项。基准胜出：修正实现和错误测试，不修改清单迁就现状。

## 阶段一：强制全量盘点

读取或创建 `docs/code-cleanup/cleanup-plan.md`。首次运行必须先完成整个目标范围的技术盘点，盘点完成前不得修改实现：

1. 枚举范围内全部源码、测试和工程配置，明确生成物、第三方代码和用户排除项，写入文件覆盖表。
2. 将每个文件映射到功能 ID、入口、调用方、状态和数据流；不能映射的文件本身就是候选或阻塞项。
3. 逐文件做语义审查，并结合项目已有 lint、类型检查、测试、依赖图、重复检测、复杂度或性能工具。只做文本搜索不足以证明扫描完成。
4. 系统检查重复规则、分叉实现、过大文件或职责、过度抽象、透传包装、冗余状态、死代码、兼容残留、不一致模式、无用依赖、自制基础设施、低效算法、重复 I/O、N+1 请求、无效渲染、错误与权限分叉、国际化漂移和测试缺口。
5. 为每个问题建立候选，写明关联功能、代码证据、规范方向、风险、验证和状态。按业务影响、混乱扩散、收益、确定性和验证强度排序。
6. 将每个文件标为 `reviewed-clean`、`candidate` 或真实 `blocked`。覆盖率达到 100% 且没有 `unreviewed` 后，才能进入执行阶段；因 `draft` 无法判断的文件和候选必须标为 `blocked`，但不阻塞其他只关联 `ready` 功能的独立候选。

不得在找到第一个未引用文件、TODO、大文件或重复 helper 后停止扫描。它们只关闭一个文件或候选，不能证明目标范围已经盘点完成。

## 阶段二：持续执行批次

1. 从最高优先级且关联功能全部为 `ready` 的候选开始，每次处理一个边界明确的语义簇。
2. 提取关联功能的验收矩阵，先记录当前基准偏差和清理前指标。
3. 选择唯一规范实现，迁移全部调用方，删除被替代路径。允许在基准边界内重新设计或重写，不保留“以防万一”的双实现。
4. 代码缺失、错误或多出与基准冲突的行为时，把代码修到基准；旧测试固定了错误行为时同步修正测试。
5. 运行功能验收、受影响测试和项目质量检查；对比重复路径、维护触点、复杂度、依赖或资源指标。没有真实收益时继续调整或撤销方案。
6. 更新文件覆盖表、候选状态、功能验证和批次记录，然后自动进入下一个 `ready` 候选。
7. 在现有测试、lint、benchmark、Agent 规则或 CI 中增加最小护栏，阻止已消除的平行实现和低效模式重新出现。

## 增量恢复

已有 cleanup plan 时先比较扫描终点与当前代码：

- 新增或修改文件及其直接依赖范围重新标为 `unreviewed`。
- 已删除文件标为 `removed`，关联候选重新核对。
- 功能基准版本变化时，受影响功能的文件和候选全部重新审查。
- 未变化且已有证据的 `reviewed-clean` 文件不重复烧 token。

每次调用都从计划恢复并继续。上下文或时间不足时保存准确断点，明确报告“cleanup 未完成”；不得把一次批次完成表述成系统清理完成。

## 完成门禁

结束前运行 `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_cleanup_plan.py" docs/code-cleanup/cleanup-plan.md`；环境没有 `CLAUDE_PLUGIN_ROOT` 时定位已安装插件后执行同一脚本。只有以下条件全部满足才能报告完成：

- 目标范围功能全部 `ready` 且验收通过。
- 文件覆盖率 100%，没有 `unreviewed` 或 `blocked`。
- 所有候选均为 `done` 或有充分理由的 `declined`。
- 项目质量检查通过，批次有清理前后收益证据和防回退护栏。

否则保持计划为 `inventory`、`executing` 或 `blocked`，继续推进或报告准确断点。

## 写入边界

- 允许修改实现、测试、必要工程护栏和 cleanup plan。
- 禁止修改功能清单；业务变化必须单独运行 `/code-cleanup:feature-list`。
- cleanup plan 是技术执行状态，不是第二份功能文档。
- 不覆盖范围外用户改动；除非用户明确要求，不提交、不推送、不部署。

结束时报告：清理范围、文件覆盖率、候选状态分布、完成批次、修正的基准偏差、删除或重写的混乱路径、清理前后证据、功能验收、护栏、剩余候选和真实阻塞项。

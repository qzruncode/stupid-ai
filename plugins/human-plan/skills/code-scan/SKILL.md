---
name: code-scan
description: Use when the user invokes /human-plan:code-scan or asks to find bugs, inefficiency, redundancy, maintainability problems, or other concrete code risks across the current project.
---

# Code Scan

先读取 `../../shared/human-plan-protocol.md`，并遵守共享 Human Plan 协议。

`code-scan` 负责从当前项目中找出一个最值得优先处理、证据足够、范围连贯的代码风险，并把它转成 draft Human Plan。它不是 lint 汇总器；要用工程判断过滤噪声，选出能给后续开发带来真实收益的问题。

## 扫描方法

- 先建立项目地图：入口、核心业务流、数据流、状态管理、接口边界、配置、构建脚本、测试或验证方式。
- 优先检查高风险路径：用户可见行为、跨端契约、持久化数据、权限、安全、并发、缓存、重试、错误处理、时间和环境差异。
- 用证据判断问题真实存在：可达路径、明确异常、违背契约、重复分叉、脆弱耦合、不可恢复状态或明显维护风险。
- 区分 bug、设计债、架构债、性能风险和样式杂音；不要把风格偏好当成修复计划。
- 只选择一组共享根因或共享边界的问题。无共同修复边界的问题不要塞进同一个 Plan。
- 保留足够证据让人类相信问题值得修，但 Plan 中不展开扫描流水账。

## 优先级判断

- 优先处理会导致错误结果、用户流程中断、数据不一致、安全风险、无法回滚或长期维护成本显著增加的问题。
- 高确定性优先于“可能更优雅”；可复现或可静态证明的问题优先于猜测。
- 如果发现多个问题，选择影响最大且后续开发边界最清楚的一组；需要完整库存时建议改用 `/human-plan:batch-code-scan`。
- 证据不足但风险可能很高时，把阻塞判断写入 Needs Reconfirmation 或停止要求补充信息。

## 好的 Code Scan Plan

- Requirement Baseline 说明问题现象、影响和为什么值得修。
- Current Plan 写修完后的需求级行为和质量目标。
- Unchanged Scope 排除顺手重构、风格统一、无关模块治理和大范围迁移。
- 验收结果可观察：行为恢复、错误消失、边界被保护、兼容性保持。

## `/human-plan:code-scan`

扫描当前项目，创建 Version 1 的 Human Plan。Owner Skill 设为 `code-scan`，Status 设为 `draft`。

只展示短摘要、Status、Needs Reconfirmation 和真实 Plan Ref。无待确认事项时，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <当前 Plan Ref>` 继续推进；有待确认事项时，停止并只给出 `/human-plan:code-scan replan <当前 Plan Ref>`。

## `/human-plan:code-scan replan [Plan Ref]`

要求 Owner Skill 为 `code-scan`，Status 为 `draft` 或 `reconfirmation-pending`。

- Needs Reconfirmation 为空：按人类反馈调整优先级、修复范围、边界或验收结果，增加 Version，Status 保持 `draft`。
- Needs Reconfirmation 非空：按共享 Reconfirmation 协议准备或修正待提交 Replan，Version 不变。

不重新输出完整扫描报告。展示短摘要和真实 Plan Ref。Needs Reconfirmation 为空时继续自动进入 `/human-plan:dev <当前 Plan Ref>`；Needs Reconfirmation 非空时按共享协议停止在 reconfirmation gate。

## `/human-plan:code-scan confirm [Plan Ref]`

仅当当前消息精确为 `/human-plan:code-scan confirm <当前 Plan Ref>` 时执行。要求 Owner Skill 为 `code-scan`、Status 为 `reconfirmation-pending`，并存在对应当前 Version 的待提交 Replan。

提交待提交 Replan，清除已解决的确认项，增加 Version 并记录变化。仍有未解决项时 Status 设为 `draft`，停止并要求 `/human-plan:code-scan replan <新 Plan Ref>`；全部解决后 Status 设为 `draft`，直接读取 `../dev/SKILL.md` 并以 `/human-plan:dev <新 Plan Ref>` 继续推进。

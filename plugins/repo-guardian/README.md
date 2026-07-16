# repo-guardian

> 一个独立的仓库治理插件。扫描仓库的每一面——架构、代码质量、依赖、性能、设计、技术选型——然后告诉你怎么治理、优化、升级，以及下一步该做什么。

`repo-guardian` 不是为了找单一 bug，而是从整体视角审视仓库健康度，输出可执行的治理建议。每个 skill 从一个维度扫描，发现的问题附上证据，按影响和成本排序，并对照 GitHub 生态给出更好的方案。

## 使用方法

| 命令 | 用途 |
|---|---|
| `/repo-guardian:full-scan` | 全维度扫描——从架构到 UI，一次跑完 |
| `/repo-guardian:full-scan [范围]` | 指定范围的全扫描 |
| `/repo-guardian:arch-review` | 架构审查——分层、模块边界、依赖方向、扩展性 |
| `/repo-guardian:code-quality` | 代码质量审查——冗余、重复、复杂度、可维护性 |
| `/repo-guardian:dep-audit` | 三方依赖审计——过时包、漏洞、替代方案、重复造轮子 |
| `/repo-guardian:perf-audit` | 性能审计——热点路径、资源消耗、瓶颈分析 |
| `/repo-guardian:design-review` | 前端样式/交互/UI 质量审查 |
| `/repo-guardian:roadmap` | 项目下一步该做什么——基于现状 + GitHub 趋势 |

所有命令都支持追加范围参数，只治理指定模块/路径，例如 `/repo-guardian:arch-review src/modules/order`。

## Skills 清单

| Skill | 扫描维度 | 产出 |
|---|---|---|
| `arch-review` | 架构分层、模块边界、依赖方向、循环依赖、扩展性 | 架构问题 + 重构建议 |
| `code-quality` | 代码冗余、重复实现、复杂度、可维护性、安全风险 | 质量问题清单 + 修复建议 |
| `dep-audit` | 三方包过时、漏洞、GitHub 替代方案、造轮子检测 | 依赖健康报告 + 升级/替换计划 |
| `perf-audit` | 慢查询、热点路径、渲染性能、包体积、资源消耗 | 性能问题 + 优化建议 |
| `design-review` | UI 一致性、响应式、无障碍、交互体验、CSS 质量 | 设计问题 + 改进建议 |
| `roadmap` | 综合各维度 + GitHub 趋势分析 | 分阶段路线图 |
| `full-scan` | 以上全部维度的全景扫描和交叉分析 | 全景治理报告 |

## 安装

```bash
/plugin marketplace add qzruncode/stupid-ai
/plugin install repo-guardian@stupid-ai
```

## 核心原则

- **生态优先**：遇到问题先查 GitHub 有没有成熟方案，不鼓励重复造轮子
- **证据驱动**：每个发现都必须附具体文件/代码位置，不输出空泛建议
- **按优先级**：按影响 → 成本 → 确定性排序，不输出噪音
- **可执行**：每个发现都含具体步骤和预期效果，不说教原理
- **范围可控**：支持指定范围分批治理，不要求一次扫完全仓库

## License

MIT © yejiawei

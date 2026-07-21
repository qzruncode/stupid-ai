# code-cleanup

> 一份功能基准，持续清理越来越乱的实现。

`code-cleanup` 只维护两个明确流程：

```text
/code-cleanup:feature-list
/code-cleanup:cleanup
```

唯一功能基准是 `docs/product-spec/feature-list.md`。它只写声明范围内的完整产品应该提供什么，不写任何代码或实现信息。未指定范围时必须覆盖仓库承载的整个可交付产品；用户明确只要求 CodeBench 等范围时，就完整覆盖该范围。任意 AI 只拿这一份文件，就应当能够复刻并验收清单声明范围内的完整产品。

## 两个独立 skill

| 命令 | 职责 | 允许修改 | 禁止修改 |
|---|---|---|---|
| `/code-cleanup:feature-list` | 首次初始化、后续业务更新、完整性审计 | 功能清单 | 源码、测试、配置 |
| `/code-cleanup:cleanup` | 全量扫描后，以清单为基准持续清理、重构或重写混乱代码 | 实现、测试、技术清理计划、必要护栏 | 功能清单 |

两个 skill 不会自动串联。业务变化先单独维护功能基准，代码清理在另一个会话或阶段执行。

## 功能清单

```text
/code-cleanup:feature-list
/code-cleanup:feature-list 把退款时限从 24 小时调整为 48 小时
/code-cleanup:feature-list 核查现有清单能否独立复刻完整产品
```

目标文件不得包含源码、伪代码、代码块、文件路径、函数、类、模块、框架、依赖、配置、数据库结构、调用链或实现证据。公开页面、交互、文案、API 和外部协议属于产品行为，使用自然语言和表格完整描述。

## 清理代码

```text
/code-cleanup:cleanup F-014
/code-cleanup:cleanup 清理业务迭代后重复和分叉最严重的实现
```

`cleanup` 不以旧代码为功能事实。旧代码或旧测试与 `ready` 基准冲突时，基准胜出并修正实现。清理可以包含：

- 重复规则、平行实现、死代码和兼容残留。
- 过度抽象、透传包装、冗余状态和无效转换。
- 不一致模式、无用依赖和重复造轮子。
- 低效算法、重复 I/O、N+1 请求和无效渲染。
- 无法继续维护但功能基准已经完整的模块重写。

完成必须同时证明功能基准全部通过，并且维护概念、重复路径、复杂度或资源消耗真实下降。

cleanup 未另传范围时继承功能清单的“覆盖范围”：CodeBench 清单就系统扫描全部 CodeBench，而不是擅自扩大到全仓或缩成最近改动。随后维护 `docs/code-cleanup/cleanup-plan.md`，逐文件达到 100% 扫描覆盖，再连续执行全部候选批次。删除一个未引用文件只完成一个候选；只要还有未审文件、未处理候选或阻塞项，就必须明确报告 cleanup 尚未完成并从断点继续。

## 安装

```text
/plugin marketplace add qzruncode/stupid-ai
/plugin install code-cleanup@stupid-ai
```

## License

MIT © yejiawei

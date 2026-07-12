# code-cleanup

> Keep the behavior, remove the duplicate ways of implementing it.

`code-cleanup` 用一个持续运行的 skill 治理不断长大的 AI 代码库。它先把页面、接口、任务和关键能力沉淀为可验证的功能清单，再按语义批次合并重复实现、替换不必要的自制基础设施、重写无法维护的模块，最后把防回退规则固化进 `CLAUDE.md`、lint 和 CI。

它不要求第一次就把全项目文档写完。某个批次涉及的行为已经被清单覆盖并可验证，就可以先安全收敛；后续开发继续增量补齐项目地图。

## 使用

```text
/code-cleanup:cleanup
/code-cleanup:cleanup 先治理订单模块，不改变公开接口
```

Skill 会持续维护：

```text
docs/code-health/
  feature-checklist.md
  cleanup-ledger.md
```

只有行为含义不明确、需要改变公开契约、涉及数据迁移或不可逆操作时才停下来请求人类决策。其余阶段会从清单、候选排序、代码收敛、验证一直推进到工程护栏。

## 安装

```text
/plugin marketplace add qzruncode/stupid-ai
/plugin install code-cleanup@stupid-ai
```

## 原则

- 功能等价是硬约束，删行数不是目标。
- 同一业务规则只有一个规范实现和明确归属。
- 先固定行为，再迁移调用方，最后删除旧路径。
- 存量问题使用 baseline ratchet，CI 禁止新增和恶化。
- 日常功能迭代只同步触达范围，不反复扫描整个仓库。

## License

MIT © yejiawei

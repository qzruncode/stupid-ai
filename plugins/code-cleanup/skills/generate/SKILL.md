---
name: generate
description: Generate the initial complete, code-free functional baseline for an existing repository. Use when the user invokes /code-cleanup:generate, asks to inventory all product behavior, wants a feature list another model can reproduce without seeing the code, or needs to establish docs/product-spec/feature-list.md as the sole acceptance baseline for future implementation, rewrites, and optimization.
---

# Generate Feature List

从现有系统反向恢复初始功能基准，只生成 `docs/product-spec/feature-list.md`，不修改源代码、测试、配置或其他产品文档。这是唯一一次允许以现有代码为主要事实来源建立基准。

## 开始前

完整读取 `../../references/feature-list-contract.md`。如果目标文件已经存在，不覆盖它；改用 `/code-cleanup:update`，除非用户明确要求废弃旧规格并重新建立基线。

## 生成流程

1. 确定覆盖范围。未指定范围时覆盖整个可交付产品，包括页面、公开接口、后台任务、CLI、通知和外部集成。
2. 读取项目规则、产品文档、路由、公开协议、数据定义、测试和部署入口；必要时运行系统，观察成功、空、加载、失败和权限状态。
3. 建立仅供本次分析使用的证据矩阵：入口、观察到的行为、证据强度、冲突和缺口。不得把源码证据写入最终清单。
4. 先列全量功能索引，再逐项填写详细契约。不得因目录或名称相似而合并业务行为，也不得把内部 helper 当成功能。
5. 把跨功能规则提到系统级章节，功能内只保留特有规则；所有外部可观察差异都必须落到某个功能 ID。
6. 对相互矛盾或无法证明的行为标记 `draft` 并写入未决事项。继续完成其他可确认范围，不用未知内容填空。
7. 运行结构校验，并在隔离思维下做复刻审读：假设实现者看不到代码，检查其是否还需要猜入口、字段、规则、状态、权限、协议或验收结果。

## 完成标准

- 目标范围的入口和功能均进入索引，没有把部分扫描说成全量完成。
- 每个 `ready` 功能仅凭清单即可实现并验收。
- 清单没有源码路径、实现符号、框架或数据库结构。
- 覆盖状态准确；存在阻塞性未知项时不能标为 `ready`。
- `ready` 范围足以作为以后实现、重写和优化代码的唯一验收依据，不再依赖原代码解释功能。
- 本次唯一持久化变更是功能清单。临时分析材料在结束前删除。

结束时报告覆盖范围、功能数量、`ready`/`draft`/`deprecated` 数量、主要未决事项和校验结果，不开始更新业务或优化代码。

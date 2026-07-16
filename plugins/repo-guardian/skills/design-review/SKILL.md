---
name: design-review
description: Use when the user invokes /repo-guardian:design-review or asks to review frontend UI quality — visual consistency, responsive layout, accessibility, interaction design, CSS quality, component library usage.
---

# Design Review

审查前端设计和交互质量：UI 一致性、响应式布局、无障碍、CSS 质量、交互体验。

## 工作步骤

### 1. 确认技术栈

确定前端技术栈（React/Vue/Tailwind/CSS Modules 等），找到主题配置（tailwind.config、CSS 变量、设计 token）。

### 2. 扫描 UI 问题

| 类别 | 检查点 |
|---|---|
| UI 一致性 | 同含义交互用了不同视觉模式、颜色/间距/字体到处硬编码 |
| 响应式 | 写死宽度、小屏溢出、触摸目标 <44px、横向滚动 |
| CSS 质量 | 大量 `!important`、深层嵌套、内联样式泛滥、魔法值 |
| 无障碍 | 缺 `aria-label`、键盘无法导航、颜色对比度不足 |
| 交互 | 缺 loading/空/错误态、表单验证无反馈、无过渡 |
| 组件 | 粒度过粗/过细、prop 爆炸、没复用项目已有的组件库 |
| 老旧方案 | 手写 UI 但项目已有成熟组件库 |

**注意**：不做"好不好看"的主观判断。所有问题必须有代码层面的证据（不一致的值、缺的属性、不正确的结构）。

### 3. 检查造轮子情况

如果发现项目自己手写了一套 UI 组件但生态已有成熟方案（shadcn/ui、Ant Design、MUI 等），用 GitHub MCP 搜索对应的推荐，给出替换建议。

### 4. 输出改进建议

每个问题：
- **问题描述**：具体问题
- **证据**：文件路径 + CSS 值/属性缺失
- **用户影响**：这个设计问题对用户的实际影响
- **改进方案**：具体改哪个文件、用什么值替换、增什么属性

## 运行方式

`/repo-guardian:design-review` — 全项目审查

`/repo-guardian:design-review src/pages/checkout` — 只查指定页面

如果不涉及前端代码，说明"当前扫描范围不包含前端代码，跳过设计审查"。
# FDE 面试 Fieldbook

> 一部有来源、重生产、可持续更新的 Forward Deployed Engineer 面试指南。

[English](README.md) · [从这里开始](docs/zh-CN/00-start-here.md) · [2026 岗位雷达](docs/research/role-radar-2026-08.md) · [参与共建](CONTRIBUTING.md)

FDE 面试真正难的地方，不是“既考代码又考沟通”这么简单。它要确认一件更现实的事：当客户只给你一个模糊目标、混乱数据、复杂权限和紧迫时间时，你能否找准问题，亲手把最小闭环做出来，让它稳定进入生产，并把一次项目经验沉淀成下一次可以复用的产品能力。

这不是一份押题集，而是一套面试与工作的共同操作系统。项目提供：

- 基于 2026 年官方岗位信息整理的 FDE 类型与能力模型；
- 从岗位理解、客户发现、编码、数据、系统设计到生产 AI 的完整主线；
- RAG、Agent、上下文工程、MCP、A2A、评测、可观测性、长任务恢复与安全治理；
- 原创案例、逐步推演、问题详解、模拟面试脚本和可直接使用的评分表；
- 来源、时效和修改记录，让项目可以在 GitHub 上长期迭代，而不是发布后迅速过期。

## 先记住一条主线：FIELD

```text
F — Frame the mission       把任务说清：谁使用、哪段流程、什么结果算成功。
I — Inspect reality         查清现实：数据、系统、权限、约束、历史故障和组织阻力。
E — Engineer the thin slice 做最小闭环：端到端证明价值，同时控制关键风险。
L — Launch and learn        上线学习：评测、灰度、采用率、遥测、故障与迭代。
D — Distill into product    沉淀产品：可复用组件、交付手册、平台反馈和客户交接。
```

FIELD 不是为了制造缩写，而是防止候选人一听到需求就开始画 RAG 或 Agent 架构。FDE 的专业性，首先体现在能够延迟解法，先弄清现实。

## 这份指南与常见题库有什么不同

现有材料通常有三个问题：一是大量重复，读得很多却没有形成主线；二是偏重通用算法或 AI 名词，忽略客户工作流、上线采用和产品反馈；三是把来源不明的“真实面经”写成确定事实。

本项目采用另一套标准：

1. **能力模型先于题目数量。** 每个问题都要对应明确的观察维度。
2. **解释推理，不鼓励背话术。** 答案会说明先问什么、为何这样判断、边界在哪里。
3. **生产责任贯穿始终。** 不只讨论模型效果，还讨论数据同步、权限、评测、回滚、审计、成本和采用率。
4. **事实和经验分级。** 官方来源、交叉印证和社区经验不会混写。
5. **公开项目不碰版权灰区。** 不上传原始资料包、付费 PDF 或泄露题目，只发布原创重构内容。

## 快速入口

| 你的时间   | 建议路径                                                                                              | 应交付的结果                       |
| ---------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 1 小时     | 阅读[岗位地图](docs/zh-CN/01-role-map.md)，完成[总评分表](interview-kits/rubrics/master-scorecard.md) | 一份按优先级排序的差距清单         |
| 7 天       | 执行[七天冲刺](docs/zh-CN/10-study-plans.md#七天冲刺)，完成案例一                                     | 一次录像复盘 + 一页案例备忘录      |
| 30 天      | 执行[三十天计划](docs/zh-CN/10-study-plans.md#三十天计划)，完成三轮模拟                               | 覆盖全部能力维度的面试证据         |
| 已进入面试 | 使用[问题详解](docs/zh-CN/08-question-bank.md)、[案例册](docs/zh-CN/07-casebook.md)和岗位类型表       | 针对目标岗位补短板，而不是重新通读 |

## 完整目录

1. [开始之前：如何使用这套指南](docs/zh-CN/00-start-here.md)
2. [FDE 到底负责什么](docs/zh-CN/01-role-map.md)
3. [面试全景与评分逻辑](docs/zh-CN/02-interview-loop.md)
4. [客户发现与问题拆解](docs/zh-CN/03-discovery.md)
5. [编码、数据与交付基本功](docs/zh-CN/04-coding-data-delivery.md)
6. [从工作流出发做系统设计](docs/zh-CN/05-system-design.md)
7. [2026 生产 AI 必修课](docs/zh-CN/06-production-ai.md)
8. [三个完整案例](docs/zh-CN/07-casebook.md)
9. [高频问题与推理式详解](docs/zh-CN/08-question-bank.md)
10. [行为面、利益相关者与演示翻车](docs/zh-CN/09-behavioral.md)
11. [七天与三十天训练计划](docs/zh-CN/10-study-plans.md)
12. [简历、作品集与项目叙事](docs/zh-CN/11-portfolio.md)

## 练习工具

- [FDE 总评分表](interview-kits/rubrics/master-scorecard.md)
- [客户发现评分表](interview-kits/rubrics/discovery-scorecard.md)
- [系统设计评分表](interview-kits/rubrics/system-design-scorecard.md)
- [90 分钟 AI FDE 模拟面试](interview-kits/mock-loops/ai-fde-90-minute.md)
- [60 分钟经典 FDE 模拟面试](interview-kits/mock-loops/classic-fde-60-minute.md)

## 项目如何保持更新

所有时效性事实都进入 [`data/sources.json`](data/sources.json)，记录来源类型和最近核验日期。项目按月检查来源新鲜度；岗位要求、协议规范或安全基线发生变化时，通过结构化 Issue 更新。重要变化写入 [CHANGELOG](CHANGELOG.md)，后续计划放在 [ROADMAP](ROADMAP.md)。

本次素材审计、代码样例反向验收和发布验收均有公开记录：[素材审计](docs/research/corpus-audit.md) · [v0.1 验证记录](docs/research/release-validation-0.1.md)。

## 许可与声明

本项目使用 [MIT License](LICENSE)。它是独立教育资料，与文中提到的任何公司均无隶属或背书关系。招聘要求和面试流程会变化，实际安排请以招聘方当期信息为准。

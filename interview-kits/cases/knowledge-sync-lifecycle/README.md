# Field Case Lab：知识库同步与删除边界

> **场景：** 多租户 RAG 每日同步出现误删除和权限残留<br>
> **时长：** 75 分钟<br>
> **主要观察：** 稳定身份、upsert、软删除、权限撤回、快照完整性、回放与对账

## 无剧透入口

候选人只打开 [`candidate-brief.md`](candidate-brief.md)。主持人使用 [`interviewer-brief.md`](interviewer-brief.md)按轮释放合成证据。

## 训练价值

问题不是写一条 `MERGE` SQL。候选人必须先定义文档身份和生命周期，区分内容更新、源端删除、快照缺失、权限撤回和保留期，再保证检索、引用、缓存和索引在失败重跑后保持一致。

## 文件

- 候选人材料：[`candidate-brief.md`](candidate-brief.md)
- 主持人材料：[`interviewer-brief.md`](interviewer-brief.md)
- 专项评分：[`rubric.md`](rubric.md)
- 参考复盘：[`debrief.md`](debrief.md)

所有文档、租户和权限数据均为原创合成数据。

---

[返回案例目录](../README.md) · [案例运行标准](../facilitation-standard.md)

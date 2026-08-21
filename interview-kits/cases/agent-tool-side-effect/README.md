# Field Case Lab：Agent 工具副作用失控

> **场景：** 客服 Agent 自动退款出现重复执行<br>
> **时长：** 75 分钟<br>
> **主要观察：** 工作流分层、权限、幂等、部分成功、事故保护与分阶段放权

## 无剧透入口

候选人只打开 [`candidate-brief.md`](candidate-brief.md)。主持人单独使用 [`interviewer-brief.md`](interviewer-brief.md)，按轮释放证据。候选人完成前不要打开评分表、复盘或证据目录。

## 训练价值

这个案例不考“会不会接 Tool Calling”。它检查候选人是否理解：模型可以建议动作，但有财务副作用的执行必须有稳定业务身份、权限、幂等、状态确认和恢复机制。网络超时不等于工具失败，重试策略不能只看 HTTP 状态。

## 文件

- 候选人材料：[`candidate-brief.md`](candidate-brief.md)
- 主持人材料：[`interviewer-brief.md`](interviewer-brief.md)
- 专项评分：[`rubric.md`](rubric.md)
- 参考复盘：[`debrief.md`](debrief.md)

所有客户、订单和金额均为原创合成数据。

---

[返回案例目录](../README.md) · [案例运行标准](../facilitation-standard.md)

# Field Case Lab：多 Pod 长任务与断点续传

> **场景：** 浏览器断开、Pod 驱逐后 Agent 任务无法可靠恢复
> **时长：** 75 分钟
> **主要观察：** 连接与任务解耦、持久状态、事件游标、租约、幂等恢复、取消与观测

## 无剧透入口

候选人只打开 [`candidate-brief.md`](candidate-brief.md)。主持人根据 [`interviewer-brief.md`](interviewer-brief.md)释放合成拓扑、事件和故障条件。

## 训练价值

Sticky session 可以暂时把重连送回原 Pod，却没有解决 Pod 崩溃、扩缩容、重复消费者和任务所有权。这个案例要求候选人把一次长 Agent 运行当作可寻址、可恢复、可审计的持久任务，而不是一条必须保持不断的 HTTP 连接。

## 文件

- 候选人材料：[`candidate-brief.md`](candidate-brief.md)
- 主持人材料：[`interviewer-brief.md`](interviewer-brief.md)
- 专项评分：[`rubric.md`](rubric.md)
- 参考复盘：[`debrief.md`](debrief.md)

---

[返回案例目录](../README.md) · [案例运行标准](../facilitation-standard.md)

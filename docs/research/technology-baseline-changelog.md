# 技术基线变更账本

核验日期：2026-08-21

这份账本不追逐每次 SDK 发版，而是记录会改变生产设计或面试答案边界的规范变化。机器可读版本见 [`data/technology-baselines.json`](../../data/technology-baselines.json)。

## 当前基线

| 领域 | 当前基线 | 状态 | 面试和生产决策里必须更新的认知 |
| --- | --- | --- | --- |
| MCP | 2026-07-28 specification | 当前正式版本 | 核心协议无状态；任务状态要显式建模；授权和弃用项需要迁移计划 |
| A2A | 1.0 | 首个稳定版本 | 面向跨 Agent/组织边界的互操作；版本、身份、租户和任务生命周期不能省略 |
| OpenTelemetry GenAI | 独立 GenAI 语义约定仓库 | 持续演进 | 不能假装字段集合已经冻结；要固定修订、做内部映射并控制敏感内容 |
| OWASP Agentic Security | Agentic Applications Top 10 2026 | 当前安全指导 | 威胁面扩展到目标、工具、身份、供应链、内存、Agent 间通信和级联动作 |

## 2026-08-21：A2A 进入 1.0，边界比“多 Agent”更重要

[A2A 1.0](https://a2a-protocol.org/v1.0.0/)是首个稳定版本，加入多协议绑定、版本协商、多租户和签名 Agent Card，并支持轮询、流式和 webhook 获取任务结果。

生产含义不是“以后都要用 A2A”。恰恰相反，只有当 Agent 之间存在独立产品、平台、供应商或组织边界时，互操作协议才值得引入。一个进程里的 planner 和 worker 通常用普通函数或队列契约更简单。真正采用 A2A 时，需要验证 Agent 身份与元数据，传递租户和授权范围，持久化任务状态，并处理 webhook 重放和版本兼容。

## 2026-08-21：OpenTelemetry GenAI 从主规范移到独立仓库

OpenTelemetry 的 GenAI 语义约定已经迁移到[独立仓库](https://github.com/open-telemetry/semantic-conventions-genai)，覆盖 GenAI client、Agent、MCP、provider、span、metric 和 event。仓库仍在处理 schema versioning，因此当前更准确的状态是“持续演进的规范工程”，不是一套可以无脑升级的冻结字段。

生产系统应固定所采用的修订，在内部定义稳定遥测契约，再把不同 provider 和框架映射进去。prompt、检索词、工具参数和输出可能包含敏感信息，是否采集、保存多久、谁能读取都必须先有政策。可观测性不能变成新的数据泄露面。

## 2026-07-28：MCP 改成无状态核心

[MCP 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/)移除了依赖握手与隐藏 session 的核心模型，引入 Multi Round-Trip Requests、可用于网关路由的 method/name header、列表缓存提示、正式扩展框架和更严格的授权规则。Tasks 进入扩展；Roots、Sampling、Logging 与 legacy HTTP+SSE 进入弃用路径。

这会改变生产架构：远程 MCP server 不再因为协议本身要求 sticky session，但业务任务仍然可能有状态。状态应通过显式 task/handle、持久化事件与应用数据库管理，不能因为传输无状态就假装业务也无状态。授权侧要验证 issuer、绑定凭证来源，并为从 DCR 迁移到 CIMD 留出计划。

## 2026-08-21：Agent 安全采用独立风险基线

[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)把安全视角从“模型输入输出”扩展到目标劫持、工具误用、身份和权限、供应链、代码执行、记忆污染、Agent 间通信、级联故障、人机信任和 rogue agent。

使用方式不是逐条贴合规标签，而是把每类风险连接到可执行控制：最小权限、来源锁定、结构化参数校验、审批、沙箱、动作预算、跨 Agent 身份、对抗评测、运行时检测、kill switch、审计和恢复。Top 10 是覆盖清单，不是安全认证。

## 维护规则

只有下列变化进入账本：

- 正式规范或安全基线发布；
- 稳定性等级、授权模型或任务生命周期发生变化；
- 重要能力弃用，要求生产迁移；
- 官方观测契约变化，会影响 trace、指标或隐私；
- 新风险分类足以改变威胁模型和测试门禁。

单个 SDK 的补丁版本、厂商营销命名和未经验证的社区预测不进入这里。若来源之间冲突，按[争议事实评审流程](claim-review-process.md)保留适用范围和未决状态。

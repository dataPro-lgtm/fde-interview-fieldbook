# 双语核心路径与来源档案维护契约

## 1. 双语对齐对齐什么

本项目不把逐句翻译当作质量目标。中文和英文篇幅、案例顺序可以不同，但 `full` 必须同时满足：

1. 学员完成后能做出相同的关键决定；
2. 风险、事实边界和禁止推断没有在翻译中消失；
3. 至少有一条可执行练习路径；
4. 产物和完成证据可以被另一人检查；
5. 相关评分、案例或模板链接有效。

`condensed` 表示保留主结论但缺少部分练习或深度，`planned` 表示尚未提供可用路径。状态记录在 `data/content-parity.json`，不能只在 README 里口头声称。

## 2. 核心路径范围

v0.9 的核心范围是中文编号 `00` 到 `15` 的十六章。英文可以用盲练案例替代中文的讲解案例，只要学习结果仍然覆盖 FIELD 推演、分轮证据更新、评分和复盘。问题数量也不要求相同，但岗位、发现、工程、RAG/评测、Agent/安全和现场判断六类决策不能缺失。

新增非核心附录不自动要求翻译。若它进入 README、学习地图或机器学习路径并成为必经产物，就必须进入对照清单或明确降级。

## 3. 术语约定

| 概念 | 英文主写法 | 中文主写法 | 边界 |
| --- | --- | --- | --- |
| FDE | Forward Deployed Engineer | FDE / 前线部署工程师 | 不假设所有公司职责相同 |
| thin slice | thin slice | 端到端最小切片 | 不是把大系统每层都做一点 |
| owner | accountable owner / operator | 负责人 / 运营责任人 | 避免只有抽象“团队负责” |
| gate | release / expansion / stop gate | 发布 / 扩大 / 停止门禁 | 必须带证据和动作 |
| rollout | staged rollout | 分阶段发布 / 灰度 | 不等同于一次部署 |
| evidence flow | evidence flow | 证据流 | trace、eval、audit、adoption 可关联 |
| unknown outcome | final result unknown | 最终状态未知 | 不得直接当失败重试 |
| N/O | Not Observed | 未观察到 | 不等于 1 分 |
| productization | productization | 产品化 | 需要第二消费者、owner 和迁移 |
| durable execution | durable execution | 持久执行 | 任务生命期不依附连接或单 Pod |

不要为了语言自然删除 certainty、risk、owner、non-goal、rollback 和 not verified。中文“生产级”也不能翻译成 production-ready，除非相关生产契约和验证真的存在。

## 4. 无障碍与移动阅读检查

每次双语核心变更检查：

- 标题按层级递进，不用加粗代替标题；
- 链接文本能说明目标，不连续堆“点这里”；
- 图旁边有能独立传达结论的文字；
- 表格用于对照，不把整段论证塞进单元格；
- 不依赖颜色、emoji 或排版位置表达风险；
- 代码与命令可复制，示例明确是否真实、合成或占位；
- 中英文页面都能从学习地图进入，并能回到下一步；
- 警告、外部验证缺口和隐私边界保持一致。

通用基线见 [ACCESSIBILITY.md](../../ACCESSIBILITY.md)。

## 5. 来源年度档案

`data/source-archives/<year>.json` 只保存：来源 ID、发布者、标题、公开 URL、类型、权威等级、最近检查日期，以及 `data/sources.json` 的 SHA-256。它不保存网页正文、长引文、HTML、登录内容、付费资料、凭证、真实面试题或客户材料。

年度内更新来源账本时，同步刷新当年元数据投影和摘要。年份结束后不覆盖旧档；新增下一年文件。URL 后来失效时保留历史记录，在当前账本和变更日志说明替代来源，不悄悄改写历史。

## 6. 变更流程

1. 确认改动是否改变注册的 learner outcome、边界、练习或完成证据；
2. 同步修改双语页面，或把状态降为 `condensed` / `planned`；
3. 更新 `data/content-parity.json` 的范围说明和资产；
4. 来源变化时更新当前账本与当年档案摘要；
5. 运行 `python3 scripts/validate_parity_archive.py`；
6. 再运行仓库链接、Markdown、Mermaid 和全部测试；
7. 在验收记录中分开写机器通过、人工审阅和未验证的读者效果。

机器校验能证明十六对路径存在、结构足够、练习资产有效、来源摘要未漂移；它不能证明两种语言的真实读者都能独立完成训练。后者仍需非作者按协议试用。

---

[对照清单](../../data/content-parity.json) · [英文学习地图](../en/reading-map.md) · [中文学习地图](../zh-CN/reading-map.md) · [版本执行计划](version-plan-0.6-to-1.0.md)

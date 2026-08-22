# v0.9 双语核心路径与来源档案验收记录

> **状态：** A1 十六对学习结果、双语导航与来源档案自动化验收通过；双语读者独立试用未执行<br>
> **核验日期：** 2026-08-22<br>
> **适用范围：** 中文 `00`—`15` 核心章节、十六个英文对应路径、双语对照清单、术语与无障碍契约、2026 来源元数据档案

## 1. v0.9 解决什么问题

此前英文路径只覆盖岗位、面试流程、系统设计、生产 AI、作品集、岗位定向和引导式训练。英文读者遇到发现、现场编码、案例盲练、行为面、答案校准和企业交付时仍需跳回中文，项目却没有一份机器可读的缺口清单。

v0.9 补齐八个英文高频章节，并将全部十六个中文核心结果登记到 `data/content-parity.json`。对齐对象是“读者完成后能做什么、用什么练、怎样判断完成”，不是篇幅或逐句翻译。

## 2. 十六对核心学习结果

| 主线 | 中文路径 | 英文路径 | 必须形成的能力 |
| --- | --- | --- | --- |
| 起点与岗位 | 开始、岗位地图、面试流程 | start、role map、interview loop | 目标岗位、证据缺口、轮次到行为 |
| 发现与工程 | 发现、编码与数据、系统设计 | discovery、coding/data、system design | mission、thin slice、可测试实现、三条流 |
| 生产 AI | 生产 AI | production AI 2026 | RAG/Agent/协议/评测/安全/恢复的生产判断 |
| 案例与问题 | 三个讲解案例、问题库 | Field Case Lab、question bank | FIELD 推演、分轮更新、二层追问 |
| 现场领导 | 行为面、训练计划、作品集 | field leadership、study plans、portfolio | 冲突、失败、修复循环、项目证据 |
| 校准与落地 | 答案校准、企业作战手册 | answer calibration、field operating playbook | 原话评分、发布恢复、采用、交接、产品化 |
| 岗位与路径 | 岗位定向、引导式训练 | job targeting、guided practice | 一条 JD 到证据战役、7/14/30 天产物 |

中文讲解案例与英文盲练案例不是文本镜像，但都必须让学员完成 FIELD、证据更新、评分和复盘。英文问题库数量较少，但保留岗位发现、编码数据、RAG 评测、Agent 安全和现场判断等高频决策域。

## 3. 对照数据契约

每个核心对照项必须具备：

- 唯一 ID、唯一中文路径和唯一英文路径；
- `full`、`condensed` 或 `planned` 的明确状态；
- 说明两种语言范围差异的 `scope_note`；
- 至少三个不重复的 learner outcomes；
- 至少一个存在的练习资产；
- `full` 英文篇章的最低正文与章节结构；
- 中文编号 `00`—`15` 全覆盖，不允许未登记章节。

当前 v0.9 十六对均为 `full` learner-outcome parity。这里的 `full` 不代表每句话、例子或问题数量完全相同，也不代表翻译已由真实双语学员验证。

## 4. 来源档案边界

`data/source-archives/2026.json` 保存十七条公开来源的 ID、发布者、标题、URL、类型、权威等级和最近检查日期，并绑定 `data/sources.json` 的 SHA-256。校验器会比较条目数量、ID 集合、元数据投影和账本摘要。

档案明确排除网页正文、HTML、长引文、登录内容、付费资料、凭证、客户材料和真实面试题。它证明“本版本使用哪一份来源账本”，不保证外部网页未来持续可用；链接健康与来源时效仍由各自定时检查负责。

## 5. 术语与无障碍审阅

本轮对核心双语路径检查：

1. FIELD、thin slice、owner、gate、rollout、evidence flow、N/O、productization 和 durable execution 的含义保持一致；
2. `production-ready`、雇主流程和外部效果不会因翻译被扩大；
3. 标题层级、描述性链接、表格用途和文本导航可独立使用；
4. 图、状态和风险不只依赖颜色；
5. 命令可复制，合成、练习和真实证据边界明确；
6. 英文地图可以进入全部十六项并返回后续练习；
7. 中文入口能够找到对照契约和 v0.9 验收记录。

维护规则和术语表记录在 `docs/research/bilingual-maintenance.md`，通用要求仍由 `ACCESSIBILITY.md` 约束。

## 6. 自动化验证

```bash
python3 scripts/validate_repo.py
python3 scripts/validate_case_packs.py
python3 scripts/validate_research_data.py
python3 scripts/validate_role_playbooks.py
python3 scripts/validate_learning_paths.py
python3 scripts/validate_calibration.py
python3 scripts/validate_parity_archive.py
python3 scripts/check_external_links.py --timeout 12 --workers 6
python3 -m unittest discover -s tests -v
npx --yes markdownlint-cli2@0.18.1 "**/*.md" "#node_modules"
npx --yes markdownlint-cli2@0.23.2 "**/*.md" "#node_modules"
python3 scripts/validate_mermaid.py --all --no-browser-sandbox
python3 -m py_compile scripts/*.py tests/*.py
git diff --check
```

观察门槛：十六对 learner-outcome parity 和十七条来源元数据通过契约；十项边界测试覆盖缺对照、学习结果不足、路径重复、练习资产、隐藏精简状态、摘要漂移、元数据漂移、禁止正文和数量不符；21 条公开外部链接无硬失败或软失败；既有案例、角色、训练和校准回归继续通过。

## 7. 尚未验证的部分

当前没有提交真实双语读者试用记录，因此尚不能证明：

- 英文读者不需要作者解释即可完成全部练习；
- 两种语言对同一评分锚点不会产生系统性理解差异；
- 英文盲练案例与中文讲解案例对不同基础读者同样有效；
- 移动端、屏幕阅读器和打印环境已由真实使用者全面测试；
- 双语材料提高任何面试、就业或交付结果。

若核心一侧出现缺口，未来维护者必须修复或把状态降为 `condensed` / `planned`，不得维持虚假的全量对齐。

## 8. 发布判断

v0.9 达到 A1 双语核心路径与来源档案发布候选门槛，可以进入 v1.0 可重现发布清单和全量验收。对外可以表述为“十六对机器登记、带练习和完成标准的中英文核心学习路径”，不能表述为“经过双语学员验证”或“逐字完整翻译”。

---

[英文学习地图](../en/reading-map.md) · [双语维护契约](bilingual-maintenance.md) · [对照清单](../../data/content-parity.json) · [版本执行计划](version-plan-0.6-to-1.0.md)

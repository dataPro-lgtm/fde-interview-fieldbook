# Forward Deployed Engineer (FDE) Interview Fieldbook

> A source-backed, production-first field guide for Forward Deployed Engineer interviews.

[简体中文](README.zh-CN.md) · [English reading map](docs/en/reading-map.md) · [Guided practice](docs/en/guided-practice.md) · [Job targeting](docs/en/job-targeting.md) · [Start here](docs/en/start-here.md) · [Role playbooks (Chinese)](interview-kits/role-playbooks/README.md) · [Field Case Lab (Chinese)](interview-kits/cases/README.md) · [Contributing](CONTRIBUTING.md)

FDE interviews do not only ask whether you can write code. They test whether you can enter an ambiguous customer environment, find the real workflow, ship a thin but valuable system, keep it reliable in production, and turn field learning into reusable product capability.

This repository is a living handbook for that whole job. It combines:

- a current, source-backed map of FDE role archetypes;
- a practical interview operating system rather than a leaked-question dump;
- production AI coverage: RAG, agents, context engineering, MCP, A2A, evals, observability, durable execution, security, and data operations;
- original walkthroughs and facilitator-ready case packs with staged evidence, role-separated briefs, and case-specific rubrics;
- a transparent update process so time-sensitive claims can be reviewed and refreshed.

## Why another FDE guide?

Most preparation material over-indexes on one of two halves:

1. generic software interviews: algorithms, APIs, and system design; or
2. generic AI interviews: model vocabulary, prompting, and toy chatbots.

The actual field role sits between the customer, the product, and production engineering. Current official role descriptions make that boundary clear:

- OpenAI describes ownership from discovery and technical scoping through build, rollout, adoption, and eval-driven feedback.
- Anthropic asks FDEs to deliver production artifacts such as MCP servers, sub-agents, and agent skills.
- Scale AI emphasizes customer-specific data infrastructure and distributed systems.
- Vercel combines embedded customer work with production agents, MCP servers, migrations, and knowledge transfer.
- Diligent explicitly calls for golden datasets, regression infrastructure, guardrails, tracing, and judgment about when a workflow needs an agent at all.
- Palantir describes FDE as the human equivalent of backpropagation: field feedback must become product capability.

The evidence and freshness dates are recorded in [`data/sources.json`](data/sources.json). Quarterly radar data is versioned under [`data/role-radar`](data/role-radar), and protocol/security baselines live in [`data/technology-baselines.json`](data/technology-baselines.json). These are bounded snapshots, not claims that every employer or geography follows the same pattern.

## The FIELD loop

The handbook uses one reusable line of reasoning across case interviews, system design, project stories, and production incidents:

```text
F — Frame the mission       Who decides? Which workflow? What outcome matters?
I — Inspect reality         Data, systems, users, permissions, constraints, failure history.
E — Engineer the thin slice Smallest end-to-end path that proves value and risk controls.
L — Launch and learn        Evals, rollout, adoption, telemetry, incidents, iteration.
D — Distill into product    Reusable primitives, playbooks, platform feedback, handoff.
```

It is not a script to memorize. It is a safeguard against the most common FDE failure: drawing architecture before understanding the job that must change.

## Choose your path

| Time available | Recommended path | Output |
| --- | --- | --- |
| 60 minutes | Read the [role map](docs/en/role-map.md), then score yourself with the [master rubric](interview-kits/rubrics/master-scorecard.md) | A prioritized gap list |
| 7 days | Follow the [7-day sprint](docs/zh-CN/10-study-plans.md#七天冲刺) and run one [Field Case Lab](interview-kits/cases/README.md) | One recorded mock plus one scored case memo |
| 30 days | Follow the [30-day plan](docs/zh-CN/10-study-plans.md#三十天计划), run three mock loops, and build a portfolio narrative | Interview-ready evidence across all dimensions |
| Already interviewing | Use the [question bank](docs/zh-CN/08-question-bank.md), [worked cases](docs/zh-CN/07-casebook.md), and [blind case labs](interview-kits/cases/README.md) | Targeted practice, not broad rereading |
| One target role | Turn its public JD into an [evidence-based campaign](docs/en/job-targeting.md), then select one [role playbook](interview-kits/role-playbooks/README.md) | A role brief, evidence matrix, and ten scored sessions |
| I keep reading but do not practise | Choose one [guided 7-, 14-, or 30-day path](docs/en/guided-practice.md) | Ordered artifacts, completion evidence, and a repair cycle |

English-first readers can use the [English reading map](docs/en/reading-map.md) for the translated high-use path. The project labels untranslated depth instead of implying full parity.

## Handbook map

### Core guide

| Chapter                                                                          | What you should be able to do afterwards                                                   |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [Start here](docs/zh-CN/00-start-here.md)                                        | Diagnose your target role and create a study backlog                                       |
| [What an FDE actually owns](docs/zh-CN/01-role-map.md)                           | Distinguish FDE archetypes and explain the field-to-product loop                           |
| [Interview loop and scoring](docs/zh-CN/02-interview-loop.md)                    | Understand what each round is trying to observe                                            |
| [Discovery and decomposition](docs/zh-CN/03-discovery.md)                        | Turn a vague request into a bounded mission and acceptance criteria                        |
| [Coding, data, and delivery](docs/zh-CN/04-coding-data-delivery.md)              | Demonstrate fast, testable implementation and messy-data judgment                          |
| [System design](docs/zh-CN/05-system-design.md)                                  | Design from workflow and risk, not from a memorized architecture                           |
| [Production AI in 2026](docs/zh-CN/06-production-ai.md)                          | Reason about RAG, agents, MCP, context, evals, security, and durability                    |
| [Casebook](docs/zh-CN/07-casebook.md)                                            | Walk through three realistic customer problems end to end                                  |
| [Question bank with guided answers](docs/zh-CN/08-question-bank.md)              | Practice high-signal answers without memorizing slogans                                    |
| [Behavioral, stakeholder, and demo recovery](docs/zh-CN/09-behavioral.md)        | Show ownership, judgment, conflict handling, and calm under pressure                       |
| [7-day and 30-day study plans](docs/zh-CN/10-study-plans.md)                     | Convert reading into observable interview performance                                      |
| [Resume and portfolio evidence](docs/zh-CN/11-portfolio.md)                      | Present proof of field impact rather than a technology inventory                           |
| [Answer calibration pack](docs/zh-CN/12-answer-calibration.md)                   | Compare weak, independent, and leverage-creating answers using evidence                    |
| [Enterprise field operating playbook](docs/zh-CN/13-field-operating-playbook.md) | Carry interview reasoning into discovery, launch, incidents, handoff, and product feedback |

The Chinese core path continues with [job targeting](docs/zh-CN/14-job-targeting.md) and the [guided-practice system](docs/zh-CN/15-guided-practice.md).

### English high-use path

- [Start here](docs/en/start-here.md)
- [FDE role map](docs/en/role-map.md)
- [Interview loop and scoring](docs/en/interview-loop.md)
- [Workflow-first system design](docs/en/system-design.md)
- [Production AI in 2026](docs/en/production-ai-2026.md)
- [Resume, portfolio, and project evidence](docs/en/portfolio-evidence.md)
- [Turn one job description into an evidence-based campaign](docs/en/job-targeting.md)
- [Turn reading into guided, evidence-producing practice](docs/en/guided-practice.md)

### Practice kits

- [Field Case Lab: ten production case packs with staged evidence](interview-kits/cases/README.md)
- [Case facilitation standard](interview-kits/cases/facilitation-standard.md)
- [Master scorecard](interview-kits/rubrics/master-scorecard.md)
- [Customer discovery scorecard](interview-kits/rubrics/discovery-scorecard.md)
- [System design scorecard](interview-kits/rubrics/system-design-scorecard.md)
- [90-minute AI FDE mock loop](interview-kits/mock-loops/ai-fde-90-minute.md)
- [60-minute classic FDE mock loop](interview-kits/mock-loops/classic-fde-60-minute.md)
- [Reviewer calibration guide](interview-kits/rubrics/reviewer-calibration.md)
- [Blind scoring, adjudication, and re-score protocol](interview-kits/rubrics/calibration-protocol.md)
- [Cross-role evidence anchor library](interview-kits/rubrics/evidence-anchor-library.md)
- [Field delivery worksheet pack](interview-kits/worksheets/field-delivery-pack.md)
- [Role-targeting playbooks for AI, data-platform, and regulated deployment FDEs](interview-kits/role-playbooks/README.md)
- [Job-targeting worksheet pack](interview-kits/worksheets/job-targeting-pack.md)
- [Three role-targeted blind mock loops and pilot protocol](interview-kits/mock-loops/role-targeted/README.md)
- [Practice journal for first attempt, evidence, score, repair, and retry](interview-kits/worksheets/practice-journal.md)

### Research and maintenance

- [Corpus audit and design decisions](docs/research/corpus-audit.md)
- [Quarterly role-radar archive](docs/research/role-radar/README.md)
- [Technology baseline changelog](docs/research/technology-baseline-changelog.md)
- [Source policy](docs/research/source-policy.md)
- [Claim-review process](docs/research/claim-review-process.md)
- [Documentation-site evaluation](docs/research/documentation-site-evaluation.md)
- [v0.1 validation record](docs/research/release-validation-0.1.md)
- [v0.5 role-targeting validation record](docs/research/release-validation-0.5.md)
- [v0.6 guided-practice validation record](docs/research/release-validation-0.6.md)
- [v0.7 production-case validation record](docs/research/release-validation-0.7.md)
- [v0.8 reviewer-calibration validation record](docs/research/release-validation-0.8.md)
- [v0.6-to-v1.0 execution plan](docs/research/version-plan-0.6-to-1.0.md)
- [Roadmap](ROADMAP.md)
- [Accessibility](ACCESSIBILITY.md)

## What this repository deliberately does not do

- It does not claim that an unofficial interview loop is company policy.
- It does not republish paid PDFs, copyrighted bundles, or confidential interview questions.
- It does not promise that memorizing model answers will pass an interview.
- It does not equate a framework name with good judgment.
- It does not treat every workflow as an agent problem.

## Living-project contract

Time-sensitive claims carry a source and `last_checked` date. Quarterly role snapshots are immutable additions, while protocol and security baselines keep a dated change log. Role playbooks separately register first-party signals, interview hypotheses, evidence boundaries, and practice assets. Guided paths separately register ordered sessions, learner outputs, and completion evidence. Monthly source-freshness and weekly public-link audits open maintenance issues when evidence ages out or a URL is confirmed dead. Changed Mermaid diagrams are rendered in CI, and versioned research and practice data is machine-checked. Contributors can propose a role update or dispute an overbroad claim using structured forms. Material changes are recorded in the changelog.

The project follows three confidence labels:

- **Official**: employer posting, protocol specification, standards body, or vendor documentation.
- **Corroborated**: multiple credible sources agree, but the employer has not published the detail.
- **Community**: useful practitioner experience; never presented as official policy.

## Contributing

Corrections, fresh role evidence, original cases, translations, and clearer explanations are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Do not submit leaked or proprietary interview content.

## License and disclaimer

Released under the [MIT License](LICENSE). This is independent educational material and is not affiliated with or endorsed by any employer mentioned in the guide. Job descriptions and interview processes change; verify current details with the recruiter.

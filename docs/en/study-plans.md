# Evidence-first study plans

> **Use this when:** your preparation plan counts pages, videos, or questions instead of observable performance.<br>
> **Produce:** scheduled artifacts, recordings, scores, and a repair backlog.<br>
> **Choose:** a seven-day sprint for an imminent interview or a thirty-day cycle for a transition.

The unit of preparation is not a chapter. It is an artifact another person can inspect: code, a workflow, a design, a recording, a score, or a decision memo. Reading belongs inside a repair loop after the first attempt exposes a gap.

## Seven-day sprint

Plan two to three focused hours per day.

| Day | Focus | Required output | Exit condition |
| --- | --- | --- | --- |
| 1 | Role and baseline | Target-role sentence, scorecard, 90-second recording | Only three high-risk gaps remain |
| 2 | Discovery | Workflow, mission, thin slice, recorded discovery | No technology chosen in first five minutes |
| 3 | Coding and data | Runnable code, tests, error log | Invariant and failure semantics are clear |
| 4 | System design | Data/control/evidence flows, decision record | Every major component traces to a constraint |
| 5 | Production AI | Five answers and one control map | No unscoped “cache/model/guardrail” answer |
| 6 | Behavior and field pressure | Five story cards, two recordings | Contribution and mechanism change are explicit |
| 7 | Full mock and replay | Independent score, debrief, two repaired behaviors | Change is observable, not just smoother delivery |

### Day 1: establish target and baseline

Use the [role map](role-map.md) and [master scorecard](../../interview-kits/rubrics/master-scorecard.md). Separate direct evidence, adjacent evidence, exercises, and gaps. Record a 90-second position statement and keep only three risks.

### Day 2: practise discovery before design

Use [discovery](discovery.md) on one case. Produce a current workflow, fact/hypothesis ledger, mission, thin slice, and non-goals. The reviewer should ask which unanswered fact could invalidate the slice.

### Day 3: make engineering behavior visible

Run one timed task in the target language and one dirty-data task with duplicates, updates, deletes, and malformed input. Submit the code, command, tests, and error classification.

### Day 4: design three flows

Use [system design](system-design.md). Draw data flow, control/state flow, and evidence flow. End with permission, rollout, fallback, recovery, and adoption—not another component.

### Day 5: production AI under follow-up

Select RAG, agent execution, protocol, long-running state, and security questions from the [question bank](question-bank.md). Pin a past project to specific prompt/model/data/tool/eval versions and define one rollback gate.

### Day 6: pressure-test stories

Prepare ambiguity, incident, conflict, refusal, speed/quality, adoption, failure, and productization evidence. Record five cards and at least one story in 90-second and eight-minute formats.

### Day 7: run a blind loop

Use a [mock loop](../../interview-kits/mock-loops/ai-fde-90-minute.md) or one [Field Case Lab](../../interview-kits/cases/README.md). Lock independent scoring before the debrief. Repair only the two highest-risk behaviors and replay the weakest segment.

## Thirty-day cycle

Plan ten to fifteen focused hours per week.

| Week | Capability | Core evidence | Exit condition |
| --- | --- | --- | --- |
| 1 | Role, discovery, stakeholders | Role brief, evidence ledger, three missions | You stop drawing architecture on first hearing |
| 2 | Coding, data, system design | Six coding runs, two designs, error taxonomy | Code runs; three flows and data semantics are explicit |
| 3 | Production AI, security, recovery | Eval set, threat model, durable state, mock | You can locate first divergence and choose no agent |
| 4 | Integration, narrative, targeting | Cases, portfolio spine, three blind scores | Answers remain bounded under unfamiliar follow-up |

### Week 1: build the role-to-mission spine

- compare three current role descriptions without inferring internal interview policy;
- create a direct/adjacent/practice/gap evidence ledger;
- complete three workflow and mission exercises;
- run a first 60-minute baseline.

### Week 2: strengthen the engineering skeleton

- complete six timed tasks across algorithms, data handling, applied building, and debugging;
- run two workflow-first designs;
- whiteboard identity, idempotency, ordering, delete, and replay;
- write one architecture decision record from your own work.

### Week 3: make AI production responsibility explicit

- design a layered RAG evaluation set;
- threat-model one tool-using agent;
- explain durable task execution across browser and pod loss;
- add version, trace, permission, evaluation, and rollback evidence to a past project;
- run a second mock.

### Week 4: integrate and target

- complete three one-page case memos and one blind lab;
- build a ten-minute project presentation with an appendix;
- rewrite resume evidence for one live role;
- run two different mock formats;
- close every rating-1 risk before broadening topics.

## Daily record

```text
Date and target dimension:
Time-boxed task:
First output and exact score evidence:
Two largest failure patterns:
Knowledge or evidence repaired:
Second output:
One reusable rule:
Continue, switch, or stop tomorrow — why:
```

Use the [practice journal](../../interview-kits/worksheets/practice-journal.md) for a fuller template.

## Calibrate peer feedback

Feedback must quote behavior before judging it.

Weak: “The architecture was not senior enough.”

Useful: “At minute three you selected multiple agents, but by minute eighteen you had not identified any step requiring dynamic planning or defined state, termination, or duplicate-action control.”

If reviewers differ by more than one level, use the [calibration protocol](../../interview-kits/rubrics/calibration-protocol.md). Do not average away a disagreement about risk.

## Decide whether to postpone an interview

Consider postponement when:

- the target language cannot produce and test a medium task within the format;
- no project can show personal decisions and verified results;
- system designs repeatedly omit identity, state, or release control;
- the target role is misunderstood;
- one follow-up collapses every key answer into terminology.

If postponement is impossible, repair veto risks rather than adding new topics.

## Completion check

The plan is complete only if it contains first attempts, inspectable outputs, independent scoring where available, two-behavior repair cycles, and an honest gap ledger. Hours spent and pages read are context, not completion evidence.

For machine-checked session order and alternate pacing, use the [guided-practice paths](guided-practice.md).

---

[← Behavioral and field leadership](behavioral-field-leadership.md) · [English reading map](reading-map.md) · [Portfolio evidence →](portfolio-evidence.md)

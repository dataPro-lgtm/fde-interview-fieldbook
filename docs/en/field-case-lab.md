# Field Case Lab: practise decisions before seeing the answer

> **Use this when:** worked examples feel clear but new evidence still breaks your reasoning.<br>
> **Produce:** a decision log, artifacts, scorecard, and repair plan from one blind case.<br>
> **Time:** 60 to 90 minutes with a facilitator; 20 minutes for the debrief.

Worked cases teach a reasoning pattern. A lab tests whether you can use that pattern while facts change. The repository contains ten original, synthetic production cases covering plans, incidents, adoption, governance, and field-to-product work. Candidate material is separated from facilitator evidence and reference debriefs.

## What the lab observes

A strong performance does more than draw a plausible architecture. It shows whether you can:

- delay a solution until the mission and current workflow are clear;
- ask questions that unlock material evidence;
- revise a decision when new facts contradict it;
- distinguish reversible experiments from irreversible exposure;
- define acceptance, rollout, recovery, ownership, and adoption;
- turn one customer-specific lesson into a bounded reusable capability.

The final answer matters less than the quality of the update path.

## The ten-case portfolio

| Case | Primary tension | Best for observing |
| --- | --- | --- |
| Data-platform migration | Change systems without corrupting downstream meaning | Dual run, reconciliation, cutover, rollback |
| Air-gapped AI deployment | Deliver useful AI under supply-chain and operating constraints | Reproducibility, evaluation, ownership |
| Production incident | Several plausible causes and pressure to restore | Triage, first divergence, evidence preservation |
| Agent tool side effect | Retrying an uncertain write can repeat harm | Operation identity, idempotency, fencing, approval |
| Knowledge sync lifecycle | Content, delete, and permission state diverge | Tombstones, snapshot boundaries, reconciliation |
| Durable agent streaming | Browser and pod lifetime differ from task lifetime | Durable state, event replay, lease fencing |
| Evaluation regression | One headline metric collapses after change | Measurement validation, slicing, pinned replay |
| Cross-border AI deployment | Regional data and ownership boundaries constrain design | Purpose limitation, minimum sharing, staged rollout |
| Adoption rescue | Technically correct system is bypassed by users | Workflow observation, experiment, stop criteria |
| Connector productization | One-off integration must support a second source | Stable core, source adapter, migration contract |

Open the [case index](../../interview-kits/cases/README.md) to select the complete package.

## Protect the blind boundary

The candidate may read only the candidate brief at the start. The facilitator controls:

- the interviewer brief;
- staged artifacts;
- case-specific rubric;
- reference debrief.

Do not reward keyword guessing. Release evidence when the candidate asks a materially valid question or when the scheduled pressure event occurs. If the question is directionally useful but vague, ask the candidate to make it testable.

## Candidate operating loop

Use FIELD as a loop, not five presentation sections.

### Frame

State the current mission, user, decision owner, success evidence, non-goals, and highest uncertainty. Mark facts and assumptions separately.

### Inspect

Ask about workflow, identity, source of truth, permissions, failure history, volume, versions, adoption, and support. Explain which decision each question could change.

### Engineer

Select the smallest end-to-end slice that resolves the largest uncertainty. Define data, control, state, and evidence flows. Name where human approval, deterministic logic, or no AI is preferable.

### Launch

Specify offline gates, shadow or limited rollout, expansion and stop conditions, fallback, trace fields, operator, and incident path. A launch date without a stop rule is incomplete.

### Distill

Separate stable core, customer configuration, temporary workaround, and a field signal that should influence product. Do not call copied customer code a platform.

## Maintain a decision log

For every major change, record:

```text
Timestamp / round:
New evidence:
Previous decision:
Updated decision:
Why the evidence changed it:
Risk introduced or removed:
Next evidence required:
```

Changing your mind is positive evidence when the change follows new facts. Quietly rewriting history is not.

## Facilitator protocol

1. Confirm time box, role level, and target scorecard dimensions.
2. Keep candidate and facilitator material physically separate.
3. Release only the evidence earned or scheduled by the case.
4. Record exact candidate statements and artifacts, not personality impressions.
5. Apply a pressure event without coaching the answer.
6. Lock the first score before opening the reference debrief.
7. Ask the candidate to repair only two behaviors and replay one segment.

The complete contract is in the [facilitation standard](../../interview-kits/cases/facilitation-standard.md).

## Common failure patterns

- **Architecture-first:** components appear before user, baseline, or decision owner.
- **Question theatre:** many questions are asked, but none are tied to a decision.
- **Static plan:** new evidence arrives, yet the candidate does not update scope or control.
- **Retry optimism:** failure is answered with “retry” despite unknown side effects.
- **Metric substitution:** model quality replaces workflow outcome and adoption.
- **Control checklist:** security, eval, and observability are named without identity, state, or owner.
- **Productization theatre:** the one-off is declared reusable without a second consumer or migration path.

## Debrief without copying the reference answer

Compare mechanisms, not wording:

1. Which question unlocked the most valuable evidence?
2. Which decision should have changed sooner?
3. Which failure state had no owner or recovery path?
4. What was treated as a fact but was only an assumption?
5. Which two observable behaviors will change in the replay?

Use the case rubric and [master scorecard](../../interview-kits/rubrics/master-scorecard.md). If two reviewers disagree, follow the [calibration protocol](../../interview-kits/rubrics/calibration-protocol.md) rather than averaging.

## Practice

Run one case under these restrictions:

- candidate gets no artifact directory access;
- facilitator gives no architecture hints;
- candidate must produce a mission, thin-slice contract, three-flow design, launch gates, and decision log;
- candidate receives one pressure event and one contradictory artifact;
- first score is locked before the debrief;
- a ten-minute replay changes exactly two behaviors.

## Completion check

The run is complete only when the record shows:

- what evidence was available at each decision;
- at least one explicit update after new evidence;
- a release and recovery owner;
- a score tied to exact statements or artifacts;
- two repair behaviors and their replay result;
- no confidential employer, customer, or real interview material.

Automated package validation proves structure, not independent facilitation quality. Every case currently declares its human-validation status in `data/case-packs.json`.

---

[Case portfolio](../../interview-kits/cases/README.md) · [English reading map](reading-map.md) · [Question bank →](question-bank.md)

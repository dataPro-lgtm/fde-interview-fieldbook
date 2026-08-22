# Answer calibration: score evidence, not polish

> **Use this when:** two answers both sound correct, but one survives production follow-up and the other does not.<br>
> **Produce:** first and second recordings, exact-quote scores, disagreement notes, and two repaired behaviors.<br>
> **Boundary:** this training rubric is not an employer's internal standard.

The purpose of calibration is not to make everyone use the same wording. It is to make the distinction between vocabulary, independent delivery, and organizational leverage observable.

## The four levels

- **1 — Dangerous:** the observed judgment would create customer or production harm;
- **2 — Developing:** concepts are present, but decisions depend on prompts or ideal conditions;
- **3 — Independent delivery:** the answer defines the task, makes a bounded choice, verifies it, and owns launch/recovery;
- **4 — Organizational leverage:** beyond the current task, the answer manages cross-system uncertainty and creates a reusable mechanism with ownership and migration.

An unobserved skill is `N/O`, not 1. If a discovery prompt creates no coding opportunity, it cannot prove poor coding.

## What changes between levels

| Signal | Level 2 | Level 3 | Level 4 |
| --- | --- | --- | --- |
| Problem | Restates request | Defines user, baseline, risk, and non-goal | Exposes hidden organizational or system boundary |
| Choice | Lists options | Chooses with evidence and failure boundary | Connects choice to staged decisions and future migration |
| Verification | Says “test and monitor” | Names sample, metric, trace, gate, and owner | Designs feedback that updates process or product |
| Failure | Adds retry or fallback | Distinguishes states, blast radius, recovery | Prevents class recurrence across teams or consumers |
| Productization | Calls code reusable | Separates core and configuration | Proves second consumer, compatibility, ownership, migration |

Longer is not necessarily stronger. A concise answer can score 3 if its decision, evidence, and boundary are explicit.

## Practice before opening anchors

1. Select one prompt and no more than three target dimensions.
2. Give a 30-second conclusion and a three-minute explanation.
3. Record one decision, one trade-off, one evidence point, and one change condition.
4. Let two reviewers score independently using exact quotes.
5. Exchange evidence before scores.
6. Open the relevant anchors and classify the disagreement.
7. Repair only two behaviors and record again.

The repository includes eight [synthetic scenarios](../../data/calibration-scenarios.json). They are designed to expose `N/O`, terminology bias, unjustified level 4, and veto-risk disagreement. They are practice data, not learner outcome evidence.

## A short example

Prompt: “The customer asks for a fully autonomous refund agent. How would you begin?”

**Developing signal:** “I would use RAG for policy and tools for payment, then add guardrails and human review.” This lists plausible components but has not defined user, error cost, or which action is allowed.

**Independent-delivery signal:** “I would first map how a refund is approved, distinguish advice from the irreversible payment action, and quantify duplicate and incorrect-refund cost. The first slice would cite policy and transaction evidence for low-value duplicate-payment cases while an agent approves the action. We expand only after fixed historical replay and shadow use meet error and adoption gates.”

**Leverage signal:** the answer additionally identifies which approval, operation-identity, audit, and policy-version primitives repeat across other financial actions; names a second workflow and owner; and defines migration rather than declaring a platform.

The difference is not jargon. It is the scope of owned uncertainty and the strength of evidence.

## Six common disagreement types

| Code | Mistake | Repair |
| --- | --- | --- |
| `no-observation-as-low` | Missing evidence is scored as inability | Use `N/O`; create another task |
| `term-density` | More AI terms raise the score | Probe state, owner, failure, and stop |
| `role-level` | Reviewers assume different seniority | Fix target level before the run |
| `risk-underweight` | Irreversible harm is treated as a minor gap | Apply veto and consequence boundary first |
| `product-leverage-overreach` | Comprehensive answer is called platform leverage | Require second consumer, owner, and migration |
| `evidence-inference` | Reviewer completes the answer mentally | Keep exact quote; ask one discriminating follow-up |

Do not average 2 and 4 into 3. The reviewers may be evaluating different dimensions or disagreeing about a critical risk.

## Separate score from confidence

Score describes the observed behavior. Confidence describes evidence sufficiency.

- **High:** multiple consistent quotes or artifacts and discriminating follow-up;
- **Medium:** direct evidence exists, but boundary or counterexample is missing;
- **Low:** sample is short, prompt is misaligned, or signal is indirect.

A “3, low confidence” is not automatically a 2. State the missing observation.

## Use the full reviewer protocol

For paired review, use:

- [blind score, adjudication, and re-score protocol](../../interview-kits/rubrics/calibration-protocol.md);
- [cross-role evidence anchor library](../../interview-kits/rubrics/evidence-anchor-library.md);
- [reviewer calibration record](../../interview-kits/worksheets/reviewer-calibration-record.md).

Privacy-safe rating records can be summarized with:

```bash
python3 scripts/summarize_calibration.py ratings.json
```

Report the denominator with any percentage. Reviewer agreement measures the scoring process, not candidate quality or interview outcome.

## Practice

Choose four prompts from the [question bank](question-bank.md), one each from discovery, engineering, production AI, and field leadership. Keep first attempts. For each replay, change only two observable behaviors, such as:

- name the decision owner;
- distinguish fact from hypothesis;
- specify unknown-outcome handling;
- define a stop gate;
- state a second-consumer test for productization.

## Completion check

You are ready to move on when:

- every numeric score cites an exact statement or artifact;
- unobserved skills remain `N/O`;
- reviewers can classify rather than hide major disagreement;
- the second answer changes behavior, not merely fluency;
- no synthetic or practice result is described as production experience;
- external effectiveness remains unclaimed until real independent review exists.

---

[← Portfolio evidence](portfolio-evidence.md) · [English reading map](reading-map.md) · [Field operating playbook →](field-operating-playbook.md)

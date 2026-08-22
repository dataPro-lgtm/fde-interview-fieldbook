# Behavioral interviews and field leadership

> **Use this when:** your project stories sound like timelines, team summaries, or disguised success stories.<br>
> **Produce:** one failure story, one conflict story, and one live-recovery story in two lengths.<br>
> **Suggested practice:** 30 minutes plus reviewer follow-ups.

The behavioral interview asks whether your judgment remains trustworthy when information is incomplete, incentives conflict, and a customer is watching. Project size is weak evidence by itself. The signal comes from decisions, consequences, accountability, and the mechanism you changed afterwards.

## Use STAR-L without sounding templated

| Part | Purpose | Approximate share |
| --- | --- | ---: |
| Situation | Only context that changes the decision | 15% |
| Task | Your responsibility, constraint, and success boundary | 10% |
| Action | Decisions, evidence, trade-offs, communication, implementation | 50% |
| Result | Verified result, miss, and side effect | 15% |
| Learning | Mechanism changed and remaining limit | 10% |

Most weak stories spend too long on setting and compress the decisive action into “we aligned.” Slow down where you chose, disagreed, built, debugged, or accepted a cost.

## Prepare eight evidence-bearing stories

1. **Ambiguity to delivery:** how you found the real problem and bounded the mission;
2. **Production incident:** impact control, evidence, recovery, communication, and prevention;
3. **Stakeholder conflict:** why the other position was rational and how the decision was made;
4. **Refusing an unsafe request:** the boundary protected and the alternative offered;
5. **Speed versus quality:** reversible scope removed and irreversible control preserved;
6. **Low adoption:** how workflow evidence changed the product, not just training;
7. **Your wrong judgment:** the specific error, impact, recovery, and mechanism change;
8. **Productization and handoff:** how the next team or customer became less dependent on you.

Do not force one story to cover all eight. Reusing the same project is acceptable if the decisions are genuinely distinct.

## Keep three lengths factually identical

- **90 seconds:** problem, your responsibility, decisive action, result, one lesson;
- **8 minutes:** current state, evidence, trade-offs, implementation, launch, result, failure, learning;
- **25 minutes:** architecture, data, evaluation, users, incident, cost, organizational boundary, and appendix.

Length changes depth, not facts. Metrics should not become more impressive in the longer version.

## Make personal contribution auditable

Use precise verbs:

- “I owned…” for responsibility;
- “I decided…” for judgment;
- “I implemented/debugged…” for hands-on work;
- “I worked with…” for collaboration;
- “The team delivered…” for the collective result.

If another person built the critical component, say how you scoped, integrated, tested, or influenced it. Endless “we” hides your role; endless “I” hides reality.

## A credible conflict story gives the other side a case

Security owns exposure, sales owns a customer commitment, platform owns long-term operations, and users absorb incorrect output. Explain why their position was reasonable before explaining your decision.

Use this sequence:

1. shared outcome;
2. conflicting responsibilities or risk;
3. missing fact;
4. experiment, option, or decision rule;
5. decision owner;
6. unresolved cost and follow-up.

“I educated the non-technical stakeholder” is often a red flag. Show how their concern improved the result.

## Recover a failing demo without deception

### Before

- define the single workflow the demo must prove;
- freeze version and input scope;
- rehearse in the same environment;
- prepare health checks and an explicit switch owner;
- prepare a transparent recorded, static, or manual fallback.

### During

State the observed symptom without inventing root cause. Make one bounded recovery attempt. At the agreed threshold, switch to the fallback and continue the user narrative.

Example:

> This request did not return within our demo threshold. I am switching to a result recorded from the same frozen version so we can complete the workflow. We will retain this trace and determine whether the first divergence was dependency, data, or release state. This demo is not evidence of production reliability.

### After

Communicate impact, owner, and next update. Preserve the trace and run a TRACE review. A successful fallback does not erase the incident.

## Answer high-pressure requests with options

When asked to launch today, guarantee 100%, or bypass review:

1. acknowledge the business objective and time pressure;
2. describe the concrete consequence, not a wall of jargon;
3. give two or three executable options;
4. recommend one and identify the decision owner and next evidence point.

This is stronger than either automatic agreement or abstract refusal.

## Change information density by audience

| Audience | Lead with | Do not substitute |
| --- | --- | --- |
| Executive | Outcome, risk, options, decision needed | Architecture tour |
| Engineering | Reproduction, evidence, interface, owner, done condition | “High priority” |
| Security/compliance | Data, identity, purpose, flow, retention, control, residual risk | “The model is safe” |
| User | Current action, when to trust, correction, escalation | Model lecture |

Changing detail is not changing truth.

## Red flags

- you are the hero in every story;
- failure always belongs to the customer, sales, or a teammate;
- result means only “on time” or “happy customer”;
- no decision can be attributed to you;
- conflict ends through hierarchy alone;
- learning means “communicate more” without a mechanism;
- an exercise is presented as production experience;
- the story has customers but no hands-on work, or code but no user.

## Story-card template

```text
Title and one-line impact:
Situation and constraints:
My responsibility:
Decision 1 / evidence / alternative rejected:
Decision 2 / evidence / alternative rejected:
Largest surprise:
How I communicated:
Verified result:
What did not work or remains unknown:
Mechanism changed afterwards:
Three likely follow-ups:
```

## Practice

Record one wrong-judgment story and one conflict story in 90-second and eight-minute forms. A reviewer should stop you whenever:

- a claim cannot be assigned to you or the team;
- an outcome has no source or boundary;
- the other party is described as irrational;
- a lesson lacks a changed mechanism;
- the long version contradicts the short version.

Then rehearse the demo-failure scenario with a 30-second decision threshold.

## Completion check

A reviewer unfamiliar with the project can accurately restate the problem, your responsibility, two decisions, the result and its limit, and the mechanism that changed. They should not need your employer's internal vocabulary to understand the story.

---

[← Question bank](question-bank.md) · [English reading map](reading-map.md) · [Study plans →](study-plans.md)

# Field operating playbook: from first meeting to independent operation

> **Use this when:** you need to translate interview reasoning into a production engagement.<br>
> **Produce:** mission, ledgers, thin-slice contract, eval gate, rollout plan, incident path, handoff, and product signal.<br>
> **Boundary:** adapt to the customer's security, legal, operational, and procurement process.

An FDE engagement is not finished when a demo works or code reaches production. It is finished when the workflow creates bounded value, failures can be operated, the customer can continue without the author, and repeatable field learning reaches the product team.

## Before entry: define responsibility

Write a one-page entry contract:

- business sponsor and day-to-day workflow owner;
- technical and security owners;
- decision rights and escalation path;
- target user, workflow, baseline, and time box;
- data and environment access process;
- production, support, and handoff boundary;
- explicit non-goals and unresolved assumptions.

A workshop without ownership produces notes, not a mission.

## First 48 hours: collect evidence

Do not spend the opening proving expertise. Observe the current workflow and obtain representative artifacts:

1. shadow an actual user;
2. identify the system of record and manual workarounds;
3. sample normal, boundary, failure, and high-cost cases;
4. map identity, permissions, data location, retention, and purpose;
5. establish baseline volume, time, error, and adoption;
6. identify one decision owner and one operator.

Open the first workshop with the workflow, not a product tour. End with facts, hypotheses, decisions, owners, and the next evidence date.

## Maintain three ledgers

### Fact ledger

Records verified observation, source, time, scope, and expiry. “The sponsor said” is evidence of a statement, not automatically evidence of user behavior.

### Hypothesis ledger

Records the assumption, why it matters, test, owner, deadline, and decision that follows. A hypothesis without a decision is research debt.

### Decision log

Records context, options, choice, trade-off, owner, rollback, and evidence that will trigger review. Do not overwrite old decisions after the facts change.

## Convert “build a system” into a mission

A mission names:

- one user and trigger;
- current decision/action and baseline;
- target workflow change;
- time box and thin slice;
- success, expansion, and stop evidence;
- prohibited actions and residual risk;
- owner for business, system, and operations.

If participants disagree on the mission, more detailed architecture will only hide the disagreement.

## Select the thin slice by uncertainty reduction

Prioritize the slice that answers the most consequential unknown with the smallest safe end-to-end path. It should include representative data, real identity, one user-visible outcome, key risk control, feedback, and fallback.

Use a one-page contract:

```text
User / trigger / current workflow:
Baseline and target:
In scope / non-goals:
Highest uncertainty:
Representative input and system boundary:
Allowed and prohibited actions:
Offline gate / rollout gate / stop gate:
Fallback and operator:
Decision after this slice:
```

## Build vertical evidence every day

Each daily increment should be demonstrable through the real path, even if narrow. Track four flows:

- **data:** source, identity, version, transformation, retention;
- **control/state:** trigger, transition, retry, approval, termination;
- **evidence:** trace, evaluation, audit, adoption event, reconciliation;
- **ownership:** builder, approver, operator, decision-maker.

Daily technical sync should answer: what changed, what evidence exists, what is blocked, what risk grew, and what decision is needed. A status meeting that cannot change a decision is too expensive.

## Treat evaluation as change control

Use four levels:

| Level | Example | Release question |
| --- | --- | --- |
| Component | parse, retrieve, tool schema, policy check | Is the local mechanism correct? |
| Task | end-to-end outcome on representative cases | Does the system complete the bounded job? |
| System | latency, cost, permissions, recovery | Can it run safely and operably? |
| Workflow | time, adoption, correction, loss | Does real work improve? |

Pin data, prompt, model, tool, policy, and judge versions. A headline average must not hide a veto slice. Every gate needs an owner and a response when it fails.

## Launch by expansion and stop rules

Define:

- offline acceptance and known exclusions;
- shadow, internal, or limited-user stage;
- who can expand and on which evidence;
- automatic and manual stop conditions;
- fallback and data correction path;
- on-call owner, dashboard, runbook, and communication;
- post-launch adoption and error review.

“Deploy Friday” is a date, not a launch plan.

## Incident: protect, preserve, then learn

Use TRACE:

1. **Triage** impact and whether it is expanding;
2. **Reproduce** with fixed input and versions;
3. **Analyze** the first divergent layer;
4. **Control** with isolation, rollback, degradation, or human takeover;
5. **Evaluate** recovery and add regression, monitor, gate, and owner.

Preserve evidence before destructive repair when safe. Communicate observed impact and action; do not announce root cause from the first plausible log line.

## Adoption is part of system behavior

Measure where users accept, edit, bypass, abandon, or escalate. Observe why:

- the answer arrives at the wrong point in the workflow;
- verification takes longer than manual work;
- incentives punish use;
- scope or language excludes actual cases;
- corrections disappear instead of improving the system;
- users correctly distrust an unreliable or unauthorized result.

Training is one intervention, not the default diagnosis. Stop or redesign when the workflow has weak value.

## Handoff means the customer can operate

Before exit, prove that a non-author operator can:

- deploy or configure the supported path;
- identify current versions and owners;
- interpret dashboards and alerts;
- execute fallback, rollback, and recovery;
- change safe configuration without code archaeology;
- escalate with a complete evidence package;
- understand residual risks and unsupported cases.

Run a reverse handoff: the customer operates while the FDE observes. Documentation alone does not prove transfer.

## Productization requires a second consumer

Classify field work as:

- stable reusable core;
- source/customer adapter;
- policy/configuration;
- temporary workaround;
- unsupported exception.

Before upstreaming, identify recurring job, second consumer, stable contract, owner, compatibility, telemetry, migration, and deprecation. Generalizing the code without generalizing the operational responsibility creates a platform nobody owns.

## Practice

Take one [Field Case Lab](../../interview-kits/cases/README.md) and produce the nine minimum field artifacts:

1. entry and ownership brief;
2. current workflow;
3. fact/hypothesis/decision ledgers;
4. mission;
5. thin-slice contract;
6. layered evaluation and release gates;
7. rollout and incident path;
8. adoption and handoff plan;
9. product signal with second-consumer test.

Templates are available in the [field delivery worksheet pack](../../interview-kits/worksheets/field-delivery-pack.md).

## Completion check

The engagement plan is independently usable when a non-author can identify the next decision, run the accepted path, stop or recover it, trace evidence to versions, and distinguish reusable product capability from customer-specific policy. A working demo alone does not meet this bar.

---

[← Answer calibration](answer-calibration.md) · [English reading map](reading-map.md) · [Job targeting →](job-targeting.md)

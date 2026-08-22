# Discovery: turn an ambiguous request into a bounded mission

> **Use this when:** you start proposing architecture before you understand the workflow.<br>
> **Produce:** a current-state workflow, problem statement, thin-slice contract, and acceptance evidence.<br>
> **Suggested practice:** 30 minutes with one case and a reviewer.

Discovery is not a polite prelude to the technical interview. It is the first engineering decision. A customer may ask for an agent while the real constraint is inconsistent policy, missing ownership, stale data, or a process nobody wants to change. The FDE must find which uncertainty changes the solution before spending delivery capacity.

## Reconstruct the current workflow first

Do not begin with the target architecture. Establish:

1. who triggers the work and why;
2. what inputs and systems are used;
3. where a person or system makes a decision;
4. what action follows and whether it is reversible;
5. who consumes the result;
6. where delay, cost, error, or risk occurs;
7. how failure is detected and recovered today.

```text
Trigger -> Input -> Decision -> Action -> Downstream outcome
              |         |          |
         data/access  exceptions  side effects/recovery
```

A request to “automate all support tickets” may become three different missions after this map: normalize the taxonomy, surface current policy with citations, or automate one low-risk action. Those choices require different systems and evidence.

## Ask in information-value order

Interview time is scarce. Ask the question most likely to change the solution class.

| Layer | High-value question | What it changes |
| --- | --- | --- |
| Outcome | What behavior or business result must change? | Whether the project is worth doing |
| Workflow | Who uses the result and how do they work around errors? | Product shape and adoption risk |
| Data | Which source is authoritative, how fast does it change, and who may see it? | Feasibility and system boundary |
| Risk | Which error or action is unacceptable or irreversible? | Autonomy and rollout |
| Scope | What can two weeks prove or disprove? | Thin slice and next decision |

Avoid a checklist interrogation. Explain why a question matters: “I am asking about reversibility because it determines whether the first release can act or should only recommend.”

## Separate facts, requests, and hypotheses

Maintain three columns during the conversation.

| Type | Example | Next action |
| --- | --- | --- |
| Fact | Median response time was 18 minutes last month | Confirm definition and source |
| Request | Reduce manual search time | Establish baseline and target |
| Hypothesis | 80% of tickets can be automated | Segment historical cases and test |

Seniority is not pretending to know. It is making uncertainty visible and attaching a test, owner, and decision date.

## Write a mission that can be accepted

Use this structure:

> For **[user]**, when **[trigger]** occurs, the current **[workflow step]** causes **[baseline impact]** because of **[known or testable cause]**. Within **[time box]**, we will use **[smallest change]** to move **[metric]** toward **[target]**, without crossing **[risk boundary]**.

Example:

> For frontline support agents handling low-value duplicate-payment requests, searching three systems produces an 18-minute median first response and a 7% incorrect escalation rate. In six weeks, we will provide a cited recommendation for English-language cases, target an eight-minute median, keep the agent as the final decision-maker, and prohibit automatic refunds or cross-customer access.

This statement is more useful than “build a refund agent” because it defines the user, baseline, scope, target, and prohibited behavior.

## Use three layers of success evidence

- **Workflow outcome:** elapsed time, human touches, backlog, loss, or resolution;
- **Adoption behavior:** accept, edit, bypass, abandon, escalate, or return to the old process;
- **System control:** retrieval, citation, task success, latency, cost, and policy violation.

System metrics explain why the workflow changed; they do not replace the workflow outcome. Higher retrieval recall is not a success if agents ignore the answer or verification takes longer.

## Decide whether an agent is justified

Ask five questions:

1. Must the system choose its next step from intermediate results?
2. Does it need iterative use of multiple tools or sources?
3. Are rules hard to enumerate while outcomes remain verifiable?
4. Can failure be detected, stopped, and compensated?
5. Is the value of autonomy greater than its governance and variance cost?

If the path is fixed, rules are clear, error cost is high, and verification is weak, a deterministic workflow or a recommendation button is usually better. State what new evidence would justify migration to an agent later.

## Select a thin slice, not a miniature platform

A valid thin slice:

- uses representative input;
- reaches a user-visible outcome end to end;
- includes the highest-risk permission or control;
- collects success and failure evidence;
- has a fallback;
- resolves one important uncertainty.

“Recommendation with cited policy and payment evidence, followed by manual confirmation” is a thin slice. “Build ingestion first and UI later” is a horizontal layer; it postpones evidence about whether the workflow is valuable.

## Handle stakeholder conflict without inventing consensus

- If business wants full autonomy, translate error modes into business consequences and propose stages: recommend, approve, then automate a proven low-risk slice.
- If security restricts data, specify purpose, fields, identity, retention, audit, and residual risk; offer a smaller field set or in-environment computation.
- If engineering fears maintenance, name operational ownership, interfaces, tests, rollback, and knowledge transfer before launch.
- If an executive wants a demo tomorrow, separate demo proof from production proof; freeze inputs, define one narrative, and prepare a transparent fallback.

The goal is not to “win” against another team. It is to expose the trade-off, identify the decision owner, and preserve what remains unresolved.

## Practice

Choose one [Field Case Lab](../../interview-kits/cases/README.md). For the first ten minutes, do not propose a model, database, or agent. Produce:

1. a five-step current workflow;
2. five facts, requests, or hypotheses labeled correctly;
3. one mission statement;
4. one thin slice and three explicit non-goals;
5. three success layers and one stop condition.

Have a reviewer use the [discovery scorecard](../../interview-kits/rubrics/discovery-scorecard.md). A useful follow-up asks which unanswered question could invalidate your slice.

## Completion check

You are ready to move on when a reviewer can identify, from your artifacts alone:

- the user and decision owner;
- the current failure and baseline;
- the most important unresolved hypothesis;
- why this slice is end to end;
- what will cause expansion, repair, or stop;
- why the chosen level of AI autonomy is justified.

---

[English reading map](reading-map.md) · [Coding, data, and delivery →](coding-data-delivery.md)

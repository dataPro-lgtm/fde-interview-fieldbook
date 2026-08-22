# High-signal FDE question bank

> **Use this when:** you know the vocabulary but your answers lose structure after one follow-up.<br>
> **Produce:** a first recording, evidence score, repair rule, and second recording for each session.<br>
> **Method:** answer before reading the reasoning spine.

This is not a set of scripts. Each prompt is a way to expose a decision: what you would inspect, what you would choose, why, how you would verify it, and where the choice stops being valid.

## Answer contract

For every question, use five moves:

1. **Boundary:** define the actual task and what is not yet known;
2. **Mechanism:** explain the system or workflow, not a component list;
3. **Decision:** choose and state the trade-off;
4. **Evidence:** define tests, metrics, trace, and acceptance;
5. **Change condition:** name the fact that would alter the choice.

Record a three-minute answer. Score only observable evidence. Then accept two follow-ups and record a second version.

## Role, discovery, and product judgment

### 1. What makes an FDE different from a software engineer or solutions architect?

Reasoning spine: role labels vary; distinguish ownership. An FDE closes a loop from mission discovery through implementation, production adoption, and field-to-product feedback. Avoid claiming one universal interview process.

Follow-up: What must remain with a durable product or platform team?

### 2. The customer asks for an agent. What do you do first?

Reasoning spine: reconstruct the current workflow, decision, failure cost, and verification path before selecting autonomy. Compare deterministic workflow, recommendation, and agent. State a migration condition.

Follow-up: What if the executive has already announced the agent?

### 3. How do you define a two-week thin slice?

Reasoning spine: choose one user, trigger, real input, user-visible outcome, key control, measurement, and fallback. The slice should eliminate a major uncertainty, not merely complete one horizontal layer.

Follow-up: Which part would you deliberately leave manual?

### 4. The customer demands 99% accuracy. How do you respond?

Reasoning spine: ask 99% of what, on which distribution, with which error cost. Split error types, define a decision threshold and human path, then connect offline evaluation to workflow impact.

Follow-up: Which single dangerous error could veto launch despite 99% aggregate accuracy?

### 5. The product is technically sound but users bypass it. What do you inspect?

Reasoning spine: observe the real workflow; segment accept, edit, bypass, abandon, and escalation. Test trust, timing, incentive, interface, and task fit. Be willing to reduce scope or stop.

Follow-up: What evidence distinguishes a training problem from a product problem?

## Coding, data, and systems

### 6. What does an FDE coding interview observe beyond correctness?

Reasoning spine: contract clarification, examples, invariants, readable implementation, tests, debugging evidence, and production semantics. Confirm the actual employer format.

Follow-up: Show a boundary test that changes the implementation.

### 7. How do you make a sync pipeline idempotent?

Reasoning spine: stable business identity, source version/order, operation key, state transition, stale rejection, replay, and reconciliation. Explain external side effects separately from message deduplication.

Follow-up: What if the remote call timed out after committing?

### 8. Where is the boundary between upsert, soft delete, and physical delete?

Reasoning spine: upsert when the logical identity remains and a newer source version exists; tombstone when source deletion or access revocation must propagate immediately; physical purge after retention, audit, legal, and rebuild needs allow it. Absence from a partial snapshot is not deletion.

Follow-up: How do you detect orphan chunks after a failed delete?

### 9. Postgres or Redis for agent state?

Reasoning spine: start from durability and query semantics. Postgres for authoritative tasks, transitions, ownership, audit, and recovery. Redis for ephemeral coordination, bounded cache, rate limits, leases, or streams where loss semantics are explicit. A cache must not silently become the system of record.

Follow-up: Which state must survive total Redis loss?

### 10. How do you design a multi-tenant external API layer?

Reasoning spine: identity propagation, least privilege, tenant-aware keys and quotas, schema validation, timeout, bounded retry, idempotency, redaction, audit, and isolation tests.

Follow-up: Where could a cache key accidentally cross tenants?

## RAG, evaluation, and model change

### 11. RAG task success drops from 90% to 28%. How do you investigate?

Reasoning spine: validate the measurement first; pin query, corpus, parser, chunker, embedding, index, retriever, reranker, prompt, model, tools, and judge. Replay fixed samples and find the first divergent layer before changing multiple variables.

Follow-up: What would prove the judge, not the system, regressed?

### 12. What makes a useful adversarial RAG sample?

Reasoning spine: target one concrete failure mechanism with an expected safe behavior: indirect injection, stale policy, near-duplicate contradiction, unauthorized content, missing answer, misleading metadata, or ambiguous identity. Include provenance and a failure oracle.

Follow-up: When should the correct result be refusal rather than retrieval?

### 13. Can LLM-as-a-judge be trusted?

Reasoning spine: it can scale bounded, rubric-based comparison, but it is another measured component. Calibrate against humans, randomize position, pin version, test counterexamples, monitor drift, and retain deterministic checks for hard constraints.

Follow-up: Which safety criteria should never depend on a single judge score?

### 14. How do you keep a changing knowledge base fresh?

Reasoning spine: stable ID, versioned source events, permission changes, parse/chunk/embed/index states, tombstones, backlog SLO, replay, and source-target reconciliation. Query-time filters cannot repair stale ingestion alone.

Follow-up: What happens when a newer document fails embedding?

### 15. Fine-tuning, RAG, prompt change, or workflow change?

Reasoning spine: identify whether the gap is knowledge freshness, task behavior, context selection, interface, or orchestration. Choose the least irreversible intervention with a fixed evaluation set and rollback.

Follow-up: What evidence justifies the operational cost of fine-tuning?

## Agents, protocols, reliability, and security

### 16. An agent is asked to do ten things and completes five. What changes?

Reasoning spine: externalize the task graph and durable state; define completion checks, budgets, stop conditions, retries, and recovery. Reduce context competition and verify each step. A longer prompt is not a scheduler.

Follow-up: Which steps should become deterministic code?

### 17. Should a custom agent use skills to enforce a process?

Reasoning spine: skills package instructions and reusable capability; they do not guarantee durable execution. Use code, workflow state, policy checks, and approvals for mandatory ordering and irreversible effects.

Follow-up: What belongs in a skill versus a state machine?

### 18. How do you split sub-agents?

Reasoning spine: split by bounded responsibility, distinct tools/context, independent verification, or parallelism. Define inputs, outputs, authority, budget, termination, and shared state. Do not let every sub-agent contact the user; route through the coordinator unless a deliberate role requires direct interaction.

Follow-up: How do you prevent two agents from acting on the same task?

### 19. What does MCP solve, and what does it not solve?

Reasoning spine: MCP standardizes discovery and invocation of tools, resources, and prompts. It does not grant trust, least privilege, idempotency, business authorization, or safe recovery. Those remain application responsibilities.

Follow-up: What validation sits between an MCP tool result and an irreversible action?

### 20. How can generation continue after the browser closes in a multi-pod system?

Reasoning spine: detach task lifetime from connection and pod. Persist task state and ordered events in durable storage; workers claim with leases/fencing; clients reconnect by task ID and replay after the last sequence before resuming live events.

Follow-up: What prevents an expired worker and a new worker from both committing?

### 21. How do you prevent duplicate charges or emails from tool retries?

Reasoning spine: stable business idempotency key, operation state, remote idempotency when available, unknown-outcome handling, reconciliation, approval for high risk, and immutable audit.

Follow-up: When is compensation unsafe or impossible?

### 22. How do you address indirect prompt injection?

Reasoning spine: treat retrieved or tool content as untrusted data; separate instructions from evidence; enforce authorization in code; constrain tool schemas and destinations; minimize privilege; scan and test adversarial inputs; require approval for consequential actions.

Follow-up: Why is a system prompt warning insufficient?

## Communication and field leadership

### 23. The demo is tomorrow and the system is unstable. What do you do?

Reasoning spine: preserve the one narrative, freeze version and inputs, set a bounded recovery attempt, prepare a transparent recorded/static/manual fallback, and state what the demo cannot prove. Keep the trace for investigation.

Follow-up: Who decides whether to continue live or switch?

### 24. How does one customer customization become product capability?

Reasoning spine: prove a recurring job and second consumer; separate stable core, connector/configuration, and temporary workaround; define ownership, compatibility, migration, telemetry, and deprecation. Do not upstream customer-specific policy blindly.

Follow-up: What evidence says this should remain a one-off?

## Practice

Select four questions from different sections. For each:

1. record a three-minute first answer;
2. underline one decision, one evidence point, and one boundary;
3. take two follow-ups;
4. score exact statements with the [master scorecard](../../interview-kits/rubrics/master-scorecard.md);
5. repair only two behaviors and record again.

Use the [answer calibration guide](answer-calibration.md) if the first answer sounds polished but evidence remains thin.

## Completion check

You are not done because you can recite a definition. You are done when an unfamiliar follow-up still leads back to task, mechanism, decision, evidence, and change condition without inventing experience or employer policy.

---

[← Field Case Lab](field-case-lab.md) · [English reading map](reading-map.md) · [Behavioral and field leadership →](behavioral-field-leadership.md)

# Production AI for FDE interviews in 2026

The production object is not a model call. It is a governed work system that obtains the right context, acts with the right authority, survives failure, and produces evidence about quality and value.

## Six planes

1. **Data** — facts, events, versions, permissions, freshness, deletion.
2. **Context** — instructions, tools, examples, retrieval, history, memory.
3. **Execution** — models, workflows, agents, tools, state, approval.
4. **Control** — policies, versions, release, rollback, budgets.
5. **Evidence** — traces, evals, feedback, audit, business outcomes.
6. **Governance** — identity, least privilege, purpose, security, responsibility.

An answer that covers only the model and vector database is missing most of the production system.

## RAG

Diagnose corpus, access, retrieval, context, generation, and product failures separately. Version logical documents and derived chunks. Propagate access revocation and deletion. Treat permission violations as release blockers, not errors that can be averaged away by good answer quality.

## Agents

Use autonomy only when the path depends on intermediate observations and the result can be verified. Define goals, termination, tools, state, budgets, idempotency, approval, recovery, and audit. Fixed, high-risk workflows often benefit from deterministic orchestration with models used only at bounded judgement points.

## Context engineering

Context includes much more than the system prompt. Keep tools non-overlapping, retrieve just in time, preserve provenance, compress history deliberately, scope memory, and treat retrieved content as untrusted data. More context can reduce performance and increase attack surface.

## Skills, MCP, and A2A

Skills package reusable procedural knowledge through progressive disclosure and deterministic utilities. They guide capability; they do not replace workflow enforcement.

MCP standardizes access to tools and resources, but does not solve trust, least privilege, supply chain, idempotency, or business correctness.

A2A manages interactions and task lifecycles between independent agents. Use it where organizational or system boundaries justify interoperability, not to replace an in-process function call.

## Durable execution

Long-running work must outlive browser connections, pods, and individual model calls. Persist task state, events, checkpoints, approvals, and artifacts behind a task ID. Reconnect by reading state or subscribing from an event cursor. Protect external side effects with idempotency and reconciliation.

## Evals and observability

Build a golden set from normal, boundary, adversarial, multi-step, and historical-failure cases. Measure the first failing layer. Record model, prompt, policy, knowledge, and tool versions, but avoid turning traces into a sensitive-data warehouse.

## Security

Use identity-bound access, least privilege, untrusted-content isolation, structured tool validation, approval, sandboxing, action budgets, supply-chain controls, adversarial evals, and an incident response path. “Add a guardrail” is not a design until the enforced invariant and failure behaviour are explicit.

See the full Chinese chapter: [2026 生产 AI 必修课](../zh-CN/06-production-ai.md).

# The FDE role map

## Working definition

A Forward Deployed Engineer owns measurable outcomes in the customer environment and turns field learning into reusable product capability.

Three responsibilities are inseparable:

1. **Customer reality** — users, workflows, data, permissions, incentives, and constraints.
2. **Engineering depth** — code, data, systems, debugging, and rapid end-to-end delivery.
3. **Production accountability** — adoption, evals, security, reliability, rollback, operations, and handoff.

Without field context, an engineer can solve the wrong problem elegantly. Without engineering depth, the role becomes advisory. Without production accountability, it stops at the demo. Without product feedback, every customer starts from zero.

## Five common archetypes

### Core-platform FDE

Deploys a reusable platform into demanding environments and feeds common requirements back into the core product. Integration, permissions, delivery architecture, and product abstraction are central.

### AI-lab FDE

Turns frontier model capability into production workflows. The hard part is not knowing more model names; it is managing non-determinism through context, evals, tools, permissions, rollout, and measurable adoption.

### Data-infrastructure FDE

Builds customer-specific pipelines and operational systems for data generation, processing, training, or evaluation. SQL, Python, distributed systems, idempotency, replay, and data-quality operations matter heavily.

### Vertical FDE

Works inside healthcare, finance, government, manufacturing, risk, or another high-context domain. Success requires learning the workflow quickly and translating professional responsibility, evidence, and regulation into system behaviour.

### Migration and modernization FDE

Owns platform migrations, performance, frontend or cloud modernization, and sometimes AI adoption. This archetype is a reminder that classic engineering remains core to many FDE roles.

## FDE versus adjacent roles

Titles vary. These are tendencies, not status rankings.

| Role                | Typical centre of gravity                           | FDE difference                                                               |
| ------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------- |
| Software engineer   | Long-lived product/platform code                    | More direct ownership of customer discovery and adoption                     |
| Solutions architect | Feasibility and architecture                        | Usually more hands-on build, debugging, and production follow-through        |
| Solutions engineer  | Technical validation and commercial progress        | Responsibility more often continues past the proof of concept                |
| Consultant          | Analysis, transformation, and implementation advice | Stronger expectation to write code and create product feedback               |
| Applied AI engineer | AI feature quality and delivery                     | Adds embedded customer work, organizational change, and field productization |

## Signals interviewers can observe

Strong signals:

- clarifies the workflow before naming technology;
- separates facts, assumptions, and tests;
- scopes a real end-to-end thin slice;
- explains individual code and decisions;
- defines baselines, gates, rollback, and adoption;
- says no with a practical alternative;
- distinguishes customer configuration from reusable platform capability;
- discusses failure without blame or inflated certainty.

Weak signals:

- defaults every problem to RAG or multi-agent architecture;
- treats a benchmark or demo as the business outcome;
- promises perfect accuracy or no hallucinations;
- places access control in the prompt;
- lists cloud services without data, control, or evidence flow;
- cannot separate personal contribution from team output;
- gives community interview reports the status of official process.

## The field-to-product loop

```text
Discover the real workflow
  -> define a bounded mission
  -> ship a thin, safe path
  -> measure quality and adoption
  -> learn from failure
  -> generalize the repeating pattern
  -> improve the product and next deployment
```

The last step is what creates organizational leverage. A successful bespoke deployment can still be a poor FDE outcome if no knowledge, contract, tool, eval, or platform primitive survives it.

For the current official-source analysis, see the [2026 Q3 role radar (Chinese)](../research/role-radar/2026-Q3.md). Continue with the [interview loop](interview-loop.md) or use the [English reading map](reading-map.md). The sixteen-part English core path has learner-outcome parity with the Chinese core; differences in examples and depth remain explicit in the [parity manifest](../../data/content-parity.json).

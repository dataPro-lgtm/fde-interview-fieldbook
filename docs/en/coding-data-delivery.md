# Coding, data, and delivery under field conditions

> **Use this when:** you can solve isolated problems but struggle with messy data, retries, debugging, or production boundaries.<br>
> **Produce:** one runnable timed implementation, its tests, and a TRACE incident note.<br>
> **Suggested practice:** 45 minutes coding plus 20 minutes review.

FDE coding is not “algorithms versus real work.” A field engineer must reason cleanly about data structures and also survive incomplete reproduction, changing schemas, external APIs, permissions, and side effects. The interview is testing whether your engineering behavior remains predictable under ambiguity.

## Expect three coding surfaces

1. **Algorithms and data structures:** basic abstraction, correctness, and complexity;
2. **Applied building:** an API, parser, aggregation, connector, cache, or extension to existing code;
3. **Debugging and code reading:** failing tests, logs, traces, or a repository with an unknown defect.

Confirm the employer's actual format. Practising only LeetCode or only notebook demos leaves a different blind spot.

## Use a stable live-coding loop

```text
Restate contract -> Work two examples -> Give a correct baseline
-> State invariants -> Implement in small steps -> Test -> Production close
```

### Restate the contract

Clarify input, output, error semantics, scale, mutation, ordering, and duplicates. Do not spend five minutes repeating the prompt; remove only ambiguity that changes the solution.

### Work two examples

Use one normal case and one boundary or counterexample. Walk the state by hand. This often exposes the invariant before code begins.

### Prefer a correct baseline

State the direct approach and complexity before optimizing. A correct, explained implementation is stronger evidence than an unexplained “optimal” answer.

### Make the invariant explicit

Examples include “the window always satisfies the constraint,” “one business key can create at most one external effect,” or “a higher source version can never be overwritten by a lower version.”

### Test while the state is small

Test the happy path, empty input, boundary size, malformed input, duplicates, and failure semantics. Narrate what the test proves rather than saying “I would add tests later.”

### Close like a production engineer

Explain complexity, remaining risks, observability, rollout, and what you would change with more time. Do not bolt on an imaginary microservice architecture.

## Treat data semantics as part of correctness

A field-style data exercise should make you ask:

- What is the stable business identity?
- Can records arrive twice, late, or out of order?
- What does update versus correction mean?
- How are deletions and revoked permissions propagated?
- Can one tenant's data enter another tenant's computation?
- Can the target be rebuilt or replayed?

### Idempotency is an outcome contract

Deduplicating messages is not enough. A retry must not create a second refund, email, ticket, or entitlement. Use a stable business operation key, persist an operation state, distinguish “failed” from “final result unknown,” and make the external action idempotent or compensatable.

### Version before timestamp when order matters

Wall-clock time can be skewed or reused. Prefer source sequence, version, or change token. Reject stale updates explicitly and retain enough metadata to explain which version won.

### Deletion is a first-class event

For a knowledge system, a source deletion or access revocation should make the content unavailable immediately through a tombstone or visibility update. Physical deletion can follow retention, audit, and rebuild requirements. Missing from one partial snapshot is not automatically a delete.

## Design external APIs around failure states

For every connector or tool call, state:

- request and response schema;
- authentication and least privilege;
- timeout and bounded retry;
- rate limit and backpressure;
- idempotency and deduplication;
- partial response and pagination;
- error taxonomy;
- correlation ID and redacted telemetry;
- circuit breaker, fallback, and operator action.

The dangerous state is often not “success” or “failure” but “the caller timed out and the remote side may have committed.” Retrying blindly can duplicate an irreversible action.

## Test the contract, not just lines

| Test layer | Question it answers |
| --- | --- |
| Unit | Does local logic preserve its invariant? |
| Contract | Do producer and consumer agree on schema and error semantics? |
| Integration | Do real boundaries, credentials, and dependencies behave? |
| Replay/regression | Does a known incident remain fixed under pinned versions? |
| Fault injection | Do timeout, duplicate, stale, and partial states recover safely? |
| Security | Can identity, tenant, or policy boundaries be bypassed? |

A high coverage percentage can still miss the one retry path that charges twice.

## Debug with TRACE

| Step | Question | Required evidence |
| --- | --- | --- |
| T — Triage | Who is affected, for how long, and is impact growing? | Scope, timeline, current risk |
| R — Reproduce | Can a fixed input and version reproduce the failure? | Minimal reproduction and slices |
| A — Analyze | Where is the first divergence from known-good behavior? | Layer evidence and rejected hypotheses |
| C — Control | How do we limit impact and restore safely? | Rollback, isolation, fallback, or handoff |
| E — Evaluate | How do we prove recovery and prevent recurrence? | Regression, monitor, release gate, owner |

During an incident, controlling impact may precede proving root cause. Preserve the failing input, version, and trace so recovery does not erase the evidence.

## Answer a production sync question completely

For a knowledge base that changes daily, cover:

1. stable `doc_id` plus source version or content hash;
2. CDC, events, delta API, or bounded snapshot according to source capability;
3. idempotent upsert and stale-version rejection;
4. tombstone and immediate retrieval invisibility before physical purge;
5. independent status/version for parse, chunk, embedding, and index;
6. permission changes as content-critical events;
7. checkpoints, replay, and rebuildable layers;
8. reconciliation counts, hashes, freshness, orphan chunks, and delete latency;
9. quarantine or DLQ so one bad record does not block a batch;
10. an owner and SLO for backlog and propagation.

Naming Kafka or Spark does not answer identity, ordering, deletion, or recovery.

## Make speed-versus-quality decisions by reversibility

Shrink features and autonomy first. Do not remove tenant isolation, audit, rollback, or critical acceptance checks to meet a date. For any temporary shortcut, record an exit condition, owner, and removal date.

## Practice

Run a 40-minute task that ingests records containing duplicate IDs, stale versions, malformed rows, updates, and deletes. Your submission must include:

- runnable code and one command to execute it;
- tests for normal, boundary, malformed, duplicate, and stale cases;
- a short note defining identity, order, deletion, and retry semantics;
- one injected failure and a TRACE record;
- the first production control you would add and why.

Do not count “I would test this in production” as a test.

## Completion check

You are ready to move on when another engineer can run the code, reproduce the failure, understand the invariant, and explain how a retry, stale event, delete, or tenant boundary is handled without asking you to fill in missing semantics.

---

[← Discovery](discovery.md) · [English reading map](reading-map.md) · [System design →](system-design.md)

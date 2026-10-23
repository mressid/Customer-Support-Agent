# Release Goals, Risks and Decision Log

## Release goals

### R1 — Text support MVP
**Outcome:** website visitor receives knowledge-grounded answers, one read-only business lookup is available, and human handoff preserves context.

Exit criteria:
- tenant isolation tests pass;
- inbound messages are deduplicated;
- unknown/unsupported questions have safe fallback;
- tool calls are allowlisted, authorized, and audited;
- human can take over;
- core API/worker telemetry is available;
- evaluation suite has no unresolved critical policy failure.

### R2 — Voice MVP
**Outcome:** customer can speak with the same AI engine and see a coherent transcript.

Exit criteria:
- session start/stop and cleanup are reliable;
- transcript finalization and ordering work;
- interruption behavior is tested;
- audio/transcript privacy policy is implemented;
- latency/cost metrics are visible;
- human handoff behavior is validated for the selected provider.

### R3 — Operational expansion
**Outcome:** support teams can scale operations with workflows, routing, additional channels and stronger evaluation.

## Initial risks

| Risk | Impact | Mitigation |
|---|---|---|
| Prompt injection via customer or retrieved content | Unauthorized or incorrect actions | Tool allowlist, server authorization, untrusted-content boundaries, adversarial tests |
| Tenant data leakage in retrieval | Severe privacy/security issue | Tenant-scoped indexes/filters, access tests, per-tenant metadata and object controls |
| LLM latency/cost | Poor customer experience and high cost | Budgets, timeouts, model routing, caching only safe content, measurement |
| Duplicate webhook or tool execution | Duplicate messages/actions | Durable inbox, idempotency keys, deduplication |
| Voice interruption/transcript race | Confusing conversation history | Sequence IDs, finalized vs partial states, cancellation semantics |
| Provider lock-in | Cost and migration risk | Provider adapters, normalized contracts, contract tests |
| AI gives unsupported answer | Loss of trust | Retrieval evaluation, evidence thresholds, safe fallback and handoff |
| Scope too broad | Delayed first usable product | Text MVP vertical slice, ordered backlog, defer nonessential channels |

## Architecture decision records to create

- ADR-001: Modular monolith boundaries and package ownership
- ADR-002: Relational database and tenant isolation strategy
- ADR-003: Queue and outbox/inbox strategy
- ADR-004: Knowledge ingestion and vector/search technology
- ADR-005: LLM provider abstraction and data policy
- ADR-006: Voice strategy: modular STT/TTS versus speech-to-speech
- ADR-007: Browser voice transport and telephony provider
- ADR-008: Transcript/audio retention and consent
- ADR-009: Authentication and customer verification
- ADR-010: Tool authorization and approval model

## Decisions not to make prematurely

- One microservice per module
- A universal workflow builder before core support works
- Multiple speech providers before the first voice use case is validated
- Autonomous write access to every customer system
- Permanent raw audio retention
- Complex subscription/billing before pricing and usage requirements are known

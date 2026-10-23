# 03 — System Architecture

## Recommended starting point

Use a modular monolith with:
- a single primary application deployment;
- strict module packages and interfaces;
- a relational database for transactional state;
- object storage for documents and permitted media;
- a queue/job runner for ingestion, outbound delivery, and other retryable work;
- a vector/search index for knowledge retrieval;
- provider adapters for LLMs, speech, channels, and business integrations.

Avoid creating a microservice for every module in the first release. Voice streaming may later need an independently scaled real-time component.

## Logical layers

1. **Edge and channel adapters:** website widget, webhook adapters, voice transport, email/messaging adapters.
2. **Application API:** authentication, tenant resolution, validation, rate limiting.
3. **Conversation domain:** sessions, messages, turns, lifecycle, identity references.
4. **AI orchestration:** model routing, policy evaluation, retrieval, tool planning, response generation.
5. **Capability modules:** knowledge, business tools, workflow, tickets, human inbox.
6. **Infrastructure adapters:** SQL, object storage, vector index, queue, LLM provider, speech provider.
7. **Cross-cutting controls:** security, audit, observability, evaluation, usage metering.

## Architecture constraints

- The core domain must not depend on a specific LLM vendor or messaging provider.
- Every request/job must have a trace/correlation ID and tenant context.
- Every tool execution must record actor, tenant, tool version, validated arguments (redacted where needed), outcome, and idempotency key.
- Durable state must be committed before acknowledging a webhook or inbound message when loss would be unacceptable.
- Use a transactional outbox when database changes must reliably publish events.
- External calls require timeouts, bounded retries, backoff, and idempotency where possible.
- Do not hold a database transaction open while waiting for an LLM or external provider.
- Streaming tokens/audio are not equivalent to a committed final message.

## Suggested deployable components at MVP

- `support-api`: HTTP API and modular domain/application modules
- `support-worker`: background jobs and event consumers; may share code with API
- `support-web-widget`: lightweight customer-facing widget
- `support-agent-console`: human support and organization admin UI
- `postgres`: transactional database
- `object-storage`: uploaded source documents and approved attachments
- `queue`: durable asynchronous work
- `vector-search`: managed or self-hosted vector/search capability
- `telemetry`: logs, metrics, traces, alerts

These can initially be combined where appropriate. Keep logical ownership even if API and worker share a codebase.

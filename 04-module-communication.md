# 04 — Module Communication and Contracts

## Communication principles

1. Use direct application interfaces for short, local, request/response operations.
2. Use asynchronous jobs/events for slow, retryable, or externally dependent operations.
3. Use durable event records for inbound webhooks and outbound deliveries.
4. Keep public provider payloads at the adapter boundary; convert them to canonical internal contracts.
5. Never use an LLM prompt as the only interface contract between modules.
6. Carry `tenant_id`, `correlation_id`, `causation_id`, and `occurred_at` on internal events.
7. Version public/event contracts and make consumers tolerant of additive fields.
8. Do not expose internal-only endpoints publicly.

## Synchronous interactions

| Caller | Callee | Purpose | Contract expectations |
|---|---|---|---|
| Channel adapter | Conversation application service | Normalize and append inbound message | Idempotent on provider event ID |
| Conversation orchestrator | AI engine | Process a new turn | Bounded timeout; trace ID |
| AI engine | Knowledge module | Retrieve relevant chunks | Tenant/source filters; citations/IDs |
| AI engine | Tool execution module | Request a named tool | Schema validation and policy check |
| Tool module | Business connector | Execute an allowed operation | Timeout, idempotency, typed result |
| Admin API | Agent configuration | Publish agent version | Immutable version; audit record |
| Human inbox | Conversation module | Claim/take over conversation | Optimistic concurrency or explicit lock |

## Asynchronous events/jobs

Suggested event names:
- `conversation.created`
- `message.received`
- `message.persisted`
- `ai.turn.requested`
- `ai.turn.completed`
- `tool.execution.requested`
- `tool.execution.completed`
- `human.handoff.requested`
- `human.handoff.accepted`
- `ticket.created`
- `knowledge.source.ingestion.requested`
- `knowledge.source.ingestion.completed`
- `channel.delivery.requested`
- `channel.delivery.completed`
- `channel.delivery.failed`
- `voice.session.started`
- `voice.session.ended`
- `evaluation.run.completed`
- `usage.recorded`

Events communicate facts that have happened. Commands request work. Do not use event names that imply success before the work has succeeded.

## Canonical inbound message envelope

```json
{
  "event_id": "provider-or-internal-unique-id",
  "tenant_id": "tenant-id",
  "channel_connection_id": "channel-id",
  "provider": "website-chat",
  "provider_event_id": "provider-event-id",
  "conversation_id": "conversation-id-or-null",
  "customer_identity": {
    "provider_identity_id": "external-identity-id",
    "display_name": "Customer-provided-name-or-null"
  },
  "message": {
    "message_id": "internal-message-id",
    "direction": "inbound",
    "kind": "text",
    "text": "Where is my order?",
    "attachments": []
  },
  "occurred_at": "2026-01-01T12:00:00Z",
  "correlation_id": "trace-or-correlation-id"
}
```

This is illustrative. Production contracts should define schemas, limits, optional fields, and validation rules. Never trust a provider-supplied tenant ID without resolving the configured channel connection.

## Tool invocation envelope

```json
{
  "tool_execution_id": "execution-id",
  "tenant_id": "tenant-id",
  "conversation_id": "conversation-id",
  "agent_version_id": "agent-version-id",
  "tool_name": "orders.lookup",
  "arguments": {
    "order_reference": "ORDER-123"
  },
  "requested_by": "ai-agent",
  "idempotency_key": "stable-operation-key",
  "correlation_id": "correlation-id"
}
```

The tool service must derive authorization from trusted application context. It must not accept model-generated claims of identity or permissions.

## Delivery state machine

Recommended outbound states:
`queued → sending → sent → delivered`
with side paths:
`queued/sending → retry_wait → sending`
and terminal or review states:
`failed`, `cancelled`, `unknown`.

`sent` and `delivered` are distinct when the provider exposes a delivery receipt. An uncertain provider timeout must not automatically mean the message was not sent; retrying may duplicate it.

## Reliability patterns

- **Webhook inbox:** persist provider event IDs and processing state to deduplicate replays.
- **Transactional outbox:** commit domain changes and pending event records in one transaction, then publish.
- **Idempotent commands:** use stable idempotency keys for external write operations.
- **Retry policy:** exponential backoff with jitter, maximum attempts, and dead-letter/review path.
- **Concurrency:** protect conversation ownership and turn sequencing.
- **Ordering:** order by conversation/stream key when the broker supports partitioning.
- **Timeouts:** bound all provider calls.
- **Circuit breaking:** stop repeatedly calling a failing dependency.
- **Compensation:** define recovery for workflows that span systems without distributed transactions.

## Error contract

Return stable machine-readable error codes, safe user-facing messages, retryability, and correlation ID. Do not return stack traces, secret values, provider tokens, or internal prompts.

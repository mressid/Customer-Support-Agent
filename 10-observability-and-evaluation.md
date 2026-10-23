# 10 — Observability, Analytics and AI Evaluation

## Correlation model

Carry:
- `trace_id`
- `correlation_id`
- `causation_id`
- `tenant_id` (safe internal identifier; avoid high-cardinality metric labels)
- `conversation_id`
- `turn_id`
- `tool_execution_id`
- `provider_request_id` where available

Do not place message text, customer email, phone, access tokens, or other sensitive values in metric labels.

## Operational signals

### API and platform
- request rate, error rate, latency;
- queue depth and oldest-job age;
- worker failures and retry count;
- database connection pool, slow queries;
- object-storage errors;
- dependency health.

### Conversation and delivery
- inbound acceptance and processing latency;
- outbound delivery success/failure;
- duplicate event count;
- conversation completion and handoff;
- abandoned session rate.

### AI and RAG
- model latency, errors, token usage/cost;
- retrieval latency, empty retrieval, source distribution;
- tool proposal/authorization/success/failure;
- groundedness and unsupported-claim review;
- clarification and escalation rates.

### Voice
- session establishment time;
- time to first audio;
- turn latency;
- interruption rate;
- transcript finalization failures;
- reconnects and dropped sessions.

## Evaluation plan

Build a curated set of realistic, anonymized or synthetic conversations covering:
- common FAQ;
- ambiguous questions;
- missing information;
- conflicting or stale documents;
- prompt injection attempts;
- requests for restricted customer data;
- tool success and tool failure;
- external provider timeout;
- customer asks for human;
- language switching;
- interruption and voice transcript errors.

Score:
- factual correctness;
- source support/groundedness;
- appropriate clarification;
- correct tool selection and arguments;
- authorization compliance;
- correct handoff decisions;
- response usefulness and tone;
- latency and cost.

Use deterministic assertions for permissions, schemas, and state transitions. Use model-based judges only as one signal, not as the sole release gate.

## Release gates

A new prompt/model/agent version should not be published until:
- critical safety tests pass;
- tool authorization tests pass;
- regression quality is within agreed thresholds;
- latency and cost are measured;
- rollback path is known;
- a versioned release record exists.

# 09 — Security, Privacy and Reliability

## Tenant isolation
- Resolve tenant from authenticated identity or trusted channel configuration.
- Never trust a tenant ID from an arbitrary customer payload.
- Apply tenant filters to SQL, search/vector retrieval, object storage, cache keys, jobs, events, and analytics.
- Add cross-tenant access tests to CI.
- Use least-privilege database and service credentials.

## Authentication and authorization
- Separate organization administrators, support agents, customers, and service identities.
- Enforce permissions on the server for every protected operation.
- Verify customer identity before exposing protected order/account details.
- Require confirmation/approval for sensitive or irreversible actions.
- Re-check authorization at execution time, not only when the AI proposes a tool call.

## Secret management
- Store provider credentials in a secret manager or protected encrypted store.
- Reference secrets by identifier in configuration.
- Redact tokens, passwords, API keys, and authorization headers from logs and traces.
- Support rotation and revocation.

## Prompt injection and untrusted content
- Treat customer messages, uploaded files, retrieved passages, web pages, and tool results as data, not authority.
- Keep tool permissions outside the model prompt.
- Allowlist tool names and validate every argument.
- Prevent retrieved instructions from changing system policy.
- Require human approval for high-risk actions.
- Use output validation and structured schemas where appropriate.

## Privacy and retention
- Classify personal and sensitive data.
- Define retention for messages, transcripts, raw audio, uploaded files, logs, and audit events separately.
- Support access/deletion workflows where applicable.
- Limit access to transcripts and recordings.
- Avoid putting unnecessary personal data into prompts or evaluation datasets.
- Use synthetic or redacted data for tests whenever practical.

## Reliability
- Durable inbox for inbound events.
- Transactional outbox for important events.
- Idempotency keys for retried commands.
- Bounded retries with exponential backoff and jitter.
- Dead-letter/review queue for exhausted retries.
- Provider timeouts and circuit breakers.
- Health checks and dependency readiness.
- Graceful degradation: if RAG is down, do not pretend a grounded answer was produced; ask/hand off instead.
- If AI provider is down, communicate temporary unavailability or route to a human.

## Upload safety
- Limit size and accepted file types.
- Validate actual file content rather than trusting extension.
- Malware-scan files where feasible.
- Keep private objects non-public by default.
- Use short-lived signed URLs when appropriate.
- Apply tenant and retention policies to object storage.

## Security testing checklist
- Cross-tenant read/write tests
- Unauthorized tool invocation
- Prompt injection through user input and retrieved documents
- Webhook signature failures and replay attempts
- Duplicate webhook delivery
- Tool timeout with unknown write outcome
- Secret leakage in logs/traces
- Unauthorized transcript/audio access
- Rate-limit and abuse scenarios

# Product Backlog — Epics, Capabilities and Stories

This is a starter backlog, not a commitment. Refine story scope, split work, estimate with the team, and reorder based on evidence. IDs are stable references for planning.

## Epic E01 — Tenant and access foundation
**Goal:** establish secure organization boundaries.

- **US-001** As an organization administrator, I can create/configure an organization so that resources have an owner.
  - Acceptance: organization ID is generated; default settings exist; audit event is recorded.
- **US-002** As an administrator, I can invite users and assign roles.
  - Acceptance: invitation expires; role is validated server-side; revoked users lose access.
- **US-003** As a developer, I can test tenant isolation.
  - Acceptance: cross-tenant read/write attempts are denied in automated tests.

## Epic E02 — Conversation and message core
**Goal:** persist and retrieve a reliable conversation timeline.

- **US-010** As a customer, I can start a conversation through website chat.
  - Acceptance: conversation is tenant/channel scoped; initial event is persisted.
- **US-011** As a customer, I can send and receive text messages.
  - Acceptance: message order is stable; delivery status is represented; errors are recoverable.
- **US-012** As a support agent, I can inspect the conversation timeline.
  - Acceptance: messages, system events, and visibility levels are distinguished.
- **US-013** As a system, I can deduplicate inbound events.
  - Acceptance: replayed provider event does not create duplicate messages.

## Epic E03 — Website chat channel
**Goal:** provide the first customer-facing channel.

- **US-020** As an administrator, I can configure a website widget.
  - Acceptance: widget is associated with the correct organization and agent configuration.
- **US-021** As a visitor, I can open chat and receive a session.
  - Acceptance: session token is scoped, expires, and cannot access other tenants.
- **US-022** As a visitor, I can reconnect after a temporary network failure.
  - Acceptance: existing conversation can be resumed under a valid session policy.

## Epic E04 — Knowledge ingestion and RAG
**Goal:** ground answers in organization-approved sources.

- **US-030** As an administrator, I can register and upload a knowledge source.
  - Acceptance: file limits and type checks are enforced; ingestion state is visible.
- **US-031** As a system, I can parse, chunk, embed, and index a document asynchronously.
  - Acceptance: failed ingestion can be retried; document version is traceable.
- **US-032** As an AI agent, I can retrieve relevant chunks for a question.
  - Acceptance: results are tenant-filtered and include source metadata.
- **US-033** As a customer, I receive a grounded answer or a clear fallback.
  - Acceptance: answer is not represented as sourced when retrieval returns no useful evidence.

## Epic E05 — AI orchestration
**Goal:** coordinate each conversation turn safely.

- **US-040** As a system, I can process a turn through a versioned agent configuration.
  - Acceptance: model/config version, latency, and outcome are recorded.
- **US-041** As a customer, I can ask a follow-up question using conversation context.
  - Acceptance: relevant recent context is used without exposing another customer's data.
- **US-042** As a system, I can handle model timeout or provider failure.
  - Acceptance: bounded retry/fallback occurs; no false success message is delivered.
- **US-043** As an administrator, I can publish and roll back an agent version.
  - Acceptance: published versions are immutable and audit logged.

## Epic E06 — Safe business tools
**Goal:** let the AI invoke a small allowlisted set of business operations.

- **US-050** As an administrator, I can enable a versioned tool for an agent.
  - Acceptance: tool must be allowlisted and schema-valid.
- **US-051** As a customer, I can ask for an order status lookup.
  - Acceptance: customer verification and tenant scope are checked; result is typed and minimal.
- **US-052** As a system, I can safely handle tool timeout and duplicate requests.
  - Acceptance: idempotency behavior is defined; unknown write outcome is not blindly retried.
- **US-053** As a security reviewer, I can audit tool calls.
  - Acceptance: actor, tool/version, outcome, timestamp and correlation ID are available with sensitive values redacted.

## Epic E07 — Human inbox and handoff
**Goal:** ensure a human can take over with context.

- **US-060** As a support agent, I can view an unassigned queue.
  - Acceptance: queue is tenant scoped and supports assignment.
- **US-061** As a customer, I can request a human.
  - Acceptance: AI stops responding when handoff policy requires; the customer receives a clear status.
- **US-062** As a support agent, I receive a handoff summary.
  - Acceptance: summary includes transcript, unresolved request and prior tool outcomes permitted by policy.
- **US-063** As a support agent, I can resolve the conversation.
  - Acceptance: resolution and ownership changes are recorded.

## Epic E08 — Tickets and case tracking
**Goal:** track support work beyond one interaction.

- **US-070** As a support agent, I can create a ticket from a conversation.
  - Acceptance: ticket links to source conversation and has a status history.
- **US-071** As a support lead, I can filter tickets by status, priority and assignment.
  - Acceptance: filters respect permissions and tenant boundaries.

## Epic E09 — Voice MVP
**Goal:** support real-time browser voice using the same conversation engine.

- **US-080** As a customer, I can start and end a voice session.
  - Acceptance: microphone permission is explicit; session state and failures are visible.
- **US-081** As a customer, I can speak and receive a spoken response.
  - Acceptance: speech provider is configurable; failures have a fallback path.
- **US-082** As a customer, I can interrupt the AI while it speaks.
  - Acceptance: obsolete audio is canceled/truncated where supported and not recorded as fully delivered.
- **US-083** As a customer, I can switch between text and voice in one conversation.
  - Acceptance: finalized transcript and message order remain coherent.
- **US-084** As a support agent, I can take over a voice conversation or receive its context.
  - Acceptance: handoff behavior is explicit for the chosen telephony/media provider.

## Epic E10 — Workflow, routing and SLA
**Goal:** automate repeatable support operations.

- **US-090** As an administrator, I can define a workflow trigger and steps.
  - Acceptance: workflow version, run state, and failures are visible.
- **US-091** As a support lead, I can define routing rules and SLA targets.
  - Acceptance: rule priority and fallback behavior are deterministic.
- **US-092** As a system, I can retry a failed workflow step safely.
  - Acceptance: retry policy is bounded; idempotency is defined per step.

## Epic E11 — Integrations and additional channels
**Goal:** add provider connectors without contaminating core domain logic.

- **US-100** As an administrator, I can configure an integration securely.
  - Acceptance: credentials are secret references; test status and health are visible.
- **US-101** As a system, I can normalize a provider webhook into a canonical event.
  - Acceptance: signature verified; replay deduplicated; event processing observable.
- **US-102** As a customer, I can continue support through a second channel.
  - Acceptance: identity linking follows verification policy; duplicate conversations are avoided where possible.

## Epic E12 — Observability, evaluation and usage
**Goal:** operate and improve the platform using evidence.

- **US-110** As an operator, I can trace one request across modules.
  - Acceptance: correlation IDs connect API, worker, model, retrieval and tool activity.
- **US-111** As a product owner, I can see resolution and handoff metrics.
  - Acceptance: definitions are documented and metrics are tenant-safe.
- **US-112** As a team, we can run AI regression evaluations.
  - Acceptance: dataset and agent/model version are recorded; critical policy tests gate release.
- **US-113** As an administrator, I can inspect usage by agent and channel.
  - Acceptance: provider usage is reconciled and sensitive data is not exposed in metrics.

## Backlog ordering guidance

Suggested early priority:
1. E01 tenant/access foundation
2. E02 conversation core
3. E03 website chat
4. E12 minimal observability/security work in parallel
5. E04 knowledge ingestion/RAG
6. E05 AI orchestration
7. E06 read-only tool
8. E07 human handoff
9. E08 ticket basics
10. E09 voice
11. E10 workflows/routing
12. E11 more connectors/channels
13. E12 advanced evaluation/usage

Reorder based on user research, risk, technical dependencies, and Sprint Review feedback.

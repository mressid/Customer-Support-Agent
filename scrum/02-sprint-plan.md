# Provisional Sprint Plan

Assumption: two-week Sprints. This sequence is a planning hypothesis, not a fixed commitment. Reforecast after the first Sprint using actual capacity and discovered complexity.

## Sprint 0 / Enablement (only if needed)
**Sprint Goal:** make the team able to build, test, and release safely.
- Repository and module/package structure
- CI pipeline, formatting, static analysis, test setup
- Local development environment and database migrations
- Initial threat model and architecture decision records
- Minimal deployment and secret handling
- Definition of Done agreement

Do not use Sprint 0 as a permanent phase that postpones delivering product value.

## Sprint 1 — Secure conversation foundation
**Sprint Goal:** a tenant-scoped conversation and message can be created, persisted, and retrieved.
- US-001 organization foundation
- US-003 tenant-isolation test foundation
- US-010 conversation creation
- US-011 text message persistence
- Initial audit/correlation ID conventions

**Review demo:** create a conversation, append messages, retrieve timeline, prove cross-tenant access is denied.

## Sprint 2 — Website chat vertical slice
**Sprint Goal:** a visitor can exchange text messages with the backend reliably.
- US-020 widget configuration
- US-021 chat session
- US-022 reconnect/resume
- US-013 inbound deduplication
- Basic delivery/error states and tracing

**Review demo:** customer sends a message; it is persisted and returned; duplicate/reconnect tests are shown.

## Sprint 3 — Knowledge ingestion and retrieval
**Sprint Goal:** organization knowledge can be ingested and retrieved with tenant boundaries.
- US-030 source registration/upload
- US-031 asynchronous parse/chunk/index
- US-032 retrieval with source metadata
- Basic ingestion status and failure retry

**Review demo:** upload a document, inspect ingestion status, query it, see source references.

## Sprint 4 — Grounded AI answers
**Sprint Goal:** website chat answers common questions from approved knowledge and handles missing evidence safely.
- US-040 turn orchestration
- US-033 grounded response/fallback
- US-041 follow-up context
- US-042 model failure handling
- Minimal evaluation set and AI usage recording

**Review demo:** grounded FAQ, follow-up question, unknown answer fallback, provider timeout behavior.

## Sprint 5 — Safe business tool and human handoff
**Sprint Goal:** the AI can perform one authorized read-only lookup and transfer unresolved conversations to a human.
- US-050 tool registry and allowlist
- US-051 order lookup (or equivalent safe read-only tool)
- US-053 audit tool calls
- US-060 inbox/queue
- US-061 customer-requested handoff
- US-062 handoff summary

**Review demo:** tool success, tool denial/failure, and human takeover with preserved context.

## Sprint 6 — Tickets and release hardening
**Sprint Goal:** support staff can track unresolved work and the MVP meets agreed release gates.
- US-070 ticket creation
- US-071 ticket filtering
- US-043 agent version publication/rollback
- US-110 end-to-end tracing
- US-112 initial regression evaluation
- Security, load, backup/restore, and runbook work

**Review demo:** conversation becomes a ticket; team shows metrics, audit, test report, and rollback path.

## Sprint 7 — Voice technical spike / MVP slice
**Sprint Goal:** validate the selected voice architecture and complete a minimal browser voice turn.
- Select speech strategy and provider based on latency, language, cost, and privacy requirements
- US-080 start/end session
- US-081 basic speech exchange
- Voice telemetry and fallback
- Security/consent review

**Review demo:** customer speaks, receives response, and transcript is linked to conversation.

## Sprint 8 — Voice synchronization and handoff
**Sprint Goal:** voice and text share a coherent conversation timeline.
- US-082 interruption
- US-083 modality switching
- US-084 voice handoff behavior for chosen provider
- Voice quality regression scenarios
- Cost/latency dashboard

**Review demo:** speak, interrupt, type a follow-up, and transfer context to human support.

## Later Sprints
- Additional channels/connectors
- Workflow builder, routing, SLA, notifications
- Advanced evaluation and release gates
- Usage plans, quotas and billing
- Additional organization administration and reporting

## Planning caveats
- Team size and capacity are unknown; sprint count may change substantially.
- Voice and integration work often depend on vendor capabilities and credentials.
- Pull security, observability, and tests into each Sprint rather than deferring them.
- Each Sprint should end with a usable Increment, not only design documents.

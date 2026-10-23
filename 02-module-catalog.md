# 02 — Full Module Catalog

The module names describe logical ownership. They do not imply one deployable service per module.

## A. Customer interaction and conversation

### M01 — Conversation Management
**Owns:** conversation lifecycle, turns, participants, message ordering, status, links to cases, and event history.  
**Does not own:** provider transport, AI reasoning, or business-system data.  
**Core records:** Conversation, ConversationParticipant, ConversationTurn, Message, ConversationEvent.  
**Key interfaces:** create/resume conversation; append inbound message; claim/release ownership; close/reopen; retrieve timeline.

### M02 — Channel Management
**Owns:** channel connections, provider adapters, webhook intake, outbound delivery, provider identities, retries, and delivery state.  
**Core records:** ChannelConnection, ChannelIdentity, InboundEvent, OutboundDelivery.  
**Key interfaces:** receive provider event; normalize event; enqueue delivery; report delivery status.  
**Initial channel:** website chat. Add email and messaging providers after the core flow is stable.

### M03 — Customer Identity and Profiles
**Owns:** customer profile, contact points, identity linking, preferences, and consent records.  
**Core records:** Customer, CustomerIdentity, CustomerContact, CustomerConsent.  
**Rule:** a phone number or email address is not, by itself, proof that a person is authorized to access a protected account.

## B. AI conversation and voice

### M04 — AI Conversation Engine
**Owns:** turn orchestration, intent/context interpretation, policy-aware response planning, model selection, and decision trace.  
**Core records:** AgentDefinition, AgentVersion, AgentExecution, ModelConfiguration.  
**May request:** retrieval, tool execution, clarification, response generation, or human handoff.  
**Must not:** bypass authorization or execute arbitrary model-generated code.

### M05 — Knowledge Base and Retrieval
**Owns:** source registration, ingestion jobs, parsing, chunking, embeddings, indexing, retrieval, source versions, and source metadata.  
**Core records:** KnowledgeSource, Document, DocumentVersion, DocumentChunk, RetrievalRun.  
**Requirements:** tenant-scoped retrieval, source freshness, deletion propagation, and traceable citations where supported.

### M06 — AI Tools and Business Actions
**Owns:** tool registry, schema validation, permission checks, execution, results, idempotency, approvals, and action audit.  
**Core records:** ToolDefinition, ToolVersion, ToolExecution, ActionApproval.  
**Rule:** model-selected arguments are untrusted. Validate inputs, customer identity, tenant, and authorization before executing.

### M07 — Real-Time Voice Sessions
**Owns:** live audio session lifecycle, streaming transport, turn-taking signals, interruption handling, timeout, and reconnection.  
**Core records:** VoiceSession, VoiceSessionEvent, AudioSegmentReference.  
**Transport:** WebRTC is a strong browser-media candidate; WebSockets may suit text/control or some audio-streaming APIs. Telephony requires a separate provider adapter.

### M08 — Speech Processing
**Owns:** speech provider abstraction, STT, TTS, speech-to-speech sessions, language/voice settings, and speech errors.  
**Core records:** SpeechProvider, SpeechConfiguration, TranscriptionSegment, SpeechGeneration.  
**Design:** support a modular STT → AI → TTS pipeline and optionally a direct speech-to-speech provider behind an interface.

### M09 — Transcript and Multimodal Synchronization
**Owns:** durable transcript alignment, partial/final transcription state, text/voice message correlation, event ordering, and modality switching.  
**Core records:** TranscriptSegment, ModalityEvent, MessageMediaReference.  
**Rule:** ephemeral partials/audio chunks should not automatically become durable customer-visible messages.

## C. Support operations and automation

### M10 — Human Support Inbox and Handoff
**Owns:** agent queues, assignment, human takeover, AI pause/resume, handoff context, internal notes, and handoff outcome.  
**Core records:** SupportAgent, SupportQueue, Assignment, HandoffEvent.  
**Handoff bundle:** transcript, summary, customer context permitted for the agent, previous tool actions, unresolved questions, and reason for escalation.

### M11 — Ticket and Case Management
**Owns:** durable support work item, status, priority, category, assignment, comments, due dates, and resolution.  
**Core records:** Ticket, TicketComment, TicketStatusHistory.  
**Rule:** a conversation is an interaction; a ticket is work to resolve. One ticket may link to multiple conversations.

### M12 — Workflow Automation
**Owns:** event-triggered business workflows, steps, conditions, schedules, retries, approvals, and execution history.  
**Core records:** WorkflowDefinition, WorkflowVersion, WorkflowRun, WorkflowStepRun.  
**Rule:** use deterministic workflows for business-critical procedures; AI can classify or propose, while the workflow enforces the procedure.

### M13 — Routing, Policies and SLAs
**Owns:** routing rules, queue selection, business hours, response/resolution targets, escalation policy, and fallback behavior.  
**Core records:** RoutingRule, SlaPolicy, BusinessSchedule, EscalationPolicy.

### M14 — Notifications and Follow-Ups
**Owns:** operational/customer notification templates, preferences, dispatch, delivery state, and retry.  
**Core records:** Notification, NotificationTemplate, NotificationDelivery.  
**Boundary:** notification delivery is separate from an ordinary conversational response.

## D. Business integrations and insights

### M15 — Integration Hub
**Owns:** connector definitions, credentials references, API/webhook mapping, health checks, rate limits, retries, and external event normalization.  
**Core records:** Integration, IntegrationCredentialReference, ConnectorDefinition, IntegrationEvent.  
**Rule:** credentials are stored in a secret manager or protected encrypted store, never in plain logs or model prompts.

### M16 — Analytics and Reporting
**Owns:** operational/product metrics, conversation outcomes, channel usage, SLA reporting, voice latency, and cost summaries.  
**Core records:** MetricEvent, ConversationOutcome, Feedback, UsageAggregate.

### M17 — AI Quality, Evaluation and Improvement
**Owns:** evaluation datasets, test runs, quality scores, regression comparison, human review, and release gates.  
**Core records:** EvaluationDataset, EvaluationRun, EvaluationResult, AgentRelease.  
**Evaluates:** correctness, grounding, retrieval, tool choice, policy adherence, refusal/escalation, latency, and voice quality.

## E. Platform administration and governance

### M18 — Organizations, Users and Access Control
**Owns:** tenant, memberships, roles, permissions, service identities, invitations, and tenant context.  
**Core records:** Organization, User, Membership, Role, Permission.  
**Rule:** enforce tenant boundaries in application authorization and data access, not only in the UI.

### M19 — Agent Configuration and Administration
**Owns:** agent instructions, persona, model/speech configuration references, knowledge assignments, tool allowlist, channel mapping, versions, publication, and rollback.  
**Core records:** AgentConfiguration, AgentVersion, AgentDeployment, AgentPolicy.

### M20 — Security, Audit, Observability and Usage
**Owns:** audit records, retention policy, abuse controls, application telemetry conventions, provider usage, quotas, and usage metering.  
**Core records:** AuditEvent, UsageRecord, ProviderUsage, RetentionPolicy, SecurityEvent.  
**Note:** billing/subscription management can be a separate module if commercial plans are introduced.

## Shared technical capabilities

These are not necessarily standalone business modules:
- API gateway / edge rate limiting
- Background job runner and durable queue
- Transactional outbox/inbox
- Object storage for approved attachments and documents
- Search/vector index
- Secret manager
- Configuration and feature flags
- Structured logs, metrics, and distributed tracing
- Database migrations and tenant-aware repository patterns

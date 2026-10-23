# 01 — Product Vision and Scope

## Vision

Build an AI-native customer support platform that can conduct complete, context-aware customer conversations over text and voice, answer using trusted business knowledge, perform explicitly authorized actions, and transfer to human agents when appropriate.

## Primary users

- **Customer:** asks questions or requests an action using a supported channel.
- **Support agent:** reviews, takes over, and resolves conversations or tickets.
- **Support lead:** manages queues, policies, reporting, and quality.
- **Organization administrator:** configures channels, knowledge, AI agents, integrations, and access.
- **Platform operator:** monitors reliability, cost, abuse, and platform health.

## Product outcomes

- Reduce time to a correct answer.
- Resolve repetitive requests without removing access to human support.
- Preserve context across text/voice and channel changes where identity can be safely linked.
- Make AI actions auditable and permission-controlled.
- Let organizations configure knowledge, tools, policies, and escalation behavior.
- Measure resolution quality, not only response speed.

## Product principles

1. **Conversation-first:** a conversation is the durable interaction record; channel sessions are delivery mechanisms.
2. **Modality-independent intelligence:** text and voice share the same orchestration and authorization model.
3. **Grounded answers:** use approved knowledge and business data; be transparent about uncertainty.
4. **Safe action execution:** models propose tool calls; application services authorize and execute them.
5. **Human escape hatch:** customers can request human support and policy can escalate automatically.
6. **Tenant isolation by default:** organization boundaries apply to data, search, tools, events, and analytics.
7. **Observable and testable:** every important AI decision, tool execution, handoff, and failure is measurable.
8. **Provider portability:** model, speech, channel, and integration providers are accessed through adapters.

## MVP scope

### Included
- Organization and user access foundation
- Website text chat
- Conversation lifecycle and message persistence
- Basic customer identity
- Knowledge source ingestion and retrieval
- AI response orchestration
- One read-only business tool
- Human handoff/inbox
- Basic ticket creation
- Audit, logs, metrics, traces, and usage tracking

### Later phases
- Real-time browser voice
- STT/TTS and speech-to-speech provider options
- Email and external messaging channels
- Workflow builder and advanced routing/SLA
- More connectors and write-capable tools
- Advanced analytics, evaluation, billing, and enterprise governance

## Explicit non-goals for the first milestone

- Replacing all existing CRM/helpdesk systems
- Arbitrary autonomous changes to customer accounts
- Unreviewed financial transactions
- Supporting every channel/provider at launch
- Training a foundation model
- Splitting every module into a microservice

## Success measures

- Correct answer rate on a curated evaluation set
- Groundedness/source support rate
- Successful task completion rate
- Human escalation rate, segmented by reason
- Median and p95 response latency
- Tool success/failure rate
- Customer satisfaction
- Cost per resolved conversation
- Availability and message-delivery success

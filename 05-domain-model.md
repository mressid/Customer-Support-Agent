# 05 — Domain Model

## Core aggregate boundaries

- **Organization:** tenant boundary and configuration owner.
- **Conversation:** durable interaction and message timeline.
- **Customer:** profile and verified identity links.
- **Agent configuration/version:** published AI behavior and allowed capabilities.
- **Knowledge source/document version:** ingestion and retrieval lifecycle.
- **Tool execution:** authorization, idempotency, result, and audit.
- **Ticket:** support work item that can span conversations.
- **Voice session:** live media lifecycle linked to a conversation.
- **Workflow run:** deterministic multi-step execution.
- **Audit/usage event:** immutable record for governance and measurement.

## Relationship overview

```mermaid
erDiagram
    ORGANIZATION ||--o{ USER_MEMBERSHIP : has
    ORGANIZATION ||--o{ CUSTOMER : owns
    ORGANIZATION ||--o{ CHANNEL_CONNECTION : configures
    ORGANIZATION ||--o{ AGENT_CONFIGURATION : configures
    ORGANIZATION ||--o{ KNOWLEDGE_SOURCE : owns
    ORGANIZATION ||--o{ INTEGRATION : configures
    CUSTOMER ||--o{ CUSTOMER_IDENTITY : has
    CUSTOMER ||--o{ CONVERSATION : participates_in
    CHANNEL_CONNECTION ||--o{ CONVERSATION : receives
    CONVERSATION ||--o{ MESSAGE : contains
    CONVERSATION ||--o{ CONVERSATION_TURN : contains
    CONVERSATION ||--o{ VOICE_SESSION : may_have
    CONVERSATION ||--o{ TOOL_EXECUTION : invokes
    CONVERSATION }o--o{ TICKET : relates_to
    AGENT_CONFIGURATION ||--o{ AGENT_VERSION : versions
    AGENT_VERSION ||--o{ AGENT_EXECUTION : runs
    KNOWLEDGE_SOURCE ||--o{ DOCUMENT : contains
    DOCUMENT ||--o{ DOCUMENT_VERSION : versions
    DOCUMENT_VERSION ||--o{ DOCUMENT_CHUNK : splits_into
    TOOL_DEFINITION ||--o{ TOOL_EXECUTION : executes
    WORKFLOW_DEFINITION ||--o{ WORKFLOW_RUN : runs
```

## Data modeling rules

- All tenant-owned rows must include or be reachable through a trusted `organization_id`.
- Use internal UUIDs/ULIDs; keep provider IDs in separate fields with uniqueness scoped to provider/connection.
- Avoid using phone number/email as the primary key for a customer.
- Store timestamps in UTC; render local time at the edge.
- Keep external provider payloads only when needed for debugging/compliance and with explicit retention/redaction.
- Prefer immutable version rows for agent configuration, knowledge documents, workflows, and tool schemas.
- Keep messages, transcripts, audio references, and attachments distinct so retention/access policies can differ.
- Store object references rather than large binary payloads in the primary relational database.
- Record deletion and re-indexing propagation for knowledge sources.
- Do not store hidden chain-of-thought. Store concise decision metadata, tool calls, sources, and outcomes needed for debugging and audit.

## Suggested message kinds

- `text`
- `image_reference`
- `file_reference`
- `audio_reference`
- `system_event`
- `internal_note` (not customer-visible)
- `transcript_segment` (if transcript is modeled in the message timeline)

Use explicit visibility and direction fields rather than relying on message text conventions.

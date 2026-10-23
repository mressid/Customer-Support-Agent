# 05 — Data Model Diagrams (split by aggregate)

Source: `05-domain-model.md`, `02-module-catalog.md`. The single ER diagram in doc 05 is expanded into one diagram per aggregate group, with attributes. Attribute lists are illustrative.

## 5.0 Aggregate map

```mermaid
flowchart TB
    ORG["Organization (tenant boundary)"]
    ORG --> ACC["5.1 Access"]
    ORG --> CUS["5.2 Customer and channel"]
    ORG --> CON["5.3 Conversation"]
    ORG --> AG["5.4 Agent configuration"]
    ORG --> KB["5.5 Knowledge"]
    ORG --> TL["5.6 Tools and integrations"]
    ORG --> OPS["5.7 Handoff and tickets"]
    ORG --> VC["5.8 Voice"]
    ORG --> WF["5.9 Workflow, routing, SLA"]
    ORG --> GOV["5.10 Audit, usage, evaluation"]
```

## 5.1 Organizations, users and access

```mermaid
erDiagram
    ORGANIZATION ||--o{ MEMBERSHIP : has
    USER ||--o{ MEMBERSHIP : joins
    ROLE ||--o{ MEMBERSHIP : assigned
    ROLE ||--o{ ROLE_PERMISSION : grants
    PERMISSION ||--o{ ROLE_PERMISSION : in
    ORGANIZATION ||--o{ INVITATION : issues
    ORGANIZATION ||--o{ SERVICE_IDENTITY : owns

    ORGANIZATION {
        uuid id PK
        string name
        json settings
        timestamp created_at
    }
    MEMBERSHIP {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        uuid role_id FK
        string status
    }
    INVITATION {
        uuid id PK
        uuid organization_id FK
        string email
        uuid role_id FK
        timestamp expires_at
        string status
    }
```

## 5.2 Customer and channel

```mermaid
erDiagram
    ORGANIZATION ||--o{ CUSTOMER : owns
    ORGANIZATION ||--o{ CHANNEL_CONNECTION : configures
    CUSTOMER ||--o{ CUSTOMER_IDENTITY : has
    CUSTOMER ||--o{ CUSTOMER_CONTACT : has
    CUSTOMER ||--o{ CUSTOMER_CONSENT : records
    CHANNEL_CONNECTION ||--o{ CHANNEL_IDENTITY : maps
    CHANNEL_IDENTITY }o--|| CUSTOMER_IDENTITY : links
    CHANNEL_CONNECTION ||--o{ INBOUND_EVENT : receives
    CHANNEL_CONNECTION ||--o{ OUTBOUND_DELIVERY : sends

    CUSTOMER_IDENTITY {
        uuid id PK
        uuid customer_id FK
        string provider
        string provider_identity_id
        string verification_level
    }
    INBOUND_EVENT {
        uuid id PK
        uuid channel_connection_id FK
        string provider_event_id UK
        string processing_state
        timestamp received_at
    }
    OUTBOUND_DELIVERY {
        uuid id PK
        uuid message_id FK
        string state
        int attempts
        string provider_message_id
    }
```

## 5.3 Conversation

```mermaid
erDiagram
    CONVERSATION ||--o{ CONVERSATION_PARTICIPANT : has
    CONVERSATION ||--o{ CONVERSATION_TURN : contains
    CONVERSATION ||--o{ MESSAGE : contains
    CONVERSATION ||--o{ CONVERSATION_EVENT : logs
    CONVERSATION_TURN ||--o{ MESSAGE : produces
    MESSAGE ||--o{ MESSAGE_MEDIA_REFERENCE : attaches
    CONVERSATION_TURN ||--o| AGENT_EXECUTION : handled_by

    CONVERSATION {
        uuid id PK
        uuid organization_id FK
        uuid customer_id FK
        uuid channel_connection_id FK
        string status
        string owner_type
        int version
    }
    MESSAGE {
        uuid id PK
        uuid conversation_id FK
        string kind
        string direction
        string visibility
        bigint sequence
        text body
        timestamp created_at
    }
    CONVERSATION_TURN {
        uuid id PK
        uuid conversation_id FK
        int turn_number
        string status
    }
```

## 5.4 Agent configuration and execution

```mermaid
erDiagram
    ORGANIZATION ||--o{ AGENT_CONFIGURATION : configures
    AGENT_CONFIGURATION ||--o{ AGENT_VERSION : versions
    AGENT_VERSION ||--o{ AGENT_DEPLOYMENT : deployed_as
    AGENT_VERSION ||--o{ AGENT_POLICY : enforces
    AGENT_VERSION }o--o{ KNOWLEDGE_SOURCE : uses
    AGENT_VERSION }o--o{ TOOL_VERSION : allows
    AGENT_VERSION }o--|| MODEL_CONFIGURATION : uses
    AGENT_DEPLOYMENT }o--|| CHANNEL_CONNECTION : serves
    AGENT_VERSION ||--o{ AGENT_EXECUTION : runs

    AGENT_VERSION {
        uuid id PK
        uuid agent_configuration_id FK
        int version_number
        text instructions
        string status
        boolean immutable
    }
    AGENT_EXECUTION {
        uuid id PK
        uuid conversation_turn_id FK
        uuid agent_version_id FK
        string outcome
        int latency_ms
        json decision_metadata
    }
```

## 5.5 Knowledge

```mermaid
erDiagram
    KNOWLEDGE_SOURCE ||--o{ DOCUMENT : contains
    KNOWLEDGE_SOURCE ||--o{ INGESTION_JOB : runs
    DOCUMENT ||--o{ DOCUMENT_VERSION : versions
    DOCUMENT_VERSION ||--o{ DOCUMENT_CHUNK : splits_into
    DOCUMENT_CHUNK ||--o| EMBEDDING : indexed_as
    AGENT_EXECUTION ||--o{ RETRIEVAL_RUN : performs
    RETRIEVAL_RUN ||--o{ RETRIEVAL_RESULT : returns
    RETRIEVAL_RESULT }o--|| DOCUMENT_CHUNK : cites

    DOCUMENT_VERSION {
        uuid id PK
        uuid document_id FK
        string content_hash
        string state
        object_ref storage_key
    }
    RETRIEVAL_RUN {
        uuid id PK
        uuid agent_execution_id FK
        string query_summary
        int result_count
        int latency_ms
    }
```

## 5.6 Tools and integrations

```mermaid
erDiagram
    TOOL_DEFINITION ||--o{ TOOL_VERSION : versions
    TOOL_VERSION ||--o{ TOOL_EXECUTION : executes
    CONVERSATION ||--o{ TOOL_EXECUTION : invokes
    TOOL_EXECUTION ||--o| ACTION_APPROVAL : may_need
    TOOL_VERSION }o--|| CONNECTOR_DEFINITION : backed_by
    ORGANIZATION ||--o{ INTEGRATION : configures
    INTEGRATION }o--|| CONNECTOR_DEFINITION : instance_of
    INTEGRATION ||--|| INTEGRATION_CREDENTIAL_REFERENCE : uses
    INTEGRATION ||--o{ INTEGRATION_EVENT : emits

    TOOL_VERSION {
        uuid id PK
        string name
        int version
        json input_schema
        json output_schema
        string risk_level
    }
    TOOL_EXECUTION {
        uuid id PK
        uuid tool_version_id FK
        string idempotency_key UK
        string status
        json redacted_arguments
        timestamp started_at
    }
```

## 5.7 Handoff and tickets

```mermaid
erDiagram
    CONVERSATION ||--o{ HANDOFF_EVENT : escalates
    HANDOFF_EVENT ||--o| ASSIGNMENT : results_in
    SUPPORT_QUEUE ||--o{ ASSIGNMENT : holds
    SUPPORT_AGENT ||--o{ ASSIGNMENT : takes
    CONVERSATION }o--o{ TICKET : relates_to
    TICKET ||--o{ TICKET_COMMENT : has
    TICKET ||--o{ TICKET_STATUS_HISTORY : tracks
    SUPPORT_AGENT ||--o{ TICKET : assigned

    HANDOFF_EVENT {
        uuid id PK
        uuid conversation_id FK
        string reason_code
        json bundle_ref
        string outcome
    }
    TICKET {
        uuid id PK
        string status
        string priority
        string category
        timestamp due_at
    }
```

## 5.8 Voice

```mermaid
erDiagram
    CONVERSATION ||--o{ VOICE_SESSION : may_have
    VOICE_SESSION ||--o{ VOICE_SESSION_EVENT : logs
    VOICE_SESSION ||--o{ TRANSCRIPT_SEGMENT : produces
    VOICE_SESSION ||--o{ AUDIO_SEGMENT_REFERENCE : may_store
    TRANSCRIPT_SEGMENT }o--o| MESSAGE : finalized_into
    VOICE_SESSION }o--|| SPEECH_CONFIGURATION : uses

    TRANSCRIPT_SEGMENT {
        uuid id PK
        uuid voice_session_id FK
        bigint sequence
        string state
        float confidence
    }
```

## 5.9 Workflow, routing and SLA

```mermaid
erDiagram
    WORKFLOW_DEFINITION ||--o{ WORKFLOW_VERSION : versions
    WORKFLOW_VERSION ||--o{ WORKFLOW_RUN : runs
    WORKFLOW_RUN ||--o{ WORKFLOW_STEP_RUN : executes
    ORGANIZATION ||--o{ ROUTING_RULE : defines
    ROUTING_RULE }o--|| SUPPORT_QUEUE : targets
    ORGANIZATION ||--o{ SLA_POLICY : defines
    SLA_POLICY }o--|| BUSINESS_SCHEDULE : uses
    SLA_POLICY ||--o{ ESCALATION_POLICY : triggers
```

## 5.10 Audit, usage and evaluation

```mermaid
erDiagram
    ORGANIZATION ||--o{ AUDIT_EVENT : records
    ORGANIZATION ||--o{ USAGE_RECORD : meters
    USAGE_RECORD ||--o{ PROVIDER_USAGE : reconciles
    ORGANIZATION ||--o{ RETENTION_POLICY : sets
    EVALUATION_DATASET ||--o{ EVALUATION_RUN : used_by
    EVALUATION_RUN ||--o{ EVALUATION_RESULT : yields
    EVALUATION_RUN }o--|| AGENT_VERSION : tests
    AGENT_VERSION ||--o| AGENT_RELEASE : released_as
    CONVERSATION ||--o| CONVERSATION_OUTCOME : ends_with
    CONVERSATION ||--o{ FEEDBACK : receives
```

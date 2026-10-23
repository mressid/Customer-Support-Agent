# 02 — Cross-Cutting Flow Diagrams

Source: `04-module-communication.md`, `08-integrations-and-tools.md`, `09-security-privacy-reliability.md`.

## 2.1 Inbound webhook handling

```mermaid
flowchart TD
    A["Provider webhook arrives"] --> B{"Signature and timestamp valid?"}
    B -- No --> R1["Reject 401 and log SecurityEvent"]
    B -- Yes --> C["Resolve channel connection from trusted endpoint config"]
    C --> D{"Body size and schema within limits?"}
    D -- No --> R2["Reject 413 or 422"]
    D -- Yes --> E["Persist InboundEvent with provider_event_id"]
    E --> F{"Duplicate provider_event_id?"}
    F -- Yes --> G["Return 200 and skip processing"]
    F -- No --> H["Commit durable acceptance"]
    H --> I["Return 200 to provider"]
    I --> J["Async job: normalize to canonical envelope"]
    J --> K["Conversation service appends message"]
    K --> L["Record processing state"]
    J -. failure .-> M["Retry with backoff then dead-letter"]
```

## 2.2 Transactional outbox and inbox

```mermaid
sequenceDiagram
    participant S as Domain service
    participant DB as Postgres
    participant O as Outbox relay worker
    participant Q as Queue
    participant C as Consumer
    participant I as Consumer inbox table

    S->>DB: BEGIN
    S->>DB: write domain change
    S->>DB: insert outbox event
    S->>DB: COMMIT
    loop poll or notify
        O->>DB: read unpublished events
        O->>Q: publish event
        O->>DB: mark published
    end
    Q->>C: deliver event
    C->>I: insert event_id if absent
    alt already processed
        C-->>Q: ack and skip
    else first time
        C->>C: handle event
        C->>I: mark processed
        C-->>Q: ack
    end
```

## 2.3 Outbound delivery state machine

```mermaid
stateDiagram-v2
    [*] --> queued
    queued --> sending
    sending --> sent: provider accepted
    sent --> delivered: delivery receipt
    sending --> retry_wait: retryable error
    retry_wait --> sending: backoff elapsed
    sending --> failed: non-retryable or attempts exhausted
    sending --> unknown: timeout with uncertain outcome
    unknown --> sent: status lookup confirms
    unknown --> failed: status lookup denies
    unknown --> review: cannot determine
    queued --> cancelled: obsolete or human takeover
    delivered --> [*]
    failed --> [*]
    cancelled --> [*]
    review --> [*]
```

## 2.4 Retry decision

```mermaid
flowchart TD
    E["Call failed"] --> T{"Error category"}
    T -- "RATE_LIMITED, PROVIDER_UNAVAILABLE" --> R["Retryable"]
    T -- "TIMEOUT" --> W{"Operation is a write?"}
    W -- No --> R
    W -- Yes --> U["UNKNOWN_OUTCOME: status lookup or human review"]
    T -- "AUTHENTICATION_FAILED, AUTHORIZATION_DENIED, VALIDATION_FAILED, NOT_FOUND, CONFLICT" --> N["Not retryable"]
    R --> B{"Attempts left and circuit closed?"}
    B -- Yes --> J["Exponential backoff with jitter"] --> A["Retry with same idempotency key"]
    B -- No --> D["Dead-letter or review queue"]
    N --> F["Return typed error to caller"]
    U --> D
```

## 2.5 Tool execution — full pipeline (split in two parts)

### Part A: validation and authorization

```mermaid
flowchart TD
    A["AI proposes tool call"] --> B{"Tool in agent version allowlist?"}
    B -- No --> X1["Deny: TOOL_NOT_ALLOWED"]
    B -- Yes --> C{"Arguments valid against JSON schema?"}
    C -- No --> X2["Deny: VALIDATION_FAILED"]
    C -- Yes --> D["Derive tenant, customer, conversation from trusted context"]
    D --> E{"Customer verified for this data?"}
    E -- No --> X3["Deny or ask for verification"]
    E -- Yes --> F{"Caller has required permission?"}
    F -- No --> X4["Deny: AUTHORIZATION_DENIED"]
    F -- Yes --> G{"Risk level"}
    G -- read_only --> OK["Proceed to Part B"]
    G -- "reversible write" --> H["Require customer confirmation"] --> OK
    G -- "sensitive write" --> I["Require human approval: ActionApproval"] --> OK
    X1 & X2 & X3 & X4 --> AUD["Write audit record and return typed denial"]
```

### Part B: execution and result handling

```mermaid
sequenceDiagram
    participant AI as AI Engine
    participant TS as Tool Execution Service
    participant DB as Postgres
    participant CN as Connector adapter
    participant EXT as Business API

    AI->>TS: ToolInvocation with idempotency_key
    TS->>DB: insert ToolExecution status=running
    Note over TS,DB: no DB transaction held during the external call
    TS->>CN: execute with timeout
    CN->>EXT: provider specific request
    alt success
        EXT-->>CN: response
        CN-->>TS: normalized typed result
        TS->>TS: validate output schema and redact
        TS->>DB: status=succeeded, audit event
        TS-->>AI: minimal typed result
    else timeout on read
        CN-->>TS: TIMEOUT
        TS->>DB: status=failed retryable
        TS-->>AI: error category
    else timeout on write
        CN-->>TS: UNKNOWN_OUTCOME
        TS->>DB: status=unknown, flag for review
        TS-->>AI: do not claim success
    end
```

## 2.6 Tool execution state machine

```mermaid
stateDiagram-v2
    [*] --> requested
    requested --> denied: allowlist, schema or authz fails
    requested --> awaiting_approval: sensitive action
    awaiting_approval --> approved
    awaiting_approval --> rejected
    awaiting_approval --> expired
    requested --> running: authorized
    approved --> running
    running --> succeeded
    running --> failed: definitive failure
    running --> retry_wait: retryable
    retry_wait --> running
    running --> unknown_outcome: write timeout
    unknown_outcome --> succeeded: status lookup
    unknown_outcome --> failed: status lookup
    unknown_outcome --> needs_review
    denied --> [*]
    rejected --> [*]
    expired --> [*]
    succeeded --> [*]
    failed --> [*]
    needs_review --> [*]
```

## 2.7 Tenant resolution and isolation

```mermaid
flowchart LR
    subgraph Sources["Trusted sources only"]
        S1["Authenticated user token"]
        S2["Channel connection config"]
        S3["Widget session token"]
        S4["Service identity"]
    end
    subgraph Rejected["Never trusted"]
        P["tenant_id in customer payload"]
    end
    S1 & S2 & S3 & S4 --> R["Tenant context resolver"]
    P -. ignored .-> R
    R --> CTX["Request context: tenant_id, correlation_id, actor"]
    CTX --> SQL["SQL filters / RLS"]
    CTX --> VEC["Vector search filter"]
    CTX --> OBJ["Object storage prefix"]
    CTX --> CACHE["Cache key prefix"]
    CTX --> JOB["Job and event metadata"]
    CTX --> ANA["Analytics scoping"]
```

## 2.8 Secrets and credential flow

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Admin UI
    participant API as Support API
    participant SM as Secret manager
    participant DB as Postgres
    participant CN as Connector

    Admin->>UI: enter provider credential
    UI->>API: submit over TLS
    API->>SM: store secret
    SM-->>API: secret_ref
    API->>DB: save IntegrationCredentialReference secret_ref only
    API-->>UI: masked confirmation
    Note over CN,SM: runtime
    CN->>SM: resolve secret_ref
    SM-->>CN: short-lived credential in memory
    CN->>CN: call provider, never log token, never send to model
```

## 2.9 Graceful degradation

```mermaid
flowchart TD
    T["Customer turn"] --> LLM{"LLM provider healthy?"}
    LLM -- No --> D1["Tell customer of temporary unavailability or route to human"]
    LLM -- Yes --> RAG{"Retrieval healthy?"}
    RAG -- No --> D2["Do not claim grounded answer: ask clarifying question or hand off"]
    RAG -- Yes --> TOOL{"Tool needed and healthy?"}
    TOOL -- "Not needed" --> ANS["Grounded answer"]
    TOOL -- "Healthy" --> ANS
    TOOL -- "Down or circuit open" --> D3["Explain limitation, offer human or ticket"]
    D1 & D2 & D3 --> AUD["Emit failure metric and audit event"]
```

## 2.10 Data lifecycle and retention

```mermaid
flowchart LR
    subgraph Classes["Data classes with independent retention"]
        direction LR
        MSG["Messages"]
        TR["Transcripts"]
        AUDIO["Raw audio: off by default"]
        FILES["Uploaded files"]
        LOGS["Logs"]
        AUDITD["Audit events"]
        PROV["Provider payloads"]
    end
    Classes --> POL["RetentionPolicy per tenant per class"]
    POL --> JOB["Scheduled retention job"]
    JOB --> DEL["Delete or redact"]
    DEL --> PROP["Propagate to search index, caches, derived data"]
    PROP --> REC["Write deletion audit record"]
    REQ["Customer access or deletion request"] --> VERIFY{"Identity verified?"}
    VERIFY -- Yes --> JOB
    VERIFY -- No --> DENY["Reject or request verification"]
```

## 2.11 Security test matrix

```mermaid
flowchart LR
    ST["Security test checklist"] --> A["Cross-tenant read/write"]
    ST --> B["Unauthorized tool invocation"]
    ST --> C["Prompt injection: user input and retrieved docs"]
    ST --> D["Webhook signature failure and replay"]
    ST --> E["Duplicate webhook delivery"]
    ST --> F["Tool timeout with unknown write outcome"]
    ST --> G["Secret leakage in logs and traces"]
    ST --> H["Unauthorized transcript or audio access"]
    ST --> I["Rate limit and abuse"]
    A --> CI["Run in CI: blocks merge"]
    B --> CI
    D --> CI
    E --> CI
    G --> CI
    C --> EV["Run in AI evaluation: blocks agent release"]
    F --> EV
```

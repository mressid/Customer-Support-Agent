# E02 — Conversation and Message Core

Goal: persist and retrieve a reliable conversation timeline. Modules: M01, M02, M03.

## Epic overview

```mermaid
flowchart LR
    E02["E02 Conversation core"] --> US10["US-010 Start conversation"]
    E02 --> US11["US-011 Send and receive text"]
    E02 --> US12["US-012 Inspect timeline"]
    E02 --> US13["US-013 Deduplicate inbound events"]
    US10 --> US11 --> US12
    US13 -. protects .-> US11
```

## Conversation lifecycle (used by all stories)

```mermaid
stateDiagram-v2
    [*] --> Open
    Open --> AiHandling: turn requested
    AiHandling --> Open: turn completed
    Open --> HandoffPending: escalation
    AiHandling --> HandoffPending: escalation
    HandoffPending --> HumanOwned: agent claims
    HumanOwned --> Open: returned to AI
    HumanOwned --> Resolved: agent resolves
    Open --> Resolved: customer satisfied or idle timeout
    Resolved --> Open: reopen on new message
    Resolved --> Closed: retention window passed
    Closed --> [*]
```

## US-010 — Start a conversation through website chat

Acceptance: tenant and channel scoped, initial event persisted.

```mermaid
sequenceDiagram
    actor V as Visitor
    participant W as Widget
    participant API as Support API
    participant CH as Channel service
    participant CV as Conversation service
    participant DB as Postgres

    V->>W: opens chat
    W->>API: start session with widget public key
    API->>CH: resolve ChannelConnection and organization
    CH-->>API: tenant context
    API->>CV: create conversation
    CV->>DB: insert conversation, customer identity (anonymous), conversation.created event
    CV->>DB: insert outbox event
    CV-->>API: conversation id
    API-->>W: session token and conversation id
```

## US-011 — Send and receive text messages

Acceptance: stable ordering, delivery status represented, errors recoverable.

### Ordering and persistence

```mermaid
sequenceDiagram
    participant W as Widget
    participant API as Support API
    participant CV as Conversation service
    participant DB as Postgres
    participant Q as Queue

    W->>API: send message with client_message_id
    API->>CV: append inbound
    CV->>DB: BEGIN
    CV->>DB: lock conversation row or use sequence
    CV->>DB: insert message with next sequence number
    CV->>DB: insert outbox message.persisted
    CV->>DB: COMMIT
    CV-->>API: message with sequence
    API-->>W: ack with server id
    DB-->>Q: relay ai.turn.requested
```

### Message delivery status as seen by the customer

```mermaid
stateDiagram-v2
    [*] --> Sending: client submits
    Sending --> Sent: server ack
    Sending --> FailedLocal: network error
    FailedLocal --> Sending: retry with same client_message_id
    Sent --> Delivered: widget confirms render
    Delivered --> [*]
```

## US-012 — Support agent inspects the timeline

Acceptance: messages, system events and visibility levels are distinguished.

```mermaid
flowchart TD
    A["Agent opens conversation"] --> B{"Has conversation.read permission in tenant?"}
    B -- No --> X["403"]
    B -- Yes --> C["Load ordered items"]
    C --> D{"Item kind"}
    D -- "text, file, audio_reference" --> E["Show as customer or assistant bubble"]
    D -- system_event --> F["Show as inline event: voice started, handoff"]
    D -- internal_note --> G["Show only to agents with badge: not customer visible"]
    D -- transcript_segment --> H["Show with modality icon"]
    E & F & G & H --> I["Timeline view"]
    I --> J["Customer widget query uses visibility=customer filter"]
```

## US-013 — Deduplicate inbound events

Acceptance: a replayed provider event does not create a duplicate message.

```mermaid
flowchart TD
    A["Inbound event arrives"] --> B["Compute key: connection id + provider_event_id"]
    B --> C["INSERT into inbound inbox with unique constraint"]
    C --> D{"Unique violation?"}
    D -- Yes --> E["Return previous result 200: no new message"]
    D -- No --> F["Process event"]
    F --> G["Create message"]
    G --> H["Mark inbox row processed"]
    F -. crash before mark .-> I["Retry picks up row: message insert is idempotent on provider_event_id"]
```

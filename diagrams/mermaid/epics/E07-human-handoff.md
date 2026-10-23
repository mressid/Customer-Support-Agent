# E07 — Human Inbox and Handoff

Goal: a human can take over with context. Modules: M10, M13.

## Epic overview

```mermaid
flowchart LR
    E07["E07 Human handoff"] --> US60["US-060 View unassigned queue"]
    E07 --> US61["US-061 Customer requests human"]
    E07 --> US62["US-062 Handoff summary"]
    E07 --> US63["US-063 Resolve conversation"]
    US61 --> US62 --> US60 --> US63
```

## Ownership model

```mermaid
stateDiagram-v2
    [*] --> AiOwned
    AiOwned --> HandoffRequested: customer asks or policy triggers
    HandoffRequested --> Queued: bundle prepared
    Queued --> Claimed: agent claims (optimistic lock)
    Claimed --> HumanOwned: AI paused
    HumanOwned --> Released: agent returns to AI
    Released --> AiOwned
    HumanOwned --> Resolved
    Queued --> Queued: reassigned
    Queued --> Abandoned: customer left
    Resolved --> [*]
    Abandoned --> [*]
```

## US-060 — Support agent views the unassigned queue

Acceptance: tenant scoped, supports assignment.

```mermaid
sequenceDiagram
    actor A1 as Agent 1
    actor A2 as Agent 2
    participant API as Support API
    participant IN as Inbox service
    participant DB as Postgres

    A1->>API: GET queue (tenant from token)
    API->>IN: list unassigned for queues agent belongs to
    IN->>DB: SELECT with organization filter
    DB-->>A1: items by priority and wait time
    A1->>API: claim item 42 (version v1)
    A2->>API: claim item 42 (version v1)
    API->>DB: UPDATE where version = v1
    DB-->>A1: success
    DB-->>A2: conflict
    API-->>A2: already claimed, refresh queue
```

## US-061 — Customer requests a human

Acceptance: AI stops responding when handoff policy requires; clear status for customer.

```mermaid
flowchart TD
    A["Customer: I want a human"] --> B["AI detects request, reason=customer_requested"]
    B --> C{"Handoff allowed now? business hours, queue open"}
    C -- Yes --> D["Set conversation HandoffPending, pause AI"]
    C -- No --> E["Offer ticket or callback, tell expected hours"]
    D --> F["Build handoff bundle"]
    F --> G["Route to queue by routing rules"]
    G --> H["Tell customer: connecting you to an agent"]
    H --> I["Emit human.handoff.requested"]
    I --> J["Further AI replies suppressed until released"]
    E --> K["Create ticket"]
```

## US-062 — Handoff summary for the agent

Acceptance: transcript, unresolved request, prior tool outcomes permitted by policy.

```mermaid
flowchart LR
    subgraph Inputs
        direction LR
        T["Transcript"]
        I["Intent and unresolved question"]
        TL["Tool executions: ok and failed"]
        C["Citations used"]
        K["Ticket and SLA state"]
        V["Verification level"]
    end
    Inputs --> S["Summarizer: model call over trusted data"]
    S --> P{"Policy filter: agent permission to see restricted data?"}
    P -- No --> R["Redact or mask fields"]
    P -- Yes --> B
    R --> B["Handoff bundle"]
    B --> UI["Agent console panel"]
    B --> N["Stored with HandoffEvent"]
```

## US-063 — Support agent resolves the conversation

Acceptance: resolution and ownership changes recorded.

```mermaid
sequenceDiagram
    actor Ag as Agent
    participant API
    participant IN as Inbox
    participant CV as Conversation
    participant TK as Tickets
    participant AUD as Audit

    Ag->>API: resolve with outcome and note
    API->>IN: close assignment
    IN->>CV: set status Resolved, owner none
    IN->>TK: link or update ticket if one exists
    IN->>AUD: ownership change and resolution recorded
    CV-->>Ag: done
    Note over CV: new customer message later reopens conversation
```

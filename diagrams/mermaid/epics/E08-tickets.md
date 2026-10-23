# E08 — Tickets and Case Tracking

Goal: track support work beyond one interaction. Module: M11.

## Epic overview

```mermaid
flowchart LR
    E08["E08 Tickets"] --> US70["US-070 Create ticket from conversation"]
    E08 --> US71["US-071 Filter tickets"]
    US70 --> US71
```

## Conversation vs ticket

```mermaid
flowchart LR
    C1["Conversation 1 chat"] --> T["Ticket: work to resolve"]
    C2["Conversation 2 voice"] --> T
    C3["Conversation 3 email later"] --> T
    T --> H["Status history"]
    T --> CM["Comments"]
    T --> A["Assignment"]
```

## Ticket status lifecycle

```mermaid
stateDiagram-v2
    [*] --> New
    New --> Open: assigned or triaged
    Open --> Pending: waiting on customer
    Pending --> Open: customer replies
    Open --> Resolved
    Resolved --> Open: reopened
    Resolved --> Closed: after grace period
    Closed --> [*]
```

## US-070 — Create a ticket from a conversation

Acceptance: ticket links to source conversation and has a status history.

```mermaid
sequenceDiagram
    actor Ag as Agent
    participant API
    participant TK as Ticket service
    participant CV as Conversation service
    participant DB as Postgres

    Ag->>API: create ticket from conversation 42
    API->>TK: create(title, priority, category, conversation id)
    TK->>CV: verify conversation in same tenant
    TK->>DB: BEGIN
    TK->>DB: insert Ticket status=New
    TK->>DB: insert link ticket to conversation
    TK->>DB: insert TicketStatusHistory (null to New)
    TK->>DB: insert outbox ticket.created
    TK->>DB: COMMIT
    TK-->>Ag: ticket id
    Note over CV: conversation gets system_event ticket linked
```

AI-initiated variant:

```mermaid
flowchart LR
    AI["AI cannot resolve"] --> P{"Policy allows AI ticket creation?"}
    P -- Yes --> T["Create ticket with summary, source=ai"]
    P -- No --> H["Handoff to human who creates ticket"]
```

## US-071 — Support lead filters tickets

Acceptance: filters respect permissions and tenant boundaries.

```mermaid
flowchart TD
    A["Lead sets filters: status, priority, assignee, queue, date"] --> B["API validates filter fields allowlist"]
    B --> C["Tenant scope from token"]
    C --> D{"Permission scope"}
    D -- "tickets.read.all" --> E["All tenant tickets"]
    D -- "tickets.read.team" --> F["Only team queues"]
    D -- "tickets.read.own" --> G["Only assigned to caller"]
    E & F & G --> H["Indexed query with pagination and stable sort"]
    H --> I["Result list with counts"]
```

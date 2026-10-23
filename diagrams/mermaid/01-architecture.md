# 01 — Architecture Diagrams

Source: `03-system-architecture.md`, `02-module-catalog.md`, `04-module-communication.md`.
Large module map is split into five domain views (A–E) plus one combined dependency view.

## 1.1 System context

```mermaid
flowchart LR
    Customer(["Customer"])
    Agent(["Support Agent"])
    Lead(["Support Lead"])
    Admin(["Org Administrator"])
    Operator(["Platform Operator"])

    subgraph Platform["AI Customer Support Platform"]
        Widget["Website Widget"]
        API["Support API"]
        Worker["Support Worker"]
        Console["Agent Console / Admin UI"]
    end

    subgraph External["External providers"]
        LLM["LLM provider"]
        Speech["Speech provider STT/TTS/S2S"]
        Msg["Email / Messaging providers"]
        Biz["Business systems: CRM, Orders, Billing"]
    end

    Customer --> Widget --> API
    Customer -. later .-> Msg --> API
    Agent --> Console --> API
    Lead --> Console
    Admin --> Console
    Operator --> Telemetry[("Telemetry")]
    API --> Worker
    API --> LLM
    API --> Speech
    API --> Biz
    Worker --> Msg
    API --> Telemetry
    Worker --> Telemetry
```

## 1.2 Logical layers

```mermaid
flowchart TB
    L1["1 Edge and channel adapters<br/>widget, webhooks, voice transport, email/messaging"]
    L2["2 Application API<br/>authN, tenant resolution, validation, rate limiting"]
    L3["3 Conversation domain<br/>sessions, messages, turns, lifecycle"]
    L4["4 AI orchestration<br/>model routing, policy, retrieval, tool planning, response"]
    L5["5 Capability modules<br/>knowledge, tools, workflow, tickets, human inbox"]
    L6["6 Infrastructure adapters<br/>SQL, object storage, vector index, queue, LLM, speech"]
    X["7 Cross-cutting<br/>security, audit, observability, evaluation, usage"]

    L1 --> L2 --> L3 --> L4 --> L5 --> L6
    X -.-> L1
    X -.-> L2
    X -.-> L3
    X -.-> L4
    X -.-> L5
    X -.-> L6
```

## 1.3 MVP deployable components

```mermaid
flowchart LR
    subgraph Clients
        W["support-web-widget"]
        C["support-agent-console"]
    end
    subgraph App["Modular monolith (one codebase)"]
        A["support-api"]
        K["support-worker"]
    end
    subgraph Data
        PG[("postgres")]
        OS[("object-storage")]
        Q[["queue"]]
        V[("vector-search")]
    end
    T["telemetry: logs, metrics, traces, alerts"]

    W --> A
    C --> A
    A --> PG
    A --> OS
    A --> V
    A --> Q
    Q --> K
    K --> PG
    K --> OS
    K --> V
    A -.-> T
    K -.-> T
```

## 1.4 Module map — split by domain

### A. Customer interaction and conversation (M01–M03)

```mermaid
flowchart LR
    M02["M02 Channel Management<br/>adapters, webhooks, delivery"]
    M01["M01 Conversation Management<br/>lifecycle, turns, messages"]
    M03["M03 Customer Identity<br/>profiles, contacts, consent"]
    M02 -->|canonical inbound event| M01
    M01 -->|delivery command| M02
    M01 -->|resolve customer| M03
    M02 -->|provider identity| M03
```

### B. AI conversation and voice (M04–M09)

```mermaid
flowchart LR
    M04["M04 AI Engine"]
    M05["M05 Knowledge / RAG"]
    M06["M06 Tools and Actions"]
    M07["M07 Real-time Voice Sessions"]
    M08["M08 Speech Processing"]
    M09["M09 Transcript Sync"]
    M01["M01 Conversation"]
    M04 -->|retrieve| M05
    M04 -->|tool request| M06
    M07 --> M08
    M08 --> M09
    M09 -->|final transcript| M01
    M01 -->|new turn| M04
    M04 -->|response text| M08
```

### C. Support operations (M10–M14)

```mermaid
flowchart LR
    M04["M04 AI Engine"] -->|handoff request| M10["M10 Human Inbox"]
    M10 --> M11["M11 Tickets"]
    M13["M13 Routing / SLA"] --> M10
    M12["M12 Workflows"] --> M13
    M12 --> M14["M14 Notifications"]
    M11 -->|status events| M14
    M10 -->|ownership events| M01["M01 Conversation"]
```

### D. Integrations and insights (M15–M17)

```mermaid
flowchart LR
    M06["M06 Tools"] --> M15["M15 Integration Hub"]
    M15 --> Ext["Business systems"]
    M01["M01 Conversation"] --> M16["M16 Analytics"]
    M04["M04 AI Engine"] --> M17["M17 Evaluation"]
    M17 -->|release gate| M19["M19 Agent Config"]
    M16 --> M17
```

### E. Platform and governance (M18–M20)

```mermaid
flowchart LR
    M18["M18 Orgs, Users, Access"]
    M19["M19 Agent Configuration"]
    M20["M20 Security, Audit, Telemetry, Usage"]
    M18 -->|tenant context| M19
    M19 -->|published AgentVersion| M04["M04 AI Engine"]
    M20 -.->|cross-cutting| M18
    M20 -.-> M19
    M20 -.-> M04
```

## 1.5 Combined module dependency view

```mermaid
flowchart TB
    subgraph Platform
        M18 --> M19
    end
    subgraph Core
        M02 --> M01
        M01 --> M04
        M19 --> M04
        M04 --> M05
        M04 --> M06
        M04 --> M10
    end
    subgraph Voice
        M07 --> M08 --> M09 --> M01
    end
    subgraph Ops
        M10 --> M11
        M12 --> M13
    end
    M06 --> M15
    M01 --> M16
    M04 --> M17
    M20 -.-> M01
    M20 -.-> M04
    M20 -.-> M15
```

## 1.6 Event catalog by lifecycle

```mermaid
flowchart LR
    subgraph Inbound
        e1["message.received"] --> e2["message.persisted"]
        e0["conversation.created"]
    end
    subgraph AI
        e3["ai.turn.requested"] --> e4["ai.turn.completed"]
        e5["tool.execution.requested"] --> e6["tool.execution.completed"]
    end
    subgraph Handoff
        e7["human.handoff.requested"] --> e8["human.handoff.accepted"]
        e9["ticket.created"]
    end
    subgraph Delivery
        d1["channel.delivery.requested"] --> d2["channel.delivery.completed"]
        d1 --> d3["channel.delivery.failed"]
    end
    subgraph Knowledge
        k1["knowledge.source.ingestion.requested"] --> k2["knowledge.source.ingestion.completed"]
    end
    subgraph Voice
        v1["voice.session.started"] --> v2["voice.session.ended"]
    end
    subgraph Governance
        g1["evaluation.run.completed"]
        g2["usage.recorded"]
    end
    e2 --> e3
    e4 --> d1
    e4 --> e5
    e4 --> e7
```

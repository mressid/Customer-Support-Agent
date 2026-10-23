# Scrum Mermaid Artifacts (copied from scrum/05-mermaid-artifacts.md)

Paste these blocks into a Mermaid-compatible Markdown renderer. Keep them in source control and update them when the backlog or delivery plan changes.

## 1. Product roadmap

```mermaid
flowchart TD
    A[Product Goal: reliable AI customer support] --> B[Release 1: Text MVP]
    B --> B1[Tenant and access]
    B --> B2[Conversation core]
    B --> B3[Website chat]
    B --> B4[Knowledge and RAG]
    B --> B5[AI orchestration]
    B --> B6[Safe read-only tool]
    B --> B7[Human handoff and ticket basics]
    B --> C[Release 2: Voice MVP]
    C --> C1[Voice sessions]
    C --> C2[STT/TTS or speech-to-speech]
    C --> C3[Transcript synchronization]
    C --> C4[Interruption and handoff]
    C --> D[Release 3: Operations expansion]
    D --> D1[Workflow automation]
    D --> D2[Routing and SLA]
    D --> D3[Additional channels/connectors]
    D --> D4[Evaluation and usage maturity]
```

## 2. Epic dependency graph

```mermaid
flowchart LR
    E01[E01 Tenant and Access] --> E02[E02 Conversation Core]
    E01 --> E04[E04 Knowledge and RAG]
    E02 --> E03[E03 Website Chat]
    E02 --> E05[E05 AI Orchestration]
    E04 --> E05
    E05 --> E06[E06 Safe Business Tools]
    E02 --> E07[E07 Human Handoff]
    E07 --> E08[E08 Tickets]
    E05 --> E09[E09 Voice MVP]
    E02 --> E09
    E06 --> E10[E10 Workflow/Routing/SLA]
    E03 --> E11[E11 More Channels/Integrations]
    E05 --> E12[E12 Evaluation/Usage]
    E06 --> E12
    E09 --> E12
```

## 3. Provisional Sprint timeline

```mermaid
gantt
    title Proposed Delivery Plan (two-week Sprints)
    dateFormat YYYY-MM-DD
    axisFormat %b %d
    section Foundations
    Sprint 1 - Secure conversation core :s1, 2026-11-02, 14d
    Sprint 2 - Website chat slice       :s2, after s1, 14d
    section AI MVP
    Sprint 3 - Knowledge ingestion      :s3, after s2, 14d
    Sprint 4 - Grounded AI answers      :s4, after s3, 14d
    Sprint 5 - Tool and handoff         :s5, after s4, 14d
    Sprint 6 - Tickets and hardening    :s6, after s5, 14d
    section Voice
    Sprint 7 - Voice technical slice    :s7, after s6, 14d
    Sprint 8 - Multimodal synchronization :s8, after s7, 14d
```

**Important:** the dates above are illustrative placeholders to demonstrate the Gantt syntax, not a proposed current calendar. Replace the start date with the team's actual Sprint start date.

## 4. Scrum workflow

```mermaid
flowchart TD
    PB[Product Backlog] --> REF[Ongoing Refinement]
    REF --> PLAN[Sprint Planning]
    PLAN --> SB[Sprint Backlog + Sprint Goal]
    SB --> DEV[Design, Build, Test, Integrate]
    DEV --> DS{Meets Definition of Done?}
    DS -- No --> DEV
    DS -- Yes --> INC[Potentially Releasable Increment]
    INC --> REVIEW[Sprint Review]
    REVIEW --> FB[Stakeholder Feedback]
    FB --> PB
    REVIEW --> RETRO[Sprint Retrospective]
    RETRO --> IMP[Improvement Actions]
    IMP --> PLAN
    DEV --> DAILY[Daily Scrum: inspect and adapt]
    DAILY --> DEV
```

## 5. User story lifecycle

```mermaid
stateDiagram-v2
    [*] --> Candidate
    Candidate --> Refinement
    Refinement --> Ready
    Ready --> Selected
    Selected --> InProgress
    InProgress --> Review
    Review --> InProgress: changes requested
    Review --> Done: DoD met
    InProgress --> Blocked
    Blocked --> InProgress
    Done --> [*]
```

## 6. Release acceptance flow

```mermaid
flowchart TD
    A[Feature implemented] --> B[Unit and integration tests]
    B --> C[Tenant and authorization tests]
    C --> D[AI regression/evaluation]
    D --> E[Latency, cost, and failure-path checks]
    E --> F{Release criteria met?}
    F -- No --> G[Fix, document, or defer]
    G --> A
    F -- Yes --> H[Versioned release]
    H --> I[Monitor rollout]
    I --> J{Healthy?}
    J -- Yes --> K[Continue rollout]
    J -- No --> L[Rollback / disable feature]
```

## 7. Sprint Review demo path for the Text MVP

```mermaid
sequenceDiagram
    actor Customer
    participant Widget as Website Widget
    participant API as Support API
    participant Conv as Conversation Module
    participant AI as AI Engine
    participant RAG as Knowledge/RAG
    participant Tool as Tool Service
    participant Inbox as Human Inbox

    Customer->>Widget: Ask a question
    Widget->>API: Send message
    API->>Conv: Persist normalized message
    Conv->>AI: Request turn
    AI->>RAG: Retrieve approved sources
    RAG-->>AI: Relevant passages and source IDs
    opt Live business data required
        AI->>Tool: Request allowed read-only tool
        Tool-->>AI: Authorized result
    end
    AI-->>Conv: Final response and metadata
    Conv-->>Widget: Deliver response
    alt Cannot resolve / customer asks for human
        AI->>Inbox: Request handoff with context
        Inbox-->>Conv: Human takes ownership
    end
```

## 8. Module-to-epic coverage

```mermaid
flowchart TB
    subgraph Customer["Customer interaction"]
      M01[M01 Conversation]
      M02[M02 Channels]
      M03[M03 Customer identity]
    end
    subgraph AI["AI and multimodal"]
      M04[M04 AI engine]
      M05[M05 Knowledge/RAG]
      M06[M06 Tools]
      M07[M07 Voice sessions]
      M08[M08 Speech]
      M09[M09 Transcript sync]
    end
    subgraph Ops["Support operations"]
      M10[M10 Human inbox]
      M11[M11 Tickets]
      M12[M12 Workflows]
      M13[M13 Routing/SLA]
      M14[M14 Notifications]
    end
    subgraph Business["Integrations and insight"]
      M15[M15 Integration hub]
      M16[M16 Analytics]
      M17[M17 AI evaluation]
    end
    subgraph Platform["Platform"]
      M18[M18 Tenant/access]
      M19[M19 Agent configuration]
      M20[M20 Security/telemetry/usage]
    end
    M18 --> M01
    M18 --> M02
    M18 --> M05
    M19 --> M04
    M04 --> M05
    M04 --> M06
    M02 --> M01
    M07 --> M08
    M08 --> M09
    M09 --> M01
    M04 --> M10
    M10 --> M11
    M06 --> M15
    M12 --> M13
    M01 --> M16
    M04 --> M17
    M20 -.cross-cutting.-> M01
    M20 -.cross-cutting.-> M04
    M20 -.cross-cutting.-> M15
```

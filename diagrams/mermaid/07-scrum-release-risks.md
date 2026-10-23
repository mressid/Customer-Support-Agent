# 07 — Scrum, Release and Risk Diagrams

Source: `scrum/00` to `scrum/06`. These extend the 8 diagrams already in `scrum/05-mermaid-artifacts.md`, which are not repeated here.

## 7.1 Scrum roles and accountabilities

```mermaid
flowchart LR
    PO["Product Owner<br/>value, goal, backlog order"] --> PB[("Product Backlog")]
    SM["Scrum Master<br/>coaching, impediments"] -. coaches .-> DEV
    DEV["Developers<br/>design, build, test, secure, operate"] --> INC["Increment"]
    PB --> DEV
    STK["Stakeholders: support, admins, security, business-system owners"] --> REV["Sprint Review"]
    INC --> REV
    REV --> PO
```

## 7.2 Scrum events within a sprint

```mermaid
sequenceDiagram
    participant PO as Product Owner
    participant DEV as Developers
    participant SM as Scrum Master
    participant STK as Stakeholders

    Note over PO,DEV: Sprint Planning: goal, selected items, plan
    PO->>DEV: ordered backlog and goal proposal
    DEV->>DEV: select items by capacity and DoD
    loop each working day
        DEV->>DEV: Daily Scrum 15 minutes, adapt plan
    end
    Note over PO,DEV: refinement continues in parallel (not an event)
    DEV->>STK: Sprint Review: demo working software
    STK-->>PO: feedback, backlog reordering
    DEV->>SM: Sprint Retrospective
    SM-->>DEV: one or two improvement actions
```

## 7.3 Definition of Ready check

```mermaid
flowchart LR
    A["Backlog item"] --> CL
    subgraph CL["Ready checklist: all must hold"]
        direction LR
        c1["Outcome is clear"]
        c2["Acceptance criteria are testable"]
        c3["Dependencies and provider assumptions identified"]
        c4["UX, API and data understood"]
        c5["Security and privacy considered"]
        c6["Fits in one Sprint and is estimated"]
        c7["Credentials, test data and environments available or planned"]
    end
    CL -- "all hold" --> OK["Ready for Sprint Planning"]
    CL -- "not clear" --> R["Refine"]
    CL -- "too large" --> S["Split the item"] --> R
    CL -- "no environment yet" --> P["Plan to obtain, may start as spike"] --> R
    R --> A
```

## 7.4 Definition of Done layers

```mermaid
flowchart TB
    subgraph Base["Base DoD"]
        b1["Acceptance criteria met"]
        b2["Code reviewed, module boundaries respected"]
        b3["Automated tests incl. failure cases"]
        b4["Tenant isolation and authorization tested"]
        b5["Validation and error handling"]
        b6["Migrations reviewed and repeatable"]
        b7["Safe correlation fields in telemetry, redaction"]
        b8["Docs and contracts updated"]
        b9["No unaccepted critical or high defects"]
        b10["Rollback or feature flag understood"]
        b11["Product Owner can inspect behavior"]
    end
    subgraph AI["AI add-on"]
        a1["Model and prompt version identifiable"]
        a2["Tool schemas validated, permissions in code"]
        a3["Retrieval tenant scoped"]
        a4["Empty retrieval and uncertainty paths tested"]
        a5["Regression example added"]
        a6["No secrets or hidden reasoning in logs"]
    end
    subgraph Voice["Voice add-on"]
        v1["Mic permission and active state clear"]
        v2["Cleanup on disconnect"]
        v3["Interruption tested"]
        v4["Transcript finalization and ordering tested"]
        v5["Audio and transcript retention per policy"]
        v6["Latency and failure metrics emitted"]
    end
    Base --> DONE(["Done"])
    AI -->|"if AI-related"| DONE
    Voice -->|"if voice-related"| DONE
```

## 7.5 Release exit criteria

### Release 1 — Text MVP

```mermaid
flowchart LR
    R1(["R1 Text MVP"]) --> c1["Tenant isolation tests pass"]
    R1 --> c2["Inbound dedupe works"]
    R1 --> c3["Safe fallback for unknown questions"]
    R1 --> c4["Tools allowlisted, authorized, audited"]
    R1 --> c5["Human can take over"]
    R1 --> c6["API and worker telemetry available"]
    R1 --> c7["No unresolved critical eval failure"]
    c1 & c2 & c3 & c4 & c5 & c6 & c7 --> GO{"All met?"}
    GO -- Yes --> SHIP["Ship"]
    GO -- No --> HOLD["Hold and fix"]
```

### Release 2 — Voice MVP

```mermaid
flowchart LR
    R2(["R2 Voice MVP"]) --> v1["Session start, stop, cleanup reliable"]
    R2 --> v2["Transcript finalization and ordering"]
    R2 --> v3["Interruption tested"]
    R2 --> v4["Audio and transcript privacy policy implemented"]
    R2 --> v5["Latency and cost metrics visible"]
    R2 --> v6["Handoff validated for selected provider"]
    v1 & v2 & v3 & v4 & v5 & v6 --> GO{"All met?"}
    GO -- Yes --> SHIP["Ship"]
    GO -- No --> HOLD["Hold and fix"]
```

## 7.6 Rollout and rollback

```mermaid
flowchart TD
    A["Versioned release created"] --> B["Deploy behind feature flag, 0 percent"]
    B --> C["Internal tenant test"]
    C --> D["Canary tenants 5 percent"]
    D --> E{"SLO, error rate, eval sample, cost healthy?"}
    E -- Yes --> F["Increase to 25, 50, 100 percent"]
    F --> E
    E -- No --> G["Disable flag or roll back AgentVersion"]
    G --> H["Incident review without blame"]
    H --> I["Add regression case"]
```

## 7.7 Risk map

```mermaid
flowchart LR
    R1["Prompt injection"] --> M1["Tool allowlist, server authz, untrusted-content boundary, adversarial tests"]
    R2["Tenant leakage in retrieval"] --> M2["Tenant-scoped indexes and filters, access tests, per-tenant object controls"]
    R3["LLM latency and cost"] --> M3["Budgets, timeouts, model routing, safe caching, measurement"]
    R4["Duplicate webhook or tool execution"] --> M4["Durable inbox, idempotency keys, dedupe"]
    R5["Voice interruption and transcript race"] --> M5["Sequence ids, partial vs final, cancellation semantics"]
    R6["Provider lock-in"] --> M6["Adapters, normalized contracts, contract tests"]
    R7["Unsupported AI answer"] --> M7["Retrieval eval, evidence thresholds, fallback and handoff"]
    R8["Scope too broad"] --> M8["Text MVP vertical slice, ordered backlog, defer channels"]
    M1 --> S1["E06 US-050 US-053, E12 US-112"]
    M2 --> S2["E01 US-003, E04 US-032"]
    M4 --> S4["E02 US-013, E06 US-052"]
    M5 --> S5["E09 US-082 US-083"]
    M7 --> S7["E04 US-033, E07 US-061"]
```

## 7.8 ADR dependency order

```mermaid
flowchart TD
    A1["ADR-001 Modular monolith boundaries"] --> A2["ADR-002 Database and tenant isolation"]
    A2 --> A3["ADR-003 Queue and outbox/inbox"]
    A2 --> A4["ADR-004 Vector/search technology"]
    A1 --> A5["ADR-005 LLM abstraction and data policy"]
    A2 --> A9["ADR-009 Authentication and customer verification"]
    A9 --> A10["ADR-010 Tool authorization and approval"]
    A5 --> A6["ADR-006 Voice strategy"]
    A6 --> A7["ADR-007 Browser voice transport and telephony"]
    A7 --> A8["ADR-008 Audio and transcript retention and consent"]
    classDef early fill:#e6f4ea,stroke:#2e7d32
    classDef later fill:#fff4e5,stroke:#ef6c00
    class A1,A2,A3,A4,A5,A9,A10 early
    class A6,A7,A8 later
```

## 7.9 Decisions to defer

```mermaid
flowchart LR
    D(["Do not decide yet"]) --> a["One microservice per module"]
    D --> b["Universal workflow builder"]
    D --> c["Multiple speech providers"]
    D --> d["Autonomous write access to all systems"]
    D --> e["Permanent raw audio retention"]
    D --> f["Complex billing and subscriptions"]
    a & b & c & d & e & f --> W["Revisit with evidence: scale, usage, validated need"]
```

## 7.10 Epic delivery map by release

```mermaid
flowchart LR
    subgraph R1["Release 1 Text MVP"]
        E01 --> E02 --> E03
        E01 --> E04
        E02 & E04 --> E05 --> E06
        E02 --> E07 --> E08
    end
    subgraph R2["Release 2 Voice MVP"]
        E09
    end
    subgraph R3["Release 3 Operations"]
        E10
        E11
    end
    E12["E12 Observability and evaluation (minimal in R1, advanced in R3)"]
    E05 & E02 --> E09
    E06 --> E10
    E03 --> E11
    E05 & E06 & E09 --> E12
```

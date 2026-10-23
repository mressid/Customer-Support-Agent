# 06 — Sprint Diagrams

Source: `scrum/02-sprint-plan.md`. Sprint length is assumed to be two weeks. The plan is a hypothesis, to be re-forecast after Sprint 1.

## 6.1 Sprint sequence and goals

```mermaid
flowchart TB
    subgraph row1["Foundations"]
        direction LR
        S0["Sprint 0<br/>Enablement (if needed)"] --> S1["Sprint 1<br/>Secure conversation foundation"] --> S2["Sprint 2<br/>Website chat slice"] --> S3["Sprint 3<br/>Knowledge ingestion"]
    end
    subgraph row2["AI MVP and Release 1"]
        direction LR
        S4["Sprint 4<br/>Grounded AI answers"] --> S5["Sprint 5<br/>Tool and handoff"] --> S6["Sprint 6<br/>Tickets and hardening"] --> R1{{"Release 1<br/>Text MVP"}}
    end
    subgraph row3["Voice and Release 2"]
        direction LR
        S7["Sprint 7<br/>Voice technical slice"] --> S8["Sprint 8<br/>Voice sync and handoff"] --> R2{{"Release 2<br/>Voice MVP"}}
    end
    row1 --> row2 --> row3
```

## 6.2 Increment growth: what the demo can show after each sprint

```mermaid
flowchart TB
    I1["After S1: create conversation, store messages, cross-tenant denied"]
    I2["After S2: visitor chat works end to end, dedupe and reconnect"]
    I3["After S3: upload document, ingestion status, retrieval with sources"]
    I4["After S4: grounded FAQ answers, fallback, provider timeout handled"]
    I5["After S5: order lookup tool, tool audit, human takeover with context"]
    I6["After S6: tickets, versions and rollback, tracing, eval, runbooks"]
    I7["After S7: one spoken turn linked to conversation"]
    I8["After S8: interrupt, mix text and voice, voice handoff"]
    I1 --> I2 --> I3 --> I4 --> I5 --> I6 --> I7 --> I8
```

## 6.3 Gantt (placeholder dates)

```mermaid
gantt
    title Proposed Delivery Plan (two-week Sprints, placeholder start date)
    dateFormat YYYY-MM-DD
    axisFormat %b %d
    section Foundations
    Sprint 0 Enablement optional          :s0, 2026-10-19, 14d
    Sprint 1 Secure conversation core     :s1, after s0, 14d
    Sprint 2 Website chat slice           :s2, after s1, 14d
    section AI MVP
    Sprint 3 Knowledge ingestion          :s3, after s2, 14d
    Sprint 4 Grounded AI answers          :s4, after s3, 14d
    Sprint 5 Tool and handoff             :s5, after s4, 14d
    Sprint 6 Tickets and hardening        :s6, after s5, 14d
    section Voice
    Sprint 7 Voice technical slice        :s7, after s6, 14d
    Sprint 8 Multimodal synchronization   :s8, after s7, 14d
```

## 6.4 Per-sprint detail

### Sprint 0 — Enablement

```mermaid
flowchart TD
    G0(["Goal: team can build, test and release safely"])
    G0 --> A["Repo and module package structure"]
    G0 --> B["CI: format, static analysis, tests"]
    G0 --> C["Local env and DB migrations"]
    G0 --> D["Threat model and first ADRs"]
    G0 --> E["Minimal deployment and secret handling"]
    G0 --> F["Definition of Done agreed"]
    A & B & C & D & E & F --> OUT["Walking skeleton deployed"]
    NOTE["Do not turn Sprint 0 into a permanent phase"] -.-> G0
```

### Sprint 1 — Secure conversation foundation

```mermaid
flowchart TD
    G1(["Goal: tenant-scoped conversation and message created, persisted, retrieved"])
    G1 --> U1["US-001 Organization foundation"]
    G1 --> U3["US-003 Tenant isolation test foundation"]
    G1 --> U10["US-010 Conversation creation"]
    G1 --> U11["US-011 Text message persistence"]
    G1 --> C1["Audit and correlation ID conventions"]
    U1 --> U10 --> U11
    U1 --> U3
    U11 --> DEMO["Demo: create, append, fetch timeline, prove cross-tenant denied"]
    U3 --> DEMO
    C1 --> DEMO
```

### Sprint 2 — Website chat vertical slice

```mermaid
flowchart TD
    G2(["Goal: visitor exchanges text with backend reliably"])
    G2 --> U20["US-020 Widget configuration"]
    G2 --> U21["US-021 Chat session"]
    G2 --> U22["US-022 Reconnect and resume"]
    G2 --> U13["US-013 Inbound deduplication"]
    G2 --> D["Delivery and error states, tracing"]
    U20 --> U21 --> U22
    U13 --> DEMO
    U22 --> DEMO["Demo: send message, persisted and returned, duplicate and reconnect tests"]
    D --> DEMO
```

### Sprint 3 — Knowledge ingestion and retrieval

```mermaid
flowchart TD
    G3(["Goal: knowledge ingested and retrieved with tenant boundaries"])
    G3 --> U30["US-030 Source registration and upload"]
    G3 --> U31["US-031 Async parse, chunk, index"]
    G3 --> U32["US-032 Retrieval with source metadata"]
    G3 --> ST["Ingestion status and failure retry"]
    U30 --> U31 --> U32
    U31 --> ST
    U32 --> DEMO["Demo: upload, status, query, source references"]
    ST --> DEMO
```

### Sprint 4 — Grounded AI answers

```mermaid
flowchart TD
    G4(["Goal: chat answers common questions from approved knowledge, handles missing evidence"])
    G4 --> U40["US-040 Turn orchestration"]
    G4 --> U33["US-033 Grounded response or fallback"]
    G4 --> U41["US-041 Follow-up context"]
    G4 --> U42["US-042 Model failure handling"]
    G4 --> EV["Minimal evaluation set and usage recording"]
    U40 --> U33 --> U41
    U40 --> U42
    U33 --> DEMO["Demo: grounded FAQ, follow-up, unknown fallback, provider timeout"]
    U41 --> DEMO
    U42 --> DEMO
    EV --> DEMO
```

### Sprint 5 — Safe business tool and human handoff

```mermaid
flowchart TD
    G5(["Goal: one authorized read-only lookup and transfer to human"])
    G5 --> U50["US-050 Tool registry and allowlist"]
    G5 --> U51["US-051 Order lookup"]
    G5 --> U53["US-053 Audit tool calls"]
    G5 --> U60["US-060 Inbox queue"]
    G5 --> U61["US-061 Customer-requested handoff"]
    G5 --> U62["US-062 Handoff summary"]
    U50 --> U51 --> U53
    U60 --> U61 --> U62
    U53 --> DEMO["Demo: tool success, denial and failure, human takeover with context"]
    U62 --> DEMO
```

### Sprint 6 — Tickets and release hardening

```mermaid
flowchart TD
    G6(["Goal: unresolved work tracked and MVP meets release gates"])
    G6 --> U70["US-070 Ticket creation"]
    G6 --> U71["US-071 Ticket filtering"]
    G6 --> U43["US-043 Agent version publish and rollback"]
    G6 --> U110["US-110 End-to-end tracing"]
    G6 --> U112["US-112 Initial regression evaluation"]
    G6 --> HARD["Security, load, backup and restore, runbooks"]
    U70 --> U71
    U43 --> GATE
    U112 --> GATE
    U110 --> GATE
    HARD --> GATE{"R1 exit criteria met?"}
    U71 --> GATE
    GATE -- Yes --> REL["Release 1"]
    GATE -- No --> FIX["Carry fixes to next sprint"]
```

### Sprint 7 — Voice technical spike and slice

```mermaid
flowchart TD
    G7(["Goal: validate voice architecture, complete one browser voice turn"])
    G7 --> SP["Select speech strategy and provider: latency, language, cost, privacy (ADR-006, ADR-007)"]
    G7 --> U80["US-080 Start and end session"]
    G7 --> U81["US-081 Basic speech exchange"]
    G7 --> TEL["Voice telemetry and fallback"]
    G7 --> SEC["Security and consent review (ADR-008)"]
    SP --> U80 --> U81
    U81 --> DEMO["Demo: speak, hear response, transcript linked to conversation"]
    TEL --> DEMO
    SEC --> DEMO
```

### Sprint 8 — Voice synchronization and handoff

```mermaid
flowchart TD
    G8(["Goal: voice and text share one coherent timeline"])
    G8 --> U82["US-082 Interruption"]
    G8 --> U83["US-083 Modality switching"]
    G8 --> U84["US-084 Voice handoff for chosen provider"]
    G8 --> QA["Voice quality regression scenarios"]
    G8 --> DB["Cost and latency dashboard"]
    U82 --> U83 --> U84
    U84 --> DEMO["Demo: speak, interrupt, type follow-up, transfer to human"]
    QA --> DEMO
    DB --> DEMO
```

## 6.5 Story to sprint traceability

```mermaid
flowchart LR
    subgraph E01_E02["E01 E02 E03"]
        US001 & US003 & US010 & US011 --> S1
        US020 & US021 & US022 & US013 --> S2
    end
    subgraph E04_E05["E04 E05"]
        US030 & US031 & US032 --> S3
        US040 & US033 & US041 & US042 --> S4
    end
    subgraph E06_E08["E06 E07 E08"]
        US050 & US051 & US053 & US060 & US061 & US062 --> S5
        US070 & US071 & US043 & US110 & US112 --> S6
    end
    subgraph E09["E09"]
        US080 & US081 --> S7
        US082 & US083 & US084 --> S8
    end
    subgraph Later["Unscheduled backlog"]
        US002 & US012 & US052 & US063 & US090 & US091 & US092 & US100 & US101 & US102 & US111 & US113 --> BL["Later sprints"]
    end
```

Stories without an explicit sprint in the plan (US-002, US-012, US-052, US-063, US-090 to US-092, US-100 to US-102, US-111, US-113) are flagged above as unscheduled. Several are needed by the Release 1 exit criteria (US-052 timeout safety, US-063 resolve, US-012 timeline view, US-002 user invitations) and should be pulled into Sprints 1 to 6 during refinement.

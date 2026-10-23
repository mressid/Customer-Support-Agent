# E12 — Observability, Evaluation and Usage

Goal: operate and improve the platform with evidence. Modules: M16, M17, M20. Source: `10-observability-and-evaluation.md`.

## Epic overview

```mermaid
flowchart LR
    E12["E12 Observability, evaluation, usage"] --> US110["US-110 Trace a request"]
    E12 --> US111["US-111 Resolution and handoff metrics"]
    E12 --> US112["US-112 AI regression evaluations"]
    E12 --> US113["US-113 Usage by agent and channel"]
```

## US-110 — Trace one request across modules

Acceptance: correlation ids connect API, worker, model, retrieval and tool activity.

```mermaid
sequenceDiagram
    participant W as Widget
    participant API
    participant Q as Queue
    participant WK as Worker
    participant LLM
    participant KB as Retrieval
    participant TS as Tool

    W->>API: request
    API->>API: create trace_id and correlation_id
    API->>Q: job with ids, tenant_id, causation_id
    Q->>WK: deliver, ids restored in context
    WK->>LLM: call with span and provider_request_id logged
    WK->>KB: retrieve, span
    WK->>TS: tool call, tool_execution_id in span
    Note over API,TS: all logs and spans carry trace_id, correlation_id, tenant_id, conversation_id, turn_id
```

### Correlation identifiers

```mermaid
flowchart LR
    TR["trace_id"] --> CO["correlation_id"]
    CO --> CA["causation_id: id of parent event"]
    CO --> TID["tenant_id (logs only, not metric labels)"]
    CO --> CVID["conversation_id"]
    CVID --> TN["turn_id"]
    TN --> TE["tool_execution_id"]
    TN --> PR["provider_request_id"]
```

## US-111 — Resolution and handoff metrics

Acceptance: definitions documented; metrics tenant-safe.

```mermaid
flowchart LR
    EV["Domain events via outbox"] --> AGG["Aggregation job"]
    AGG --> CO["ConversationOutcome: resolved by AI, by human, abandoned, escalated"]
    AGG --> UA["UsageAggregate"]
    CO --> DASH["Dashboard per tenant"]
    UA --> DASH
    DASH --> K1["Resolution rate"]
    DASH --> K2["Escalation rate by reason"]
    DASH --> K3["p50 and p95 latency"]
    DASH --> K4["CSAT"]
    DASH --> K5["Cost per resolved conversation"]
    GUARD["Rule: no message text, email, phone or tokens in metric labels"] -.-> AGG
```

### Platform signal groups

```mermaid
flowchart TB
    subgraph API_Platform["API and platform"]
        a1["request rate, errors, latency"]
        a2["queue depth, oldest job age"]
        a3["DB pool, slow queries"]
    end
    subgraph Conversation_Delivery["Conversation and delivery"]
        c1["inbound latency"]
        c2["delivery success and failure"]
        c3["duplicate events"]
    end
    subgraph AI_RAG["AI and RAG"]
        r1["model latency, tokens, cost"]
        r2["empty retrieval rate"]
        r3["tool proposal and success rate"]
        r4["groundedness reviews"]
    end
    subgraph Voice
        v1["time to first audio"]
        v2["interruptions"]
        v3["dropped sessions"]
    end
    API_Platform & Conversation_Delivery & AI_RAG & Voice --> ALR["Alerts and dashboards"]
```

## US-112 — Run AI regression evaluations

Acceptance: dataset and agent/model version recorded; critical policy tests gate release.

```mermaid
flowchart TD
    DS["EvaluationDataset: FAQ, ambiguous, injection, restricted data, tool failure, human request, language switch, voice errors"] --> RUN["EvaluationRun on candidate AgentVersion"]
    RUN --> DET["Deterministic assertions: permissions, schemas, state transitions"]
    RUN --> JUDGE["Model judge: one signal only"]
    RUN --> HUM["Human review sample"]
    DET & JUDGE & HUM --> SC["Scores: correctness, groundedness, clarification, tool choice, authz, handoff, tone, latency, cost"]
    SC --> CMP["Compare with baseline"]
    CMP --> G{"Critical safety and authz tests pass? Regression within threshold?"}
    G -- Yes --> REL["Create AgentRelease record, allow publish"]
    G -- No --> BLK["Block publish and report failures"]
```

### Improvement loop

```mermaid
flowchart LR
    PROD["Production conversations"] --> SAMP["Sample and redact"]
    SAMP --> REV["Human review"]
    REV --> CASE["New regression case in dataset"]
    CASE --> FIX["Prompt, retrieval or tool change"]
    FIX --> RUN["Evaluation run"]
    RUN --> PUB["Publish new version"]
    PUB --> PROD
```

## US-113 — Inspect usage by agent and channel

Acceptance: provider usage reconciled; sensitive data not exposed in metrics.

```mermaid
flowchart LR
    CALL["Model, speech, embedding calls"] --> UR["UsageRecord per call: tenant, agent version, channel, tokens or seconds"]
    UR --> AGG["Hourly aggregate"]
    PU["Provider invoice or usage export"] --> REC["Reconciliation job"]
    AGG --> REC
    REC --> DIFF{"Difference above tolerance?"}
    DIFF -- Yes --> ALERT["Alert operator"]
    DIFF -- No --> OK["Usage view by agent and channel"]
    AGG --> Q["Quota checks and rate limits"]
    Q --> BLK["Throttle or block when quota exceeded"]
```

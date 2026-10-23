# 08 — Technology Diagrams

Source: `11-technology-stack.md`, `12-technology-by-task.md`, `13-technology-decisions.md`. These show the proposed default stack. Provider-specific parts sit behind adapters, so any box marked with several options can change without touching the core domain.

## 8.1 Technology stack map

```mermaid
flowchart TB
    subgraph L1["Clients"]
        direction TB
        W["Preact widget"]
        C["React console"]
        V["WebRTC voice"]
    end
    subgraph L2["Edge"]
        direction TB
        E["CDN, WAF, TLS, gateway"]
    end
    subgraph L3["Modular monolith: TypeScript, Node.js, NestJS"]
        direction TB
        API["support-api<br/>REST, WebSocket"]
        WK["support-worker<br/>pg-boss jobs"]
    end
    subgraph L4["Data services"]
        direction LR
        PG[("PostgreSQL<br/>RLS, pgvector")]
        RD[("Redis")]
        OS[("S3 storage")]
    end
    subgraph L5["Providers behind adapters"]
        direction LR
        LLM["LLM"]
        EMB["Embeddings"]
        SPC["Speech"]
        CN["Business connectors"]
    end
    subgraph L6["Platform services"]
        direction LR
        ID["OIDC login"]
        SM["Secret manager"]
        FF["Feature flags"]
    end
    subgraph L7["Observability"]
        direction LR
        OT["OpenTelemetry"]
        GF["Grafana or Datadog"]
        SN["Sentry"]
        LF["Langfuse"]
    end
    L1 --> L2 --> L3
    L3 --> L4
    L3 --> L5
    L3 --> L6
    L3 -.-> L7
```

## 8.2 A customer message through the stack

```mermaid
flowchart TB
    subgraph R1["1. Receive and persist"]
        direction LR
        A["Widget<br/>WebSocket"] --> B["NestJS<br/>JWT, Zod, rate limit"] --> C["Postgres transaction<br/>message plus outbox"] --> D["pg-boss job<br/>ai.turn.requested"]
    end
    subgraph R2["2. Think and act"]
        direction LR
        E["Context builder"] --> F["Retrieval<br/>pgvector, full-text"] --> G["LLM adapter<br/>tool calling"] --> H["Tool service<br/>Ajv, authz, idempotency"] --> I["Connector<br/>timeout, breaker"]
    end
    subgraph R3["3. Reply"]
        direction LR
        J["Persist reply<br/>citations, usage, audit"] --> K["Delivery<br/>WebSocket push, retry"]
    end
    R1 --> R2 --> R3
```

## 8.3 Voice stack

```mermaid
flowchart LR
    B["Browser<br/>getUserMedia, WebRTC"] <--> L["LiveKit<br/>media server and agents"]
    L --> VAD["Voice activity detection<br/>endpointing"]
    VAD --> STT["STT adapter<br/>streaming"]
    STT --> TS["Transcript sync<br/>sequence ids, partial vs final"]
    TS --> ENG["Conversation engine<br/>same tools and authorization"]
    ENG --> TTS["TTS adapter<br/>streaming, cancellable"]
    TTS --> L
    L -.-> S2S["Option B: speech-to-speech model<br/>behind the same adapter"]
    S2S -.-> ENG
```

## 8.4 Delivery toolchain

```mermaid
flowchart TB
    subgraph B1["Build and verify"]
        direction LR
        A["Commit<br/>trunk-based"] --> B["CI<br/>lint, types, unit"] --> C["Integration<br/>Testcontainers"] --> D["Tenant and authz tests<br/>required"] --> E["Security scans<br/>Semgrep, gitleaks, Trivy"]
    end
    subgraph B2["Ship and operate"]
        direction LR
        F["AI evaluation<br/>release gate"] --> G["Docker image"] --> H["Deploy<br/>Terraform"] --> I["Canary<br/>feature flag"] --> J["Monitor<br/>OpenTelemetry"]
    end
    B1 --> B2
    J -. unhealthy .-> K["Rollback or disable flag"]
```

## 8.5 When each technology arrives

```mermaid
flowchart LR
    subgraph R1["Release 1: text MVP"]
        direction LR
        r1a["TypeScript, NestJS, Postgres with RLS and pgvector"]
        r1b["pg-boss, S3 storage, OIDC, JWT sessions"]
        r1c["React console, Preact widget, WebSocket"]
        r1d["LLM and embedding adapters, Ajv tools"]
        r1e["OpenTelemetry, Sentry, CI with eval gate"]
    end
    subgraph R2["Release 2: voice"]
        direction LR
        r2a["LiveKit and WebRTC"]
        r2b["STT and TTS adapters or speech-to-speech"]
        r2c["Voice activity detection"]
        r2d["Voice metrics and cost dashboard"]
    end
    subgraph R3["Release 3: operations"]
        direction LR
        r3a["Workflow engine: custom or Temporal"]
        r3b["Email and messaging adapters"]
        r3c["Telephony via SIP"]
        r3d["Analytics store if Postgres is outgrown"]
    end
    R1 --> R2 --> R3
```

# E06 — Safe Business Tools

Goal: let the AI invoke a small allowlisted set of operations. Modules: M06, M15. Full pipeline: see `../02-cross-cutting-flows.md` sections 2.5 and 2.6.

## Epic overview

```mermaid
flowchart LR
    E06["E06 Safe tools"] --> US50["US-050 Enable versioned tool for agent"]
    E06 --> US51["US-051 Order status lookup"]
    E06 --> US52["US-052 Timeout and duplicate safety"]
    E06 --> US53["US-053 Audit tool calls"]
    US50 --> US51 --> US52
    US51 --> US53
```

## Three-layer connector architecture

```mermaid
flowchart LR
    AI["AI Engine"] --> TD["Tool definition: orders.lookup v1<br/>schema, risk, permission"]
    TD --> TES["Tool execution service<br/>validate, authorize, idempotency, audit, timeout"]
    TES --> CA["Connector adapter<br/>auth, mapping, error interpretation"]
    CA --> API["Commerce API"]
```

## US-050 — Enable a versioned tool for an agent

Acceptance: tool must be allowlisted and schema-valid.

```mermaid
flowchart TD
    A["Admin selects tool version for agent draft"] --> B{"Tool schema valid JSON Schema, additionalProperties false?"}
    B -- No --> X1["Reject"]
    B -- Yes --> C{"Integration configured and healthy for tenant?"}
    C -- No --> X2["Block: configure integration first"]
    C -- Yes --> D{"Risk level"}
    D -- read_only --> E["Allow"]
    D -- "write" --> F["Require confirmation or approval policy to be set"]
    E & F --> G["Add to agent allowlist in draft"]
    G --> H["Takes effect only after publish of new AgentVersion"]
    H --> I["Audit event"]
```

## US-051 — Customer asks for order status

Acceptance: verification and tenant scope checked; typed minimal result.

```mermaid
sequenceDiagram
    actor C as Customer
    participant AI as AI Engine
    participant TS as Tool service
    participant ID as Customer identity
    participant CN as Commerce connector
    participant EXT as Commerce API

    C->>AI: Where is my order ORDER-123?
    AI->>TS: orders.lookup(order_reference=ORDER-123)
    TS->>TS: validate schema and allowlist
    TS->>ID: verification level of this customer
    alt not verified for order data
        TS-->>AI: VERIFICATION_REQUIRED
        AI-->>C: ask for verification step
    else verified
        TS->>CN: lookup scoped to tenant and customer
        CN->>EXT: GET order
        EXT-->>CN: order payload
        CN-->>TS: status and estimated_delivery only
        TS->>TS: check order belongs to this customer
        TS-->>AI: typed minimal result
        AI-->>C: grounded status answer
    end
```

## US-052 — Handle tool timeout and duplicate requests

Acceptance: idempotency behavior defined; unknown write outcome not blindly retried.

```mermaid
flowchart TD
    A["Tool request with idempotency key"] --> B{"Key already seen?"}
    B -- "Yes, succeeded" --> C["Return stored result: no second call"]
    B -- "Yes, running" --> D["Wait or return in-progress"]
    B -- No --> E["Create ToolExecution"]
    E --> F["Call connector with timeout"]
    F --> G{"Outcome"}
    G -- success --> H["Store result"]
    G -- "timeout, read tool" --> I["Retry with backoff"]
    G -- "timeout, write tool" --> J["Mark UNKNOWN_OUTCOME"]
    J --> K{"Status lookup available?"}
    K -- Yes --> L["Query external system by idempotency key"]
    K -- No --> M["Human review"]
    L --> H
    L --> N["Confirmed failure: safe to retry or tell customer"]
    J --> O["AI must not claim success"]
```

## US-053 — Audit tool calls

Acceptance: actor, tool/version, outcome, timestamp, correlation id with redaction.

```mermaid
flowchart LR
    TE["ToolExecution event"] --> R["Redaction filter<br/>mask PII and secrets per tool policy"]
    R --> AE["AuditEvent<br/>actor, tenant, tool, version, args redacted, outcome, time, correlation id"]
    AE --> DB[("Append-only audit table")]
    DB --> Q["Security reviewer query UI"]
    DB --> EX["Export with retention policy"]
    AE --> M["Metric: tool success and failure rate"]
```

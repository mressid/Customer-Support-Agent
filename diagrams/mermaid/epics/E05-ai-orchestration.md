# E05 — AI Orchestration

Goal: coordinate each conversation turn safely. Modules: M04, M19. Detailed turn pipeline: see `../03-ai-engine.md`.

## Epic overview

```mermaid
flowchart LR
    E05["E05 AI orchestration"] --> US40["US-040 Process turn via versioned agent"]
    E05 --> US41["US-041 Follow-up using context"]
    E05 --> US42["US-042 Handle provider failure"]
    E05 --> US43["US-043 Publish and roll back agent version"]
    US43 --> US40 --> US41
    US40 --> US42
```

## US-040 — Process a turn through a versioned agent configuration

Acceptance: model/config version, latency and outcome recorded.

```mermaid
sequenceDiagram
    participant CV as Conversation
    participant W as Worker
    participant AI as AI Engine
    participant AG as Agent config
    participant LLM as Model adapter
    participant DB as Postgres

    CV->>W: ai.turn.requested
    W->>AI: run turn(conversation, turn id)
    AI->>AG: get active AgentVersion for channel
    AG-->>AI: immutable version: instructions, tools, model config
    AI->>DB: insert AgentExecution status=running
    AI->>LLM: generate with version config
    LLM-->>AI: response, usage, latency
    AI->>DB: update AgentExecution: model, version id, latency, outcome
    AI->>CV: final response and metadata
```

## US-041 — Follow-up question using conversation context

Acceptance: relevant recent context used without exposing another customer's data.

```mermaid
flowchart TD
    A["New customer message"] --> B["Load last N messages of THIS conversation only"]
    B --> C{"Window within token budget?"}
    C -- Yes --> E["Use as is"]
    C -- No --> D["Use stored rolling summary plus last K messages"]
    D --> D2["Refresh summary asynchronously"]
    E --> F["Add structured state: verification level, open ticket, last tool results"]
    D --> F
    F --> G{"Item belongs to same tenant and customer?"}
    G -- No --> X["Drop item and log SecurityEvent"]
    G -- Yes --> H["Final context for model"]
```

## US-042 — Handle model timeout or provider failure

Acceptance: bounded retry/fallback; no false success message delivered.

```mermaid
flowchart TD
    A["Model call"] --> B{"Result"}
    B -- ok --> OK["Continue turn"]
    B -- "timeout or 5xx or rate limit" --> C{"Retries left?"}
    C -- Yes --> D["Backoff with jitter"] --> A
    C -- No --> E{"Fallback model configured?"}
    E -- Yes --> F["Call fallback"] --> B
    E -- No --> G["Circuit breaker records failure"]
    G --> H["Deliver safe message: temporary issue"]
    H --> I{"Policy: route to human?"}
    I -- Yes --> J["Create handoff reason=provider_down"]
    I -- No --> K["Mark turn failed, allow customer retry"]
    B -- "invalid structured output" --> L["Repair or retry once then fallback message"]
```

## US-043 — Publish and roll back an agent version

Acceptance: published versions immutable and audit logged.

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Admin console
    participant AG as Agent config service
    participant EV as Evaluation service
    participant DB as Postgres
    participant AUD as Audit

    Admin->>UI: publish draft
    UI->>AG: publish(draft id)
    AG->>AG: validate tool allowlist and schemas
    AG->>EV: run release gate suite
    EV-->>AG: pass or fail with report
    alt gates pass
        AG->>DB: create immutable AgentVersion n+1
        AG->>AUD: agent.version.published
        AG-->>UI: published
    else gates fail
        AG-->>UI: blocked with failures
    end
    Admin->>UI: rollback
    UI->>AG: activate AgentVersion n
    AG->>DB: move deployment pointer
    AG->>AUD: agent.version.rolled_back
    Note over AG: in-flight turns finish on the version they started with
```

# 03 — AI Conversation Engine Diagrams

Source: `06-ai-conversation-engine.md`. The 12-step turn pipeline is too big for one readable diagram, so it is split into four phases and then recombined as a state machine.

## 3.1 Turn pipeline overview

```mermaid
flowchart LR
    P1["Phase 1<br/>Prepare<br/>steps 1-3"] --> P2["Phase 2<br/>Understand and retrieve<br/>steps 4-5"]
    P2 --> P3["Phase 3<br/>Plan and act<br/>steps 6-8"]
    P3 --> P4["Phase 4<br/>Respond and persist<br/>steps 9-12"]
    P3 -. escalate .-> H["Handoff"]
    P1 -. blocked .-> H
```

### Phase 1 — Prepare (resolve trust, check state, build context)

```mermaid
flowchart TD
    A["ai.turn.requested"] --> B["1 Resolve tenant, conversation, customer identity, active AgentVersion"]
    B --> C{"2 Conversation state"}
    C -- closed --> X1["Reject or reopen per policy"]
    C -- human_owned --> X2["Do not respond: AI paused"]
    C -- rate_limited --> X3["Return throttle message"]
    C -- open --> D["3 Build minimal context"]
    D --> D1["Recent messages"]
    D --> D2["Safe summary"]
    D --> D3["Structured state: verification level, open ticket"]
    D1 & D2 & D3 --> OUT["Context window ready"]
```

### Phase 2 — Understand and retrieve

```mermaid
flowchart TD
    A["Context ready"] --> B["4 Classify intent and risk"]
    B --> C{"Missing information?"}
    C -- Yes --> Q["Plan: ask clarifying question"]
    C -- No --> D{"Risk level"}
    D -- "high risk or policy flag" --> H["Plan: handoff"]
    D -- normal --> E{"Knowledge useful?"}
    E -- No --> OUT["Proceed to Phase 3"]
    E -- Yes --> R["5 Retrieve approved knowledge, tenant filtered"]
    R --> F{"Evidence above threshold?"}
    F -- Yes --> OUT
    F -- No --> G["Mark evidence insufficient"] --> OUT
```

### Phase 3 — Plan and act (tool loop)

```mermaid
flowchart TD
    A["6 Plan next step using only allowed tool registry"] --> B{"Plan type"}
    B -- "direct answer" --> Z["Go to Phase 4"]
    B -- clarify --> Z
    B -- handoff --> H["HandoffPending"]
    B -- "tool call" --> C["7 Validate schema and policy"]
    C -- denied --> D["Record denial, tell planner"] --> A
    C -- allowed --> E["8 Execute authorized tool"]
    E -- success --> F["Validate returned data"] --> A
    E -- "retryable failure" --> G{"Retry budget left?"}
    G -- Yes --> E
    G -- No --> H
    E -- "unknown outcome" --> H
    A -. "loop guard: max steps" .-> H
```

### Phase 4 — Respond and persist

```mermaid
flowchart TD
    A["9 Generate customer reply from verified results and sources"] --> B["10 Output safety and disclosure rules"]
    B --> C{"Passes?"}
    C -- No --> D["Regenerate once or fallback message"] --> B
    C -- Yes --> E["11 Persist in one transaction"]
    E --> E1["Final message"]
    E --> E2["Citations"]
    E --> E3["Tool results and timing"]
    E --> E4["Usage and outcome metadata"]
    E1 & E2 & E3 & E4 --> F["12 Emit events via outbox"]
    F --> G["channel.delivery.requested"]
    F --> H["ai.turn.completed"]
    F --> I["usage.recorded"]
    F --> J["evaluation sampling"]
```

## 3.2 Turn state machine

```mermaid
stateDiagram-v2
    [*] --> Received
    Received --> ContextBuilding
    ContextBuilding --> Deciding
    Deciding --> Retrieving: knowledge needed
    Deciding --> ToolValidation: tool proposed
    Deciding --> Responding: direct response
    Deciding --> HandoffPending: escalate
    Retrieving --> Deciding
    ToolValidation --> ToolRunning: authorized
    ToolValidation --> Responding: invalid or denied
    ToolRunning --> Deciding: result received
    ToolRunning --> Recovery: retryable failure
    Recovery --> ToolRunning: retry budget remains
    Recovery --> HandoffPending: exhausted or policy
    Responding --> Persisting
    Persisting --> DeliveryPending
    DeliveryPending --> Completed
    HandoffPending --> HumanOwned
    HumanOwned --> Completed
    Completed --> [*]
```

## 3.3 Context sections and trust levels

```mermaid
flowchart TB
    subgraph Trusted["Trusted: authored by platform or org"]
        S1["System behaviour and non-negotiable policy"]
        S2["Org-approved agent instructions"]
        S3["Trusted application state"]
        S4["Tool descriptions and JSON schemas"]
        S5["Output format requirements"]
    end
    subgraph Untrusted["Untrusted data: never overrides policy"]
        U1["Customer messages"]
        U2["Retrieved passages with source IDs"]
        U3["Tool results"]
        U4["Uploaded files"]
    end
    Trusted --> PROMPT["Assembled prompt with labelled sections"]
    Untrusted --> PROMPT
    PROMPT --> MODEL["Model call"]
    MODEL --> OUT["Output is untrusted: validate before acting"]
    OUT --> APP["Application code enforces authorization"]
```

## 3.4 Escalation decision tree

```mermaid
flowchart LR
    S["Turn in progress"] --> C
    subgraph C["Escalate if ANY condition holds"]
        direction LR
        a["Customer explicitly asks for a human"]
        b["Policy requires escalation: sensitive topic, VIP, legal"]
        c["Evidence missing or contradictory after clarification"]
        d["Tool failed, retries exhausted or unknown write outcome"]
        e["Repeated misunderstanding count above limit"]
        f["AI or retrieval provider outage"]
    end
    C -- "any holds" --> H["Handoff"]
    C -- "none holds" --> OK["AI continues"]
    H --> R["Record reason code for metrics: escalation rate by reason"]
```

## 3.5 Response policy decision

```mermaid
flowchart TD
    A["Candidate answer"] --> B{"Relies on order, account or action data?"}
    B -- Yes --> C{"Tool confirmed the data or action?"}
    C -- No --> X1["Do not state it as fact"]
    C -- Yes --> D["State with tool-sourced wording"]
    B -- No --> E{"Relies on policy or FAQ?"}
    E -- Yes --> F{"Retrieved source supports it?"}
    F -- No --> X2["Say not sure and offer human"]
    F -- Yes --> G["Answer with citation"]
    E -- No --> H["General conversational reply"]
    D & G & H --> I["Concise, understandable wording, requested language"]
```

## 3.6 Model-provider adapter

```mermaid
flowchart LR
    ENG["AI Engine core domain"] --> IF["ModelProvider interface<br/>generate_response, stream_response,<br/>classify, embed, open_realtime_session"]
    IF --> A1["Adapter: Provider A"]
    IF --> A2["Adapter: Provider B"]
    IF --> A3["Adapter: Local or test stub"]
    A1 --> V1["Vendor API"]
    A2 --> V2["Vendor API"]
    IF -. records .-> M["model name and version, latency, usage, errors, no secrets"]
```

## 3.7 Agent version lifecycle (publish, rollback)

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Draft: edit instructions, tools, knowledge, channels
    Draft --> Validating: request publish
    Validating --> Draft: validation fails
    Validating --> Evaluating: schemas and allowlist OK
    Evaluating --> Draft: safety or regression gate fails
    Evaluating --> Published: gates pass, immutable version
    Published --> Deployed: AgentDeployment to channel
    Deployed --> Superseded: newer version deployed
    Deployed --> RolledBack: rollback to previous version
    RolledBack --> Deployed: previous version reactivated
    Superseded --> [*]
```

## 3.8 Failure handling inside a turn

```mermaid
sequenceDiagram
    participant C as Conversation
    participant AI as AI Engine
    participant LLM as Model adapter
    participant H as Human Inbox

    C->>AI: new turn
    AI->>LLM: generate with timeout
    alt success
        LLM-->>AI: response
    else timeout or 5xx
        AI->>LLM: bounded retry with backoff
        alt retry succeeds
            LLM-->>AI: response
        else fallback model configured
            AI->>LLM: fallback model
            LLM-->>AI: response
        else all failed
            AI->>C: safe unavailability message, never false success
            AI->>H: optional handoff with reason provider_down
        end
    end
    AI->>C: persist outcome and failure metrics
```

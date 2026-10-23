# E10 — Workflow, Routing and SLA

Goal: automate repeatable support operations. Modules: M12, M13, M14.

## Epic overview

```mermaid
flowchart LR
    E10["E10 Workflow, routing, SLA"] --> US90["US-090 Define workflow trigger and steps"]
    E10 --> US91["US-091 Routing rules and SLA targets"]
    E10 --> US92["US-092 Safe step retry"]
    US90 --> US92
    US91 --> US90
```

## Principle: deterministic procedure, AI proposes

```mermaid
flowchart LR
    AI["AI classifies or proposes"] --> WF["Workflow engine enforces the procedure"]
    WF --> S1["Step: validate"] --> S2["Step: approval if needed"] --> S3["Step: execute tool"] --> S4["Step: notify"]
```

## US-090 — Define workflow trigger and steps

Acceptance: workflow version, run state and failures visible.

### Authoring and versioning

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Validated: schema, step refs, permissions OK
    Validated --> Published: immutable WorkflowVersion
    Published --> Active: enabled for tenant
    Active --> Paused
    Paused --> Active
    Active --> Retired: new version replaces
    Retired --> [*]
```

### Run execution

```mermaid
flowchart TD
    EV["Trigger event, e.g. ticket.created"] --> M{"Conditions match?"}
    M -- No --> END1["No run"]
    M -- Yes --> R["Create WorkflowRun pinned to version"]
    R --> S["Execute step N"]
    S --> O{"Result"}
    O -- success --> NX{"More steps?"}
    NX -- Yes --> S
    NX -- No --> DONE["Run succeeded"]
    O -- "wait: approval or timer" --> WT["Suspend, persist state"] --> S
    O -- "failure" --> RT["Go to US-092 retry logic"]
```

## US-091 — Routing rules and SLA targets

Acceptance: rule priority and fallback behavior are deterministic.

```mermaid
flowchart TD
    A["Handoff or ticket needs a queue"] --> B["Load rules ordered by priority, then id"]
    B --> C{"Rule 1 matches? channel, topic, language, tier"}
    C -- Yes --> Q["Select queue of rule 1"]
    C -- No --> D{"Rule 2 matches?"}
    D -- Yes --> Q2["Select queue of rule 2"]
    D -- No --> E{"More rules?"}
    E -- Yes --> D
    E -- No --> F["Fallback default queue"]
    Q & Q2 & F --> G{"Within business hours schedule?"}
    G -- Yes --> H["Start SLA clock with response and resolution targets"]
    G -- No --> I["Queue, clock starts at next open time"]
```

### SLA timers

```mermaid
stateDiagram-v2
    [*] --> Running
    Running --> Paused: waiting on customer or outside hours
    Paused --> Running
    Running --> AtRisk: 80 percent of target elapsed
    AtRisk --> Breached: target exceeded
    AtRisk --> Met: first response or resolution
    Running --> Met
    Breached --> EscalationPolicy: notify lead, reassign
    Met --> [*]
    EscalationPolicy --> [*]
```

## US-092 — Retry a failed workflow step safely

Acceptance: retry policy bounded; idempotency defined per step.

```mermaid
flowchart TD
    F["Step failed"] --> A{"Step declares idempotent or has idempotency key?"}
    A -- No --> H["Pause run and ask human"]
    A -- Yes --> B{"Error retryable?"}
    B -- No --> X["Mark step failed, run failed, notify"]
    B -- Yes --> C{"Attempts below max?"}
    C -- No --> D["Dead-letter, mark run needs_review"]
    C -- Yes --> E["Wait backoff with jitter"]
    E --> G["Re-run step with same idempotency key"]
    G --> R{"Outcome"}
    R -- success --> N["Continue workflow"]
    R -- failure --> F
    D --> COMP["Compensation steps if defined"]
```

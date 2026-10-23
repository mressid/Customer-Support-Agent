# E11 — Integrations and Additional Channels

Goal: add provider connectors without contaminating core domain logic. Modules: M02, M15.

## Epic overview

```mermaid
flowchart LR
    E11["E11 Integrations and channels"] --> US100["US-100 Configure integration securely"]
    E11 --> US101["US-101 Normalize provider webhook"]
    E11 --> US102["US-102 Continue on a second channel"]
    US100 --> US101 --> US102
```

## Adapter boundary

```mermaid
flowchart LR
    P1["Provider A payload"] --> A1["Adapter A"]
    P2["Provider B payload"] --> A2["Adapter B"]
    A1 --> CAN["Canonical internal contract"]
    A2 --> CAN
    CAN --> CORE["Core domain: no provider types"]
    CORE --> CAN2["Canonical outbound command"]
    CAN2 --> A1
    CAN2 --> A2
```

## US-100 — Configure an integration securely

Acceptance: credentials are secret references; test status and health visible.

```mermaid
sequenceDiagram
    actor Admin
    participant UI
    participant API
    participant SM as Secret manager
    participant IH as Integration hub
    participant EXT as External system

    Admin->>UI: choose connector, enter credentials
    UI->>API: submit
    API->>SM: store secret, get ref
    API->>IH: create Integration with secret_ref only
    Admin->>UI: test connection
    UI->>API: test
    API->>IH: run health check
    IH->>SM: resolve ref in memory
    IH->>EXT: lightweight authenticated call
    EXT-->>IH: ok or error
    IH-->>UI: status healthy or failing with safe message
    Note over IH: scheduled health checks update status and rate-limit counters
```

### Integration health states

```mermaid
stateDiagram-v2
    [*] --> Unconfigured
    Unconfigured --> Configured: secret saved
    Configured --> Healthy: test OK
    Configured --> Failing: test failed
    Healthy --> Degraded: errors or rate limited
    Degraded --> Healthy
    Degraded --> Failing: circuit open
    Failing --> Healthy: recovered
    Healthy --> Disabled: admin disables
    Disabled --> Configured
```

## US-101 — Normalize provider webhook into canonical event

Acceptance: signature verified; replay deduplicated; processing observable.

```mermaid
flowchart TD
    W["Webhook"] --> V["Verify signature and timestamp window"]
    V -- fail --> R["Reject and SecurityEvent"]
    V -- ok --> D["Dedupe on provider_event_id"]
    D -- seen --> S["200, no reprocess"]
    D -- new --> P["Persist raw minimal payload with retention"]
    P --> N["Adapter maps to canonical envelope"]
    N --> VAL{"Valid against schema?"}
    VAL -- No --> DL["Dead-letter with reason"]
    VAL -- Yes --> PUB["Publish canonical event"]
    PUB --> OBS["Metrics: accepted, duplicate, failed, latency"]
```

## US-102 — Continue support through a second channel

Acceptance: identity linking follows verification policy; duplicate conversations avoided where possible.

```mermaid
flowchart TD
    A["Message on channel B from identity X"] --> B{"ChannelIdentity X known?"}
    B -- Yes --> C["Resolve existing Customer"]
    B -- No --> D{"Identity can be linked by verified proof? OTP, signed-in link"}
    D -- Yes --> E["Link CustomerIdentity to existing Customer, record consent"]
    D -- No --> F["Create separate customer, no access to protected data"]
    E --> C
    C --> G{"Open conversation within policy window?"}
    G -- Yes --> H["Attach channel B to existing conversation"]
    G -- No --> I["Start new conversation, optionally link to previous summary"]
    F --> I
    Note1["Phone number or email alone is not proof of account ownership"] -.-> D
```

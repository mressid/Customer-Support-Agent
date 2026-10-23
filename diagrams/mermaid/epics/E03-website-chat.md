# E03 — Website Chat Channel

Goal: first customer-facing channel. Modules: M02, M03.

## Epic overview

```mermaid
flowchart LR
    E03["E03 Website chat"] --> US20["US-020 Configure widget"]
    E03 --> US21["US-021 Open chat and get session"]
    E03 --> US22["US-022 Reconnect and resume"]
    US20 --> US21 --> US22
```

## US-020 — Administrator configures the website widget

Acceptance: widget associated with correct organization and agent configuration.

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Admin console
    participant API as Support API
    participant CH as Channel service
    participant AG as Agent config service
    participant DB as Postgres

    Admin->>UI: create website channel
    UI->>API: name, allowed origins, theme
    API->>CH: create ChannelConnection for tenant
    CH->>DB: save connection with generated public key
    Admin->>UI: select published agent version
    UI->>API: bind agent
    API->>AG: create AgentDeployment (connection, version)
    AG->>DB: save deployment
    API-->>UI: embed snippet with public key
    Note over API: audit event channel.configured
```

## US-021 — Visitor opens chat and receives a session

Acceptance: session token is scoped, expires, cannot access other tenants.

```mermaid
sequenceDiagram
    actor V as Visitor
    participant W as Widget in browser
    participant API as Support API
    participant S as Session service

    V->>W: page loads, opens chat
    W->>API: POST /sessions with public key, Origin header
    API->>API: verify origin is in allow list, rate limit by IP
    API->>S: issue session
    S->>S: sign token with tenant, connection, conversation, expiry
    S-->>API: token
    API-->>W: short-lived token
    Note over W,API: every later call is authorized from token claims only
```

### Token claim checks

```mermaid
flowchart TD
    A["API request with token"] --> B{"Signature valid?"}
    B -- No --> X["401"]
    B -- Yes --> C{"Expired?"}
    C -- Yes --> Y["401: client must reconnect"]
    C -- No --> D{"Requested conversation matches claim?"}
    D -- No --> Z["403: cross-conversation or cross-tenant"]
    D -- Yes --> E["Proceed with tenant from claim"]
```

## US-022 — Reconnect after temporary network failure

Acceptance: existing conversation can be resumed under valid session policy.

```mermaid
stateDiagram-v2
    [*] --> Connected
    Connected --> Disconnected: network loss
    Disconnected --> Reconnecting: backoff timer
    Reconnecting --> Connected: token valid, resume
    Reconnecting --> Refreshing: token expired but within resume window
    Refreshing --> Connected: new token for same conversation
    Reconnecting --> Disconnected: still offline
    Refreshing --> NewConversation: resume window expired
    NewConversation --> Connected
```

```mermaid
sequenceDiagram
    participant W as Widget
    participant API as Support API
    participant CV as Conversation service

    W->>API: resume with token and last_seen_sequence
    API->>CV: messages after sequence N
    CV-->>API: missed messages including assistant replies
    API-->>W: replay in order
    W->>W: dedupe by message id, resend unsent with same client_message_id
```

# E01 — Tenant and Access Foundation

Goal: establish secure organization boundaries. Modules: M18, M20.

## Epic overview

```mermaid
flowchart LR
    E01["E01 Tenant and access"] --> US1["US-001 Create organization"]
    E01 --> US2["US-002 Invite users and roles"]
    E01 --> US3["US-003 Tenant isolation tests"]
    US1 --> OUT1["Tenant context available to every module"]
    US2 --> OUT2["Server-side RBAC"]
    US3 --> OUT3["CI gate: no cross-tenant access"]
    OUT1 --> NEXT["Unblocks E02, E04"]
```

## US-001 — Create and configure an organization

Acceptance: ID generated, default settings exist, audit event recorded.

```mermaid
sequenceDiagram
    actor Admin
    participant API as Support API
    participant ORG as Organization service
    participant DB as Postgres
    participant AUD as Audit

    Admin->>API: POST /organizations
    API->>API: authenticate and validate input
    API->>ORG: create(name, settings)
    ORG->>DB: BEGIN
    ORG->>DB: insert organization with generated id
    ORG->>DB: insert default settings and default roles
    ORG->>DB: insert admin membership
    ORG->>DB: insert audit event organization.created
    ORG->>DB: COMMIT
    ORG-->>API: organization
    API-->>Admin: 201 with organization id
```

## US-002 — Invite users and assign roles

Acceptance: invitation expires, role validated server-side, revoked users lose access.

### Invitation lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Sent: email dispatched
    Sent --> Accepted: valid token before expiry
    Sent --> Expired: expires_at passed
    Sent --> Revoked: admin cancels
    Accepted --> [*]
    Expired --> [*]
    Revoked --> [*]
```

### Role assignment and revocation

```mermaid
flowchart TD
    A["Admin invites user with role"] --> B{"Caller has users.invite permission?"}
    B -- No --> X["403"]
    B -- Yes --> C{"Role exists in this organization?"}
    C -- No --> Y["422 invalid role"]
    C -- Yes --> D["Create invitation with expiry and single-use token"]
    D --> E["User accepts"] --> F["Create Membership: user, org, role"]
    F --> G["Session carries org and role claims, re-checked on every request"]
    H["Admin revokes membership"] --> I["Mark membership revoked, invalidate sessions and tokens"]
    I --> J["Next request: permission check fails, access lost"]
    I --> K["Audit event membership.revoked"]
```

## US-003 — Test tenant isolation

Acceptance: cross-tenant read and write attempts are denied in automated tests.

```mermaid
flowchart TD
    S["CI test suite: tenant isolation"] --> F["Fixture: tenant A and tenant B with data"]
    F --> L["Authenticate as tenant A"]
    L --> T1["Read B conversation by id"]
    L --> T2["Write message into B conversation"]
    L --> T3["Search vector index: B documents"]
    L --> T4["Fetch B object storage key"]
    L --> T5["Read B cache key"]
    L --> T6["Enqueue or consume B job"]
    L --> T7["Query B analytics"]
    L --> T8["Spoof tenant_id in payload"]
    T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 --> A{"All denied or empty?"}
    A -- Yes --> P["Pass"]
    A -- No --> FAIL["Fail build: SecurityEvent"]
```

### Where tenant filtering is enforced

```mermaid
flowchart LR
    REQ["Request"] --> MW["Tenant context middleware"]
    MW --> REPO["Tenant-aware repository base class"]
    REPO --> DBQ["SQL WHERE organization_id or RLS policy"]
    MW --> VS["Vector filter"]
    MW --> OS["Object prefix"]
    MW --> CK["Cache key prefix"]
    DBQ -. "missing filter?" .-> LINT["Static check and test failure"]
```

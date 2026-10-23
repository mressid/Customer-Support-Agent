# U4 — UML Activity Diagrams (with swimlanes)

Mermaid has no activity-diagram syntax, so these use flowcharts: initial node `((start))`, final node `(((end)))`, decision diamonds, and one subgraph per swimlane (partition).

## U4.1 Customer support conversation — end to end

```mermaid
flowchart TB
    start((Start)) --> a1
    subgraph Customer
        a1["Open chat"]
        a2["Send message"]
        a9["Read reply"]
    end
    subgraph Platform
        b1["Create session and conversation"]
        b2["Persist message"]
        b3["Request AI turn"]
        b8["Deliver reply"]
    end
    subgraph AI_Engine["AI Engine"]
        c1["Build context"]
        c2{"Need knowledge?"}
        c3["Retrieve passages"]
        c4{"Need live data?"}
        c5["Execute authorized tool"]
        c6{"Can answer safely?"}
        c7["Compose grounded reply"]
    end
    subgraph Human["Human support"]
        h1["Claim from queue"]
        h2["Resolve with customer"]
    end
    a1 --> b1 --> a2 --> b2 --> b3 --> c1 --> c2
    c2 -- yes --> c3 --> c4
    c2 -- no --> c4
    c4 -- yes --> c5 --> c6
    c4 -- no --> c6
    c6 -- yes --> c7 --> b8 --> a9
    c6 -- no --> h1 --> h2 --> fin
    a9 --> d{"Resolved?"}
    d -- no --> a2
    d -- yes --> fin(((End)))
```

## U4.2 Document ingestion

```mermaid
flowchart TB
    s((Start)) --> u1
    subgraph Administrator
        u1["Select file and register source"]
        u9["Review status"]
    end
    subgraph API
        p1{"Size and type OK?"}
        p2["Sniff content and scan"]
        p3{"Clean?"}
        p4["Store object, create version"]
        p5["Enqueue ingestion"]
    end
    subgraph Worker
        w1["Parse"]
        w2["Chunk"]
        w3["Embed"]
        w4["Index with tenant metadata"]
        w5{"Success?"}
        w6["Backoff and retry"]
        w7["Mark failed"]
        w8["Activate version"]
    end
    u1 --> p1
    p1 -- no --> rej["Reject"] --> u9
    p1 -- yes --> p2 --> p3
    p3 -- no --> q["Quarantine and audit"] --> u9
    p3 -- yes --> p4 --> p5 --> w1 --> w2 --> w3 --> w4 --> w5
    w5 -- yes --> w8 --> u9
    w5 -- no --> w6
    w6 -- attempts left --> w1
    w6 -- exhausted --> w7 --> u9
    u9 --> e(((End)))
```

## U4.3 Human handoff

```mermaid
flowchart TB
    s((Start)) --> t1
    subgraph Trigger
        t1{"Handoff trigger"}
    end
    subgraph AI_Engine["AI Engine"]
        a1["Pause AI replies"]
        a2["Build bundle and summary"]
        a3["Tell customer status"]
    end
    subgraph Routing
        r1["Select queue by rules"]
        r2{"Business hours?"}
        r3["Start SLA clock"]
        r4["Offer ticket or callback"]
    end
    subgraph Agent
        g1["Claim item"]
        g2{"Claim succeeded?"}
        g3["Read bundle"]
        g4["Converse and act"]
        g5{"Return to AI?"}
        g6["Release to AI"]
        g7["Resolve"]
    end
    t1 -- "customer request, policy, tool failure, low confidence" --> a1 --> a2 --> a3 --> r1 --> r2
    r2 -- yes --> r3 --> g1 --> g2
    r2 -- no --> r4 --> e(((End)))
    g2 -- no --> g1
    g2 -- yes --> g3 --> g4 --> g5
    g5 -- yes --> g6 --> e
    g5 -- no --> g7 --> e
```

## U4.4 Tool call authorization

```mermaid
flowchart TB
    s((Start)) --> a
    subgraph AI_Engine["AI Engine"]
        a["Propose tool call"]
        z["Use typed result or denial"]
    end
    subgraph Tool_Service["Tool Service"]
        b{"Allowlisted?"}
        c{"Schema valid?"}
        d{"Customer verified and tenant scope OK?"}
        e{"Risk level"}
        f["Create execution record"]
        g["Call connector with timeout"]
        h{"Outcome"}
        i["Redact and store result"]
        j["Mark unknown outcome"]
    end
    subgraph Approval
        k["Wait for human approval"]
        l{"Approved?"}
    end
    a --> b
    b -- no --> deny["Denied"] --> z
    b -- yes --> c
    c -- no --> deny
    c -- yes --> d
    d -- no --> deny
    d -- yes --> e
    e -- "read only" --> f
    e -- "sensitive write" --> k --> l
    l -- no --> deny
    l -- yes --> f
    f --> g --> h
    h -- success --> i --> z
    h -- "write timeout" --> j --> z
    h -- "failure" --> z
    z --> fin(((End)))
```

## U4.5 Release process

```mermaid
flowchart TB
    s((Start)) --> d1
    subgraph Developers
        d1["Implement story to Definition of Done"]
        d2["Merge small change"]
    end
    subgraph CI
        c1["Unit and integration tests"]
        c2["Tenant and authorization tests"]
        c3["AI regression and safety evaluation"]
        c4["Latency, cost and failure-path checks"]
        c5{"All gates pass?"}
    end
    subgraph Release
        r1["Create versioned release"]
        r2["Deploy behind feature flag"]
        r3["Canary rollout"]
        r4{"Healthy?"}
        r5["Roll back or disable"]
        r6["Full rollout"]
    end
    d1 --> d2 --> c1 --> c2 --> c3 --> c4 --> c5
    c5 -- no --> d1
    c5 -- yes --> r1 --> r2 --> r3 --> r4
    r4 -- yes --> r6 --> e(((End)))
    r4 -- no --> r5 --> d1
```

## U4.6 Incident response for provider outage

```mermaid
flowchart TB
    s((Start)) --> m1
    subgraph Monitoring
        m1["Alert: error rate or latency breach"]
    end
    subgraph Operator
        o1["Acknowledge and open incident"]
        o2{"Provider or internal?"}
        o3["Enable fallback model or degrade"]
        o4["Fix or roll back release"]
        o5["Close incident"]
    end
    subgraph Platform
        p1["Circuit breaker opens"]
        p2["Customers get safe message or human handoff"]
        p3["Queue retries with backoff"]
    end
    subgraph Team
        t1["Blameless review"]
        t2["Add regression case and runbook update"]
    end
    m1 --> o1 --> o2
    o2 -- provider --> p1 --> p2 --> o3 --> p3 --> o5
    o2 -- internal --> o4 --> o5
    o5 --> t1 --> t2 --> e(((End)))
```

# U1 — UML Use Case Diagrams

Mermaid has no native use-case notation, so actors are drawn as stadium nodes outside a system-boundary subgraph and use cases as ellipses. `include` and `extend` relations are dotted arrows with stereotypes. Actors come from `01-product-vision.md`; use cases from the epics.

## U1.1 System-level use cases

```mermaid
flowchart LR
    Customer(["Customer"])
    Agent(["Support Agent"])
    Lead(["Support Lead"])
    Admin(["Org Administrator"])
    Operator(["Platform Operator"])
    Provider(["External Provider<br/>LLM, Speech, Business API"])

    subgraph SYS["AI Customer Support Platform"]
        direction TB
        UC1(["Ask a question"])
        UC2(["Request order status"])
        UC3(["Request a human"])
        UC4(["Talk by voice"])
        UC5(["Take over conversation"])
        UC6(["Manage tickets"])
        UC7(["Configure agent and channels"])
        UC8(["Manage knowledge sources"])
        UC9(["Manage users and roles"])
        UC10(["Review reports and SLAs"])
        UC11(["Monitor health, cost, abuse"])
        UC12(["Authenticate customer"])
    end

    Customer --- UC1
    Customer --- UC2
    Customer --- UC3
    Customer --- UC4
    Agent --- UC5
    Agent --- UC6
    Lead --- UC6
    Lead --- UC10
    Admin --- UC7
    Admin --- UC8
    Admin --- UC9
    Operator --- UC11
    UC2 -. include .-> UC12
    UC3 -. extend .-> UC1
    UC4 -. extend .-> UC1
    UC5 -. include .-> UC6
    UC1 --- Provider
    UC2 --- Provider
```

## U1.2 Customer use cases

```mermaid
flowchart LR
    C(["Customer"])
    subgraph B["Customer-facing boundary"]
        A1(["Open chat session"])
        A2(["Send text message"])
        A3(["Receive grounded answer"])
        A4(["Look up order status"])
        A5(["Verify identity"])
        A6(["Request human agent"])
        A7(["Start voice session"])
        A8(["Interrupt assistant"])
        A9(["Switch text and voice"])
        A10(["Rate conversation"])
        A11(["Resume after disconnect"])
        A12(["Request data access or deletion"])
    end
    C --- A1
    C --- A2
    C --- A4
    C --- A6
    C --- A7
    C --- A10
    C --- A12
    A2 -. include .-> A1
    A3 -. extend .-> A2
    A4 -. include .-> A5
    A8 -. extend .-> A7
    A9 -. extend .-> A7
    A11 -. extend .-> A1
```

## U1.3 Support staff use cases

```mermaid
flowchart LR
    AG(["Support Agent"])
    LD(["Support Lead"])
    subgraph B["Support console boundary"]
        S1(["View queue"])
        S2(["Claim conversation"])
        S3(["Read handoff summary"])
        S4(["Reply to customer"])
        S5(["Add internal note"])
        S6(["Return to AI"])
        S7(["Resolve conversation"])
        S8(["Create ticket"])
        S9(["Filter tickets"])
        S10(["Define routing and SLA"])
        S11(["Review quality and metrics"])
        S12(["Approve sensitive action"])
    end
    AG --- S1
    AG --- S2
    AG --- S4
    AG --- S5
    AG --- S6
    AG --- S7
    AG --- S8
    AG --- S12
    LD --- S9
    LD --- S10
    LD --- S11
    LD --- S12
    S2 -. include .-> S3
    S4 -. extend .-> S2
    S7 -. extend .-> S2
    S8 -. extend .-> S7
```

## U1.4 Administration and governance use cases

```mermaid
flowchart LR
    AD(["Org Administrator"])
    OP(["Platform Operator"])
    RV(["Security Reviewer"])
    subgraph B["Admin and governance boundary"]
        G1(["Create organization"])
        G2(["Invite user and assign role"])
        G3(["Configure website widget"])
        G4(["Upload knowledge source"])
        G5(["Configure integration"])
        G6(["Enable tool for agent"])
        G7(["Publish agent version"])
        G8(["Roll back agent version"])
        G9(["Run evaluation"])
        G10(["Inspect usage"])
        G11(["Trace a request"])
        G12(["Audit tool calls"])
        G13(["Set retention policy"])
    end
    AD --- G1
    AD --- G2
    AD --- G3
    AD --- G4
    AD --- G5
    AD --- G6
    AD --- G7
    AD --- G8
    AD --- G10
    AD --- G13
    OP --- G11
    OP --- G10
    RV --- G12
    G7 -. include .-> G9
    G6 -. include .-> G5
    G8 -. extend .-> G7
```

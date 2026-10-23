# U5 — UML Structural Diagrams: Component, Package, Deployment, Object

## U5.1 Component diagram: provided and required interfaces

Lollipop notation is approximated: `-->|provides|` shows an exposed interface and `-.->|requires|` a dependency on one.

```mermaid
flowchart LR
    subgraph Core["Modular monolith"]
        CH["Channel component"]
        CV["Conversation component"]
        AI["AI Engine component"]
        KB["Knowledge component"]
        TL["Tool component"]
        HI["Human Inbox component"]
        TK["Ticket component"]
        AG["Agent config component"]
        AC["Access component"]
    end
    ICV(("IConversation"))
    IAI(("IAiTurn"))
    IKB(("IRetrieval"))
    ITL(("IToolExecution"))
    IHI(("IHandoff"))
    IAUTH(("IAuthorization"))
    CV -->|provides| ICV
    AI -->|provides| IAI
    KB -->|provides| IKB
    TL -->|provides| ITL
    HI -->|provides| IHI
    AC -->|provides| IAUTH
    CH -.->|requires| ICV
    CV -.->|requires| IAI
    AI -.->|requires| IKB
    AI -.->|requires| ITL
    AI -.->|requires| IHI
    HI -.->|requires| ICV
    HI -.->|requires| TK
    AI -.->|requires| AG
    CH -.->|requires| IAUTH
    TL -.->|requires| IAUTH
```

## U5.1b Component diagram: outbound ports and adapters

```mermaid
flowchart LR
    AI["AI Engine"] -.-> PLLM["ModelProvider port"]
    AI -.-> PSP["SpeechProvider port"]
    TL["Tool component"] -.-> PCN["Connector port"]
    TL -.-> PSM["SecretManager port"]
    KB["Knowledge component"] -.-> PVS["VectorIndex port"]
    CV["Conversation component"] -.-> PQ["Queue port"]
    PLLM --> A1["LLM adapters"]
    PSP --> A2["Speech adapters"]
    PCN --> A3["Business connectors"]
    PSM --> A4["Secret manager adapter"]
    PVS --> A5["Vector store adapter"]
    PQ --> A6["Queue adapter"]
```

## U5.2 Package diagram (code organization and allowed dependencies)

```mermaid
classDiagram
    namespace api {
        class HttpControllers
        class WebhookEndpoints
        class AuthMiddleware
    }
    namespace modules_conversation {
        class ConversationApp
        class ChannelApp
        class CustomerApp
    }
    namespace modules_ai {
        class EngineApp
        class KnowledgeApp
        class ToolsApp
        class VoiceApp
    }
    namespace modules_ops {
        class InboxApp
        class TicketApp
        class WorkflowApp
    }
    namespace modules_platform {
        class AccessApp
        class AgentConfigApp
        class AuditApp
    }
    namespace infrastructure {
        class SqlRepositories
        class ObjectStorageAdapter
        class VectorAdapter
        class QueueAdapter
        class LlmAdapters
        class SpeechAdapters
        class ConnectorAdapters
    }
    HttpControllers ..> ConversationApp
    WebhookEndpoints ..> ChannelApp
    AuthMiddleware ..> AccessApp
    ConversationApp ..> EngineApp : via interface
    EngineApp ..> KnowledgeApp
    EngineApp ..> ToolsApp
    EngineApp ..> InboxApp
    InboxApp ..> TicketApp
    WorkflowApp ..> TicketApp
    EngineApp ..> AgentConfigApp
    EngineApp ..> LlmAdapters
    VoiceApp ..> SpeechAdapters
    KnowledgeApp ..> VectorAdapter
    ToolsApp ..> ConnectorAdapters
    ConversationApp ..> SqlRepositories
    ConversationApp ..> QueueAdapter
    KnowledgeApp ..> ObjectStorageAdapter
    ConversationApp ..> AuditApp
```

## U5.3 Deployment diagram — MVP

```mermaid
flowchart TB
    subgraph Browser["Customer browser"]
        WG["support-web-widget"]
    end
    subgraph Staff["Staff browser"]
        CON["support-agent-console"]
    end
    subgraph Edge["Edge node"]
        GW["API gateway and rate limiting"]
    end
    subgraph AppNode["Application node (container)"]
        API["support-api"]
        WRK["support-worker"]
    end
    subgraph DataNode["Data services"]
        PG[("postgres")]
        OS[("object storage")]
        VS[("vector search")]
        QU[["queue"]]
        SM{{"secret manager"}}
    end
    subgraph Ext["External providers"]
        LLM["LLM API"]
        SPC["Speech API"]
        BIZ["Business APIs"]
    end
    subgraph Obs["Observability stack"]
        TEL["logs, metrics, traces, alerts"]
    end
    WG -- HTTPS WSS --> GW
    CON -- HTTPS --> GW
    GW --> API
    API --> PG
    API --> QU
    QU --> WRK
    WRK --> PG
    WRK --> OS
    WRK --> VS
    API --> VS
    API --> OS
    API --> SM
    WRK --> SM
    API -- HTTPS --> LLM
    WRK -- HTTPS --> LLM
    API -- HTTPS --> BIZ
    API -- WebRTC or WSS --> SPC
    API -.-> TEL
    WRK -.-> TEL
```

## U5.4 Deployment diagram — later: independent real-time voice component

```mermaid
flowchart LR
    W["Widget"] -- WebRTC --> VG["voice-gateway<br/>independently scaled"]
    VG -- internal gRPC or events --> API["support-api"]
    VG --> SPC["Speech provider"]
    API --> PG[("postgres")]
    API --> QU[["queue"]]
    QU --> WRK["support-worker"]
    note1["Extract only if independent scaling or fault isolation justifies cost"] -.-> VG
```

## U5.5 Object diagram — one live conversation (instance specification)

```mermaid
classDiagram
    class org1["org1 : Organization"] {
        id = 0192-A
        name = Acme Store
    }
    class cust1["cust1 : Customer"] {
        verificationLevel = verified
    }
    class conv1["conv1 : Conversation"] {
        status = AiHandling
        owner = AI
    }
    class m1["m1 : Message"] {
        sequence = 1
        kind = text
        direction = inbound
        body = Where is my order?
    }
    class m2["m2 : Message"] {
        sequence = 2
        direction = outbound
        body = Your order ORDER-123 ships tomorrow
    }
    class exec1["exec1 : AgentExecution"] {
        outcome = answered
        latencyMs = 2100
    }
    class te1["te1 : ToolExecution"] {
        tool = orders.lookup v1
        status = succeeded
    }
    class av1["av1 : AgentVersion"] {
        number = 7
        immutable = true
    }
    org1 --> cust1
    cust1 --> conv1
    conv1 --> m1
    conv1 --> m2
    m2 --> exec1 : producedBy
    exec1 --> av1 : runsOn
    exec1 --> te1 : invoked
```

## U5.6 Composite structure — tool execution internals

```mermaid
flowchart LR
    subgraph TES["ToolExecutionService (composite structure)"]
        direction LR
        IN(["port: invoke"])
        V["Validator"]
        AZ["Authorizer"]
        ID["IdempotencyGuard"]
        EX["Executor"]
        RD["Redactor"]
        AU["Auditor"]
        OUT(["port: result"])
        CN(["port: connector"])
    end
    IN --> V --> AZ --> ID --> EX
    EX --> CN
    CN --> EX
    EX --> RD --> OUT
    EX --> AU
    AZ --> AU
```

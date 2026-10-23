# E04 — Knowledge Ingestion and RAG

Goal: ground answers in organization-approved sources. Module: M05.

## Epic overview

```mermaid
flowchart LR
    E04["E04 Knowledge and RAG"] --> US30["US-030 Register and upload source"]
    E04 --> US31["US-031 Parse, chunk, embed, index"]
    E04 --> US32["US-032 Retrieve relevant chunks"]
    E04 --> US33["US-033 Grounded answer or fallback"]
    US30 --> US31 --> US32 --> US33
```

## US-030 — Register and upload a knowledge source

Acceptance: file limits and type checks enforced; ingestion state visible.

```mermaid
flowchart TD
    A["Admin uploads file"] --> B{"Size within limit?"}
    B -- No --> X1["Reject 413"]
    B -- Yes --> C{"Declared type allowed?"}
    C -- No --> X2["Reject 415"]
    C -- Yes --> D["Sniff real content type"]
    D --> E{"Matches declared type?"}
    E -- No --> X3["Reject"]
    E -- Yes --> F["Malware scan where feasible"]
    F --> G{"Clean?"}
    G -- No --> X4["Quarantine and audit"]
    G -- Yes --> H["Store in private object storage under tenant prefix"]
    H --> I["Create KnowledgeSource, Document, DocumentVersion state=uploaded"]
    I --> J["Emit knowledge.source.ingestion.requested"]
    J --> K["UI shows status"]
```

## US-031 — Parse, chunk, embed and index asynchronously

Acceptance: failed ingestion can be retried; document version traceable.

### Pipeline

```mermaid
flowchart LR
    Q["Job: ingestion.requested"] --> P["Parse by type"]
    P --> C["Clean and normalize"]
    C --> K["Chunk with overlap, keep section metadata"]
    K --> E["Embed via model adapter in batches"]
    E --> I["Upsert into vector index with tenant, source, version metadata"]
    I --> A["Activate DocumentVersion, deactivate previous"]
    A --> D["Emit ingestion.completed"]
```

### Ingestion state machine

```mermaid
stateDiagram-v2
    [*] --> Uploaded
    Uploaded --> Parsing
    Parsing --> Chunking
    Parsing --> Failed: unreadable
    Chunking --> Embedding
    Embedding --> Indexing
    Embedding --> RetryWait: provider error
    RetryWait --> Embedding: backoff
    Indexing --> Active: swap complete
    Indexing --> Failed
    Failed --> Uploaded: manual retry
    Active --> Superseded: new version active
    Active --> Deleting: source deleted
    Deleting --> Deleted: chunks and vectors removed
    Deleted --> [*]
```

### Deletion and freshness propagation

```mermaid
sequenceDiagram
    actor Admin
    participant API
    participant KB as Knowledge service
    participant V as Vector index
    participant OS as Object storage
    participant AUD as Audit

    Admin->>API: delete source
    API->>KB: mark deleting, exclude from retrieval immediately
    KB->>V: delete vectors by source filter
    KB->>OS: delete original and derived objects
    KB->>KB: invalidate caches
    KB->>AUD: record deletion propagation complete
```

## US-032 — Retrieve relevant chunks

Acceptance: tenant-filtered results with source metadata.

```mermaid
sequenceDiagram
    participant AI as AI Engine
    participant KB as Knowledge service
    participant EM as Embedding adapter
    participant V as Vector/search index
    participant DB as Postgres

    AI->>KB: retrieve(query, tenant, allowed sources, k)
    KB->>EM: embed query
    EM-->>KB: vector
    KB->>V: search with mandatory tenant and source filter
    V-->>KB: ranked chunk ids and scores
    KB->>DB: load chunk text and source metadata
    KB->>KB: drop below threshold, dedupe, rerank
    KB->>DB: log RetrievalRun
    KB-->>AI: passages with source ids, version, score
```

## US-033 — Grounded answer or clear fallback

Acceptance: answer is not represented as sourced when retrieval has no useful evidence.

```mermaid
flowchart TD
    A["Retrieval result"] --> B{"Any passage above threshold?"}
    B -- No --> F1["Fallback: say not found, offer to clarify, ticket or human"]
    B -- Yes --> C{"Passages contradict each other or are stale?"}
    C -- Yes --> F2["Ask clarifying question or escalate"]
    C -- No --> D["Generate answer constrained to passages"]
    D --> E{"Every claim supported?"}
    E -- No --> G["Remove unsupported claims or fallback"]
    E -- Yes --> H["Reply with citations"]
    F1 & F2 & G --> I["Never mark as sourced"]
```

# 04 — Voice and Multimodal Diagrams

Source: `07-voice-and-multimodal.md`, modules M07, M08, M09.

## 4.1 Voice session lifecycle

```mermaid
stateDiagram-v2
    [*] --> Requested
    Requested --> PermissionPending: widget asks for microphone
    PermissionPending --> Denied: user refuses
    PermissionPending --> Connecting: granted
    Connecting --> Active: transport established
    Connecting --> Failed: timeout
    Active --> Listening
    Listening --> Processing: end of speech detected
    Processing --> Speaking: assistant audio starts
    Speaking --> Listening: playback finished
    Speaking --> Interrupted: user barge-in
    Interrupted --> Listening: obsolete audio cancelled
    Active --> Reconnecting: transport drop
    Reconnecting --> Active: resumed within window
    Reconnecting --> Ended: window expired
    Active --> Ended: user hangs up, quota or timeout
    Denied --> [*]
    Failed --> [*]
    Ended --> [*]
```

## 4.2 Two speech strategies

### Option A — modular pipeline

```mermaid
flowchart LR
    MIC["Customer audio"] --> T["M07 transport"] --> STT["M08 STT"]
    STT -->|partial: provisional| UI["Live caption only"]
    STT -->|final transcript| M09["M09 Transcript sync"]
    M09 --> CONV["M01 Conversation"] --> AI["M04 AI Engine"]
    AI --> TXT["Assistant text"] --> TTS["M08 TTS"] --> T --> SPK["Customer speaker"]
```

### Option B — speech-to-speech

```mermaid
flowchart LR
    MIC["Customer audio"] <--> T["M07 transport"] <--> S2S["M08 realtime multimodal model"]
    S2S -->|tool call request| TS["Tool Execution Service<br/>same authorization model"]
    TS --> S2S
    S2S -->|transcripts and events| M09["M09 Transcript sync"] --> CONV["M01 Conversation"]
    CONV -. policy and state .-> S2S
```

### Decision: which to start with

```mermaid
flowchart TD
    A["ADR-006: choose first strategy"] --> B{"Need explicit transcript and per-stage control?"}
    B -- Yes --> C["Option A modular"]
    B -- No --> D{"Lowest latency is top priority and provider coupling is acceptable?"}
    D -- Yes --> E["Option B speech-to-speech"]
    D -- No --> C
    C --> F["Validate product first. Do not build both fully."]
    E --> F
```

## 4.3 One voice turn (Option A) with persistence boundaries

```mermaid
sequenceDiagram
    actor Cu as Customer
    participant T as Voice transport
    participant STT as STT
    participant TS as Transcript sync
    participant CV as Conversation
    participant AI as AI Engine
    participant TTS as TTS

    Cu->>T: audio frames
    T->>STT: stream
    STT-->>TS: partial segments
    Note over TS: provisional, not persisted as messages
    STT-->>TS: final segment with sequence id
    TS->>CV: append finalized transcript message
    CV->>AI: new turn
    AI-->>CV: reply text
    CV->>TTS: synthesize
    TTS-->>T: audio stream
    T-->>Cu: spoken reply
    T->>TS: playback complete marker
    TS->>CV: mark assistant audio delivered
```

## 4.4 Interruption (barge-in)

```mermaid
sequenceDiagram
    actor Cu as Customer
    participant T as Voice transport
    participant TTS as TTS
    participant TS as Transcript sync
    participant CV as Conversation
    participant AI as AI Engine

    T-->>Cu: assistant audio playing
    Cu->>T: starts speaking
    T->>TTS: cancel generation
    T->>T: truncate playback buffer
    T->>TS: interrupted at offset N
    TS->>CV: store delivered portion only, flag truncated
    Note over CV: never record cancelled utterance as fully delivered
    T->>AI: cancel in-flight response if still generating
    Cu->>T: new utterance
    T->>TS: final transcript, new sequence id
    TS->>CV: append and request turn
```

## 4.5 Partial vs final transcript handling

```mermaid
flowchart TD
    A["STT event"] --> B{"Partial or final?"}
    B -- Partial --> C["Update ephemeral caption, overwrite previous partial"]
    B -- Final --> D{"segment id already processed?"}
    D -- Yes --> E["Ignore duplicate: same audio never becomes two messages"]
    D -- No --> F["Assign sequence id, order server-side"]
    F --> G["Persist TranscriptSegment and message in timeline"]
    G --> H["Emit turn request"]
    C --> I["Never durable, never visible to AI"]
```

## 4.6 Modality switching in one conversation

```mermaid
stateDiagram-v2
    [*] --> TextMode
    TextMode --> VoiceMode: customer starts voice (event voice.session.started)
    VoiceMode --> TextMode: customer ends voice (event voice.session.ended)
    VoiceMode --> VoiceMode: reconnect same session
    TextMode --> HumanOwned: handoff
    VoiceMode --> HumanOwned: handoff with provider transfer reference
    HumanOwned --> TextMode: resolved or returned to AI
    note right of VoiceMode
        Engine consumes normalized text and trusted state.
        It does not care if text was typed or transcribed.
    end note
```

## 4.7 Voice handoff bundle

```mermaid
flowchart LR
    subgraph Bundle["Handoff bundle"]
        direction LR
        B1["Conversation ID and verification level"]
        B2["Transcript and concise summary"]
        B3["Intent and unresolved question"]
        B4["Citations already used"]
        B5["Completed and failed tool executions"]
        B6["Ticket and SLA state"]
        B7["Current modality and provider transfer refs"]
    end
    AI["AI Engine"] --> F{"Restricted account data?"}
    F -- Yes --> R["Redact or mask per agent permission"]
    F -- No --> Bundle
    R --> Bundle
    Bundle --> INBOX["Human Inbox"]
```

## 4.8 Voice privacy and consent

```mermaid
flowchart TD
    A["Customer clicks voice"] --> B["Show notice: voice active, transcription, retention"]
    B --> C{"Consent given?"}
    C -- No --> T["Stay in text"]
    C -- Yes --> D["Request microphone permission only now"]
    D --> E{"Granted?"}
    E -- No --> T
    E -- Yes --> F["Start session with visible active indicator"]
    F --> G{"Recording retention enabled by tenant policy?"}
    G -- No --> H["Process stream, keep transcript only per transcript policy"]
    G -- Yes --> I["Store audio reference with audio retention policy"]
    H --> J["On disconnect: release mic and cleanup session"]
    I --> J
```

## 4.9 Voice metrics pipeline

```mermaid
flowchart LR
    ev1["session establishment"] --> M
    ev2["time to first audio"] --> M
    ev3["end-of-speech to response-start"] --> M
    ev4["total turn latency"] --> M
    ev5["interruption rate"] --> M
    ev6["transcript finalization failures"] --> M
    ev7["reconnects and drops"] --> M
    ev8["cost and duration per session"] --> M
    M[("Metrics store, tenant safe labels")] --> D["Cost and latency dashboard"]
    M --> A["Alerts on p95 latency or drop rate"]
```

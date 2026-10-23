# E09 — Voice MVP

Goal: real-time browser voice using the same conversation engine. Modules: M07, M08, M09. Deeper voice diagrams: see `../04-voice-multimodal.md`.

## Epic overview

```mermaid
flowchart LR
    E09["E09 Voice MVP"] --> US80["US-080 Start and end session"]
    E09 --> US81["US-081 Speak and hear response"]
    E09 --> US82["US-082 Interrupt the AI"]
    E09 --> US83["US-083 Switch text and voice"]
    E09 --> US84["US-084 Agent takeover of voice"]
    US80 --> US81 --> US82
    US81 --> US83 --> US84
```

## Reuse of the text engine

```mermaid
flowchart LR
    T["Typed text"] --> N["Normalized customer message"]
    V["Finalized transcript"] --> N
    N --> E["Same AI Engine, same tool authorization"]
    E --> R["Assistant text"]
    R --> W["Widget text"]
    R --> TTS["TTS audio"]
```

## US-080 — Start and end a voice session

Acceptance: explicit mic permission; session state and failures visible.

```mermaid
sequenceDiagram
    actor C as Customer
    participant W as Widget
    participant API as Support API
    participant VS as Voice session service
    participant MEDIA as Media transport

    C->>W: click voice
    W->>C: notice about voice and transcription
    W->>W: request microphone permission
    W->>API: create voice session for conversation
    API->>VS: authorize via session token, check quota
    VS-->>API: session id and transport credentials short-lived
    API-->>W: credentials
    W->>MEDIA: connect (WebRTC or WebSocket)
    MEDIA-->>VS: connected, emit voice.session.started
    W-->>C: visible active indicator
    C->>W: end call
    W->>MEDIA: close
    MEDIA-->>VS: ended, emit voice.session.ended
    VS->>VS: release resources, finalize transcript
```

## US-081 — Speak and receive a spoken response

Acceptance: provider configurable; failures have fallback path.

```mermaid
flowchart TD
    A["Customer speaks"] --> B["Speech provider adapter selected by SpeechConfiguration"]
    B --> C{"STT ok?"}
    C -- No --> F1["Fallback: ask to repeat or switch to text"]
    C -- Yes --> D["Final transcript to conversation"]
    D --> E["AI turn"]
    E --> G{"TTS ok?"}
    G -- No --> F2["Fallback: show reply as text, log audio generation failure"]
    G -- Yes --> H["Stream audio to customer"]
    H --> I["Emit latency metrics: first audio, turn latency"]
```

## US-082 — Interrupt the AI while it speaks

Acceptance: obsolete audio cancelled or truncated; not recorded as fully delivered.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> UserSpeaking: voice activity
    UserSpeaking --> Thinking: end of speech
    Thinking --> AssistantSpeaking: audio starts
    AssistantSpeaking --> Idle: finished, mark delivered
    AssistantSpeaking --> Cancelling: barge-in detected
    Cancelling --> UserSpeaking: stop TTS, flush buffer, store delivered part only
    Thinking --> UserSpeaking: user spoke again, cancel pending generation
```

## US-083 — Switch between text and voice

Acceptance: finalized transcript and message order remain coherent.

```mermaid
sequenceDiagram
    actor C as Customer
    participant W as Widget
    participant CV as Conversation timeline
    participant AI as AI Engine

    C->>W: types question
    W->>CV: message seq 1 (text)
    CV->>AI: turn
    AI-->>CV: reply seq 2
    C->>W: start voice
    CV->>CV: system_event seq 3 voice started
    C->>W: speaks
    W->>CV: transcript seq 4 (final only)
    CV->>AI: turn (same history)
    AI-->>CV: reply seq 5 (text plus audio ref)
    C->>W: hang up, types follow-up
    CV->>CV: system_event seq 6 voice ended
    W->>CV: message seq 7
    Note over CV: single ordered timeline, sequence assigned server-side
```

## US-084 — Agent takes over a voice conversation or receives its context

Acceptance: handoff behavior explicit for chosen telephony/media provider.

```mermaid
flowchart TD
    A["Handoff requested during voice"] --> B{"Provider supports live transfer to human audio?"}
    B -- Yes --> C["Transfer media leg to agent softphone, include bundle"]
    B -- No --> D["End AI voice leg, notify customer"]
    D --> E["Agent receives bundle in console"]
    E --> F{"Customer reachable?"}
    F -- "Chat widget open" --> G["Agent continues in text"]
    F -- No --> H["Callback ticket"]
    C --> I["Record HandoffEvent with provider transfer reference"]
    G --> I
    H --> I
```

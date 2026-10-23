# 07 — Voice and Multimodal Conversations

## Goal

A customer can start with text, switch to voice, return to text, or be transferred to a human without losing the durable conversation history.

## Voice subsystem responsibilities

### Real-time voice session
- Open and close media sessions.
- Track transport state, audio input/output, interruptions, silence, reconnects, and failures.
- Associate every voice session with a conversation and tenant.
- Enforce session duration and resource quotas.

### Speech processing
Two strategies should be supported behind a common abstraction.

**Option A: modular pipeline**
`audio → STT → conversation engine → TTS → audio`

Advantages: explicit transcript, modular provider choice, easier inspection of each stage.  
Trade-off: additional latency and more orchestration.

**Option B: speech-to-speech**
`audio ↔ real-time multimodal model`

Advantages: potentially more natural, lower-latency interactions.  
Trade-off: provider coupling and less explicit control over intermediate artifacts depending on provider.

Start with one strategy that matches latency, language, cost, and observability requirements; do not implement both fully before validating the product.

## Turn and interruption semantics

- Partial transcription is provisional.
- Finalized user speech creates a durable turn input.
- When a user interrupts generated speech, cancel or truncate the obsolete response where supported.
- Do not persist a canceled assistant utterance as if it were fully delivered.
- Avoid processing the same audio segment as both a final transcript and a second independent message.
- Preserve turn order with sequence IDs or timestamps plus server-side ordering.
- Keep audio chunks and ephemeral transport events separate from canonical messages.

## Switching modalities

A conversation can contain:
- text customer messages;
- finalized speech transcripts;
- assistant text;
- generated audio references;
- system events such as voice started/ended;
- handoff events.

The conversation engine should consume normalized text/intent and trusted state, not depend on whether the text came from typing or transcription.

## Human handoff

A handoff bundle should include:
- conversation ID and customer identity level/verification status;
- transcript and concise summary;
- customer intent and unresolved question;
- source citations already used;
- completed/failed tool executions;
- relevant ticket and SLA state;
- current modality and provider transfer references where appropriate.

Do not silently expose restricted account data in a handoff summary.

## Voice-specific operational metrics

- time to first audio;
- end-of-speech to response-start latency;
- total turn latency;
- interruption/cancellation rate;
- transcription confidence or provider quality indicators when available;
- reconnect and dropped-session rate;
- audio generation failures;
- cost and duration per session;
- handoff completion rate.

## Privacy

- Request microphone permission only when needed.
- Clearly communicate when voice is active and when recording/transcription is retained.
- Define audio and transcript retention separately.
- Avoid storing raw audio by default unless required by a defined product feature.
- Provide deletion, access, and consent workflows according to applicable law and customer policy.

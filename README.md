# AI Customer Support Platform — Project Documentation

This repository is the initial documentation pack for an AI-native customer support platform that supports full conversations over text and voice, grounded answers from organizational knowledge, authorized business actions, and human handoff.

## Documentation map

- `01-product-vision.md` — product goals, users, scope, and principles
- `02-module-catalog.md` — functional module inventory and responsibilities
- `03-system-architecture.md` — logical architecture and deployment approach
- `04-module-communication.md` — synchronous/asynchronous communication contracts
- `05-domain-model.md` — core entities and relationships
- `06-ai-conversation-engine.md` — orchestration, tools, grounding, and guardrails
- `07-voice-and-multimodal.md` — voice sessions, speech processing, transcript synchronization
- `08-integrations-and-tools.md` — tool contracts, connector model, external systems
- `09-security-privacy-reliability.md` — tenant isolation, secrets, audit, retries, retention
- `10-observability-and-evaluation.md` — operational metrics and AI evaluation
- `11-technology-stack.md` — proposed technology stack, selection criteria, assumptions
- `12-technology-by-task.md` — technologies for every epic, user story and Sprint
- `13-technology-decisions.md` — role and usage rule of each technology, decisions to validate, lock-in risks
- `scrum/` — Scrum project charter, roles, backlog, sprint plan, ceremonies, and Mermaid diagrams
- `diagrams/` — editable Mermaid and LaTeX/TikZ diagrams
- `diagrams/mermaid/` — detailed Mermaid pack (211 diagrams): architecture, flows, AI/voice, data model, UML (use case, class, sequence, activity, component, package, deployment, object), one diagram set per epic/user story and sprint. Standalone sources in `mmd/`, rendered PDF/SVG in `rendered/`, tooling in `tools/` (start at `00-index.md`)
- `docs/` — reveal.js decks (Scrum plan, product, technologies, engineering deep dive) with PDF handouts, published as the project site; `docs/assets/rapport.pdf` is the full report (open `docs/index.html`)
- `latex-scrum/` — Overleaf-ready LaTeX project for the Scrum artifacts report, the rapport (293 pages); `latex-scrum-overleaf.zip` is the upload bundle

## Recommended implementation strategy

Start as a **modular monolith** with explicit module boundaries and internal interfaces. Use asynchronous jobs/events where durability, retries, or slow processing require them. Extract services only when independent scaling, fault isolation, or deployment cadence justify the operational cost.

## Initial end-to-end milestone

A website assistant can:
1. accept a customer text message;
2. maintain a conversation;
3. retrieve relevant organization knowledge;
4. invoke one safe, read-only business tool;
5. answer with source-grounded information;
6. escalate to a human while preserving context;
7. emit audit and observability events.

Voice should reuse the same conversation engine and business-tool authorization model.

## Conventions

- `MUST` means required for correctness or security.
- `SHOULD` means recommended unless a documented reason exists.
- Provider-specific details belong in adapters, not in the core domain.
- AI output is untrusted input. Authorization and business invariants are enforced by application code.
- Do not store raw audio or sensitive customer data unless there is a clear product need, consent/legal basis, access policy, and retention policy.

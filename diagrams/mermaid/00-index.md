# Mermaid Diagram Pack — Index

Detailed Mermaid diagrams for every task in the AI Customer Support Platform docs. Large flows are split into parts so each diagram stays readable. Render with any Mermaid-capable viewer (GitHub, VS Code "Markdown Preview Mermaid Support", mermaid.live).

Existing diagrams that are not duplicated here: `../module-communication.mmd`, `../../scrum/05-mermaid-artifacts.md` (roadmap, epic dependency graph, Gantt, Scrum workflow, story lifecycle, release acceptance, demo sequence, module-to-epic coverage), and the ER and state diagrams embedded in docs 05 and 06 (expanded here).

## Standalone `.mmd` files

Every diagram below (211 in total) is also available as its own file under [mmd/](mmd/), already rendered to PDF and SVG under [rendered/](rendered/) (tooling in [tools/](tools/)), one folder per source file (for example `mmd/epics/E06-safe-business-tools/04-us-051-customer-asks-for-order-status.mmd`). Each file starts with a `%% Source:` comment naming the Markdown file and heading it came from. The `.md` files stay the readable version; the `.mmd` files are for `mmdc`, mermaid.live, or embedding. If you edit one, update the other.

## Platform-level

| File | Contents |
|---|---|
| [01-architecture.md](01-architecture.md) | System context, layers, deployables, 5 module-domain views, event catalog |
| [02-cross-cutting-flows.md](02-cross-cutting-flows.md) | Webhook inbox, outbox, delivery states, retry, tool pipeline (2 parts), tenant resolution, secrets, degradation, retention, security tests |
| [03-ai-engine.md](03-ai-engine.md) | Turn pipeline in 4 phases, state machine, trust levels, escalation, response policy, provider adapter, agent version lifecycle |
| [04-voice-multimodal.md](04-voice-multimodal.md) | Voice session states, strategy A and B, voice turn, barge-in, partial vs final, modality switch, privacy |
| [05-data-model.md](05-data-model.md) | ER diagrams per aggregate (10 groups) |

## Epics and user stories (43 stories)

| Epic | File | Stories |
|---|---|---|
| E01 Tenant and access | [epics/E01-tenant-and-access.md](epics/E01-tenant-and-access.md) | US-001, 002, 003 |
| E02 Conversation core | [epics/E02-conversation-core.md](epics/E02-conversation-core.md) | US-010, 011, 012, 013 |
| E03 Website chat | [epics/E03-website-chat.md](epics/E03-website-chat.md) | US-020, 021, 022 |
| E04 Knowledge and RAG | [epics/E04-knowledge-and-rag.md](epics/E04-knowledge-and-rag.md) | US-030, 031, 032, 033 |
| E05 AI orchestration | [epics/E05-ai-orchestration.md](epics/E05-ai-orchestration.md) | US-040, 041, 042, 043 |
| E06 Safe business tools | [epics/E06-safe-business-tools.md](epics/E06-safe-business-tools.md) | US-050, 051, 052, 053 |
| E07 Human handoff | [epics/E07-human-handoff.md](epics/E07-human-handoff.md) | US-060, 061, 062, 063 |
| E08 Tickets | [epics/E08-tickets.md](epics/E08-tickets.md) | US-070, 071 |
| E09 Voice MVP | [epics/E09-voice-mvp.md](epics/E09-voice-mvp.md) | US-080 to 084 |
| E10 Workflow, routing, SLA | [epics/E10-workflow-routing-sla.md](epics/E10-workflow-routing-sla.md) | US-090, 091, 092 |
| E11 Integrations and channels | [epics/E11-integrations-and-channels.md](epics/E11-integrations-and-channels.md) | US-100, 101, 102 |
| E12 Observability, eval, usage | [epics/E12-observability-evaluation-usage.md](epics/E12-observability-evaluation-usage.md) | US-110 to 113 |

## Technology

| File | Contents |
|---|---|
| [08-technology.md](08-technology.md) | Technology stack map, a message through the stack, voice stack, delivery toolchain, when each technology arrives |

## UML models

| File | Contents |
|---|---|
| [uml/U1-use-cases.md](uml/U1-use-cases.md) | Use case diagrams: system level, customer, support staff, administration and governance |
| [uml/U2-class-diagrams.md](uml/U2-class-diagrams.md) | Class diagrams per module group (access, conversation, channels, AI engine, knowledge, tools, handoff and tickets, voice, workflow, audit and evaluation) plus design patterns |
| [uml/U3-sequence-diagrams.md](uml/U3-sequence-diagrams.md) | 10 runtime sequences: end to end, duplicate webhook, prompt injection, approval, handoff, ingestion, release gate, deletion, barge-in, circuit breaker |
| [uml/U4-activity-diagrams.md](uml/U4-activity-diagrams.md) | Swimlane activity diagrams: conversation, ingestion, handoff, tool authorization, release, incident |
| [uml/U5-component-package-deployment-object.md](uml/U5-component-package-deployment-object.md) | Component, package, deployment (MVP and later), object and composite-structure diagrams |

## Planning

| File | Contents |
|---|---|
| [06-sprints.md](06-sprints.md) | Sprint sequence, increments, Gantt, one diagram per sprint (S0 to S8), story-to-sprint traceability |
| [07-scrum-release-risks.md](07-scrum-release-risks.md) | Roles, events, DoR, DoD, release criteria, rollout, risks, ADR order, deferred decisions |

## Conventions used

- `flowchart` for processes and decisions, `sequenceDiagram` for cross-module interactions, `stateDiagram-v2` for lifecycles, `erDiagram` for data.
- Every user-story diagram is preceded by the story's acceptance criteria.
- Labels avoid unquoted special characters so diagrams parse in older Mermaid versions.

# Scrum Charter

## Product goal

Deliver an AI-native customer support platform that handles complete text conversations first, provides grounded answers and safe tool use, supports human handoff, and then expands to real-time voice and additional channels.

## Scrum setup

- **Product Owner:** accountable for product value, Product Goal, and Product Backlog ordering.
- **Scrum Master:** coaches Scrum, removes impediments, and helps the team improve.
- **Developers:** cross-functional team that designs, builds, tests, integrates, secures, and operates a usable Increment.
- **Stakeholders:** support teams, organization administrators, customers, security/privacy, and business-system owners.

Roles can be held by a small team, but accountabilities must remain clear.

## Product Goal

A customer can contact an organization through website chat, receive accurate knowledge-grounded answers, complete at least one authorized read-only business lookup, and reach a human without losing conversation context. The architecture must be ready to add voice without duplicating business reasoning.

## Proposed release goals

- **Release 1 — Text support MVP:** tenant foundation, website chat, conversation lifecycle, RAG, one read-only tool, handoff, basic analytics and audit.
- **Release 2 — Voice MVP:** real-time browser voice, speech processing, transcript synchronization, interruption handling, voice handoff and voice observability.
- **Release 3 — Operations expansion:** additional channels, workflow automation, routing/SLA, connectors, evaluation, and commercial usage controls.

## Sprint approach

- Suggested Sprint length: 2 weeks.
- Each Sprint has one Sprint Goal and a potentially releasable Increment.
- Sprint Planning selects work based on Product Goal, ordered backlog, capacity, and Definition of Done.
- Daily Scrum is for Developers to inspect progress toward the Sprint Goal and adapt the plan.
- Sprint Review inspects the Increment with stakeholders and adapts the Product Backlog.
- Sprint Retrospective improves team effectiveness and quality.
- Refinement is ongoing; it is not a formal Scrum event.

## Working assumptions

- A small team is building a modular monolith initially.
- Product design, infrastructure, security and automated tests are part of delivery—not separate downstream phases.
- Story points are team-specific estimates, not time conversions.
- Sprint sequence and estimates are provisional until capacity and dependencies are confirmed.

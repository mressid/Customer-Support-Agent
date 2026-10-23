#!/usr/bin/env python3
"""Generate docs/technologies.html (the technology deck).

Content comes from 11-technology-stack.md, 12-technology-by-task.md and 13-technology-decisions.md.
Run:  python3 docs/tools/build_technologies.py && python3 docs/tools/apply_icons.py
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "technologies.html"
GRAD = "linear-gradient(135deg,#0f2b46 0%,#1F4E79 62%,#2E7D32 130%)"

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Technologies - AI Customer Support Platform</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link rel="stylesheet" href="vendor/reveal/dist/reset.css">
<link rel="stylesheet" href="vendor/reveal/dist/reveal.css">
<link rel="stylesheet" href="vendor/reveal/dist/theme/white.css">
<link rel="stylesheet" href="css/theme.css">
</head>
<body>
<div class="reveal"><div class="slides">
'''
FOOT = '''
</div></div>
<script src="vendor/reveal/dist/reveal.js"></script>
<script src="vendor/reveal/plugin/notes/notes.js"></script>
<script src="vendor/reveal/plugin/zoom/zoom.js"></script>
<script src="vendor/reveal/plugin/highlight/highlight.js"></script>
<script src="js/deck.js"></script>
</body>
</html>
'''


def opener(num, title, sub, grad="linear-gradient(135deg,#0f2b46,#1F4E79)"):
    return ('  <section class="on-dark" data-transition="convex" data-background-gradient="%s">\n'
            '    <div class="hero"><div class="kicker">Chapter %d</div><h1>%s</h1><p>%s</p></div>\n  </section>\n') % (grad, num, title, sub)


def img(name, alt, cls="", cap=""):
    c = "<figcaption>%s</figcaption>" % cap if cap else ""
    return '<figure class="diagram %s"><img src="assets/%s.svg" alt="%s">%s</figure>' % (cls, name, alt, c)


def sl(body, extra="", notes=""):
    n = '<aside class="notes">%s</aside>' % notes if notes else ""
    return "  <section %s>\n%s\n%s\n  </section>\n" % (extra, body, n)


def stack(chapter, *slides):
    return '<section data-chapter="%s">\n%s</section>\n' % (chapter, "".join(slides))


def card(title, role, rule, alt, cls=""):
    return ('<div class="card %s fragment fade-up"><h3>%s</h3><p><b>Role</b> %s</p><p><b>Rule</b> %s</p>'
            '<p class="muted">Instead of: %s</p></div>') % (cls, title, role, rule, alt)


def cards(kicker, title, items):
    colors = ["brand", "accent", "amber"]
    body = '<div class="kicker">%s</div><h2>%s</h2><div class="grid g3">%s</div>' % (
        kicker, title, "".join(card(*it, cls=colors[i % 3]) for i, it in enumerate(items)))
    return sl(body)


def table(headers, rows, fragment=True):
    th = "".join("<th>%s</th>" % h for h in headers)
    f = ' class="fragment"' if fragment else ""
    tr = "".join("<tr%s>%s</tr>" % (f, "".join("<td>%s</td>" % c for c in r)) for r in rows)
    return "<table><tr>%s</tr>%s</table>" % (th, tr)


out = [HEAD]

# ---------------------------------------------------------------- title
out.append('''<section class="on-dark" data-transition="zoom" data-background-gradient="%s">
  <div class="hero"><div class="kicker">Technology overview</div><h1>The technologies behind the platform</h1>
  <p>What we use, the role each one plays, the rule for using it, and what it could be swapped for.</p></div>
  <div class="hint">→ next chapter · ↓ details inside a chapter · Esc overview · I all decks · click a diagram to enlarge</div>
  <aside class="notes">Everything here is a proposal. Each choice is confirmed or replaced by an architecture decision record. The full detail is in the rapport, Part V.</aside>
</section>
''' % GRAD)

# ---------------------------------------------------------------- 1 how we choose
out.append(stack("1 · How we choose",
    opener(1, "How we choose", "Criteria first, products second. Every name here is an example of a category."),
    sl('''<div class="kicker">Status</div><h2>A proposal, confirmed by decisions</h2>
<blockquote>Each technology is a <strong>recommendation</strong>. It becomes a decision only through an <strong>ADR</strong>, with evidence from a spike or an evaluation.</blockquote>
<ul class="check small"><li class="fragment">Provider-specific parts live in adapters, never in the core domain</li>
<li class="fragment">Vendor names, prices, licenses and data policies are verified at ADR time</li>
<li class="fragment">If the team prefers Python, only the language rows change, not the architecture</li></ul>'''),
    sl('''<div class="kicker">Selection criteria</div><h2>Six tests every choice must pass</h2>
<div class="grid g3" style="gap:14px">
<div class="tile"><b>Fits the team</b><span>Few moving parts, one main language and database</span></div>
<div class="tile"><b>Proven where it matters</b><span>Mature storage, queues, auth and delivery</span></div>
<div class="tile"><b>Security first</b><span>Cross-tenant access is hard by design</span></div>
<div class="tile"><b>Portable core</b><span>No vendor type inside the domain</span></div>
<div class="tile"><b>Observable and testable</b><span>Every decision and tool call can be traced and replayed</span></div>
<div class="tile"><b>Reasonable cost</b><span>Start simple, keep a trigger for moving up</span></div>
</div>'''),
    sl('''<div class="kicker">Assumptions</div><h2>What we assume today</h2>
<ul class="check small"><li class="fragment">A small team, text MVP first, voice and operations later</li>
<li class="fragment">TypeScript as the primary language</li>
<li class="fragment">Cloud-agnostic containers, managed services welcome, no design tied to one cloud</li>
<li class="fragment">One channel (website chat) and exactly one read-only business tool in the first release</li></ul>'''),
))

# ---------------------------------------------------------------- 2 the stack
out.append(stack("2 · The stack",
    opener(2, "The stack at a glance", "Seven layers, one modular monolith in the middle."),
    sl('''<h2>The stack in one picture</h2>
<div class="split tight"><ul>
<li class="fragment"><b>Clients:</b> widget, console, browser voice</li>
<li class="fragment"><b>App:</b> one TypeScript codebase, API and worker</li>
<li class="fragment"><b>Data:</b> PostgreSQL does most of the work</li>
<li class="fragment"><b>Providers:</b> models, speech and business systems behind adapters</li>
<li class="fragment"><b>Platform:</b> login, secrets, flags</li>
<li class="fragment"><b>Observability:</b> traces, metrics, errors</li></ul>
%s</div>''' % img("tech-stack", "Technology stack map")),
    sl('<h2>One message through the stack</h2>' + img("tech-request", "A customer message through the stack", "",
       "No database transaction is held open while the model or a business system is called"), 'data-transition="fade"'),
))

# ---------------------------------------------------------------- 3 backend and data
out.append(stack("3 · Backend and data",
    opener(3, "Backend and data", "One language, one database, and rules that keep tenants apart."),
    cards("Application and storage", "Core building blocks", [
        ("TypeScript and NestJS", "application code and module boundaries", "modules talk only through interfaces, never through internals", "Python with FastAPI"),
        ("PostgreSQL 16", "system of record, queue, outbox and vector index", "no transaction stays open during an external call", "MySQL, CockroachDB"),
        ("Row-level security", "tenant isolation enforced by the database", "tenant context is set per request, and a missing context returns nothing", "schema per tenant"),
    ]),
    cards("Search, jobs and files", "Retrieval, work queues and objects", [
        ("pgvector and full-text", "knowledge retrieval", "every query carries tenant and source filters", "Qdrant, OpenSearch"),
        ("pg-boss", "durable jobs, retries and delayed jobs", "enqueue in the same transaction as the change, and keep consumers idempotent", "BullMQ, RabbitMQ, SQS"),
        ("Redis and S3 storage", "rate limits and short-lived data, documents and media", "nothing durable lives only in Redis, objects are private with signed URLs", "in-memory, GCS or Azure Blob"),
    ]),
))

# ---------------------------------------------------------------- 4 AI stack
out.append(stack("4 · AI stack",
    opener(4, "The AI stack", "Models, retrieval, contracts and the evidence that they work."),
    cards("Models and retrieval", "How the AI gets its answers", [
        ("LLM adapter", "model access with routing", "vendor types never leave the adapter, and model, latency and usage are recorded", "OpenAI, Google, self-hosted"),
        ("Embedding adapter", "text vectors for retrieval", "index and query use the same model version", "Voyage AI, OpenAI, BGE or E5"),
        ("Hybrid retrieval", "find the evidence", "vector plus keyword, fused and thresholded, with a reranker only if evaluation shows a gain", "a dedicated search engine"),
    ]),
    sl('''<div class="kicker">Model routing, decided by ADR-005</div><h2>Right-sized model for each job</h2>
<div class="grid g3">
<div class="card brand fragment fade-up"><h3>Small model</h3><p>Intent and risk classification, rolling summaries, handoff bundles.</p></div>
<div class="card accent fragment fade-up"><h3>Mid-size model</h3><p>Customer replies, grounded in retrieved evidence and verified tool results.</p></div>
<div class="card amber fragment fade-up"><h3>Large model</h3><p>Hard cases that need more reasoning, and judging evaluation runs.</p></div>
</div><p class="small muted fragment">Chosen on correctness, groundedness, latency and cost per resolved conversation.</p>'''),
    cards("Contracts and proof", "Typed tools and measured quality", [
        ("Tool contracts", "typed, validated tool calls", "schema with additionalProperties false, and validation before execution", "TypeBox, Pydantic"),
        ("AI regression evaluation", "regression suite and release gate", "deterministic assertions gate release, and model judges are one signal only", "DeepEval, a custom runner"),
        ("LLM tracing", "replayable traces of model calls", "redact before sending, and sample by policy", "LangSmith, OpenTelemetry GenAI conventions"),
    ]),
))

# ---------------------------------------------------------------- 5 clients and identity
out.append(stack("5 · Clients and identity",
    opener(5, "Clients, channels and identity", "What customers and staff touch, and how we know who they are."),
    cards("Interfaces", "Widget, console and live transport", [
        ("Preact widget", "customer chat on the website", "Shadow DOM isolation, no secrets in the bundle, works under a strict CSP", "React"),
        ("React console", "agent inbox and admin screens", "the UI hides, the API denies", "Vue, Angular"),
        ("WebSocket and SSE", "live messages", "persist first, push second", "long polling"),
    ]),
    cards("Identity and channels", "Login, sessions and later channels", [
        ("OIDC provider", "staff login", "no password handling in our code, authorization stays in the app", "Ory, WorkOS"),
        ("JWT sessions", "widget session for customers", "short lifetime, scoped claims, verified on every call", "opaque tokens"),
        ("Email and messaging adapters", "later channels", "same canonical event contract as website chat", "other providers"),
    ]),
))

# ---------------------------------------------------------------- 6 voice
out.append(stack("6 · Voice",
    opener(6, "Voice", "Real-time voice on the same engine and the same authorization.", "linear-gradient(135deg,#0f2b46,#2E7D32 150%)"),
    sl('<h2>The voice stack</h2>' + img("tech-voice", "Voice stack", "", "Partial transcripts stay ephemeral. Only finalized speech becomes a message."), 'data-transition="fade"'),
    cards("Voice components", "Media, speech and the alternative", [
        ("LiveKit and WebRTC", "real-time audio", "access tokens are short-lived and scoped to one conversation", "Twilio Voice, Daily"),
        ("STT and TTS adapters", "speech in and speech out", "cancel on barge-in, and keep no raw audio by default", "Whisper self-hosted"),
        ("Speech-to-speech", "low-latency voice option", "tool calls still pass through our authorization", "the modular pipeline"),
    ]),
    sl('''<div class="kicker">Spike in Sprint 7</div><h2>How we will decide</h2>
<ul class="check small"><li class="fragment">End-of-speech to response latency</li><li class="fragment">Language coverage</li><li class="fragment">Cost per minute</li><li class="fragment">Control over the transcript</li><li class="fragment">Privacy and retention options</li><li class="fragment">Handoff behavior for the chosen provider</li></ul>'''),
))

# ---------------------------------------------------------------- 7 integrations and security
out.append(stack("7 · Integrations and security",
    opener(7, "Integrations and security", "Reaching business systems without handing over the keys.", "linear-gradient(135deg,#0f2b46,#b3382c 190%)"),
    cards("Reaching out", "Connectors, secrets and inbound events", [
        ("Connector adapters", "reach business systems", "one interface, typed errors, timeout and idempotency", "vendor SDKs inside adapters"),
        ("Secret manager", "credentials", "reference by id, never in logs, prompts or the repository", "Vault, Doppler"),
        ("Webhook verification", "trust inbound events", "HMAC and timestamp check, deduplicate by event id", "provider SDK verifiers"),
    ]),
    cards("Defensive layers", "Validation, files and resilience", [
        ("Zod and Ajv", "validation at the edges", "validate requests, adapter boundaries and model output", "TypeBox"),
        ("File safety", "uploads you can trust", "content sniffing and a malware scan before indexing, private by default", "managed scanning"),
        ("Retries and breakers", "survive flaky providers", "bounded attempts with jitter, and an open breaker fails fast", "a custom implementation"),
    ]),
))

# ---------------------------------------------------------------- 8 quality and delivery
out.append(stack("8 · Quality and delivery",
    opener(8, "Quality and delivery", "Test with real databases, scan every change, ship behind flags."),
    cards("Testing and scanning", "What runs on every change", [
        ("Vitest and Testcontainers", "unit and integration tests", "use a real Postgres for tenant and authorization tests", "Jest"),
        ("Playwright and k6", "end-to-end and load tests", "cover widget and console critical paths, and run load tests before each release", "Cypress"),
        ("Security scanners", "static, secret and dependency scans", "Semgrep, gitleaks and Trivy are required checks on every merge", "Snyk, SonarQube"),
    ]),
    cards("Running it", "Observe, build, deploy, roll back", [
        ("OpenTelemetry and Grafana", "traces, metrics and logs", "trace id on every request and job, no personal data in labels", "Datadog"),
        ("CI/CD and Docker", "automation and packaging", "trunk-based, no manual production deploys, one image runs as API and worker", "GitLab CI"),
        ("Terraform and OpenFeature", "infrastructure and flags", "environments are reproducible, and every risky feature ships behind a flag", "Pulumi"),
    ]),
    sl('<h2>From commit to production</h2>' + img("tech-delivery", "Delivery toolchain", "short",
       "Gates run in order. An unhealthy canary rolls back or disables the flag."), 'data-transition="fade"'),
))

# ---------------------------------------------------------------- 9 by task
epics_a = [
    ("E01 Tenant and access", "Postgres RLS, Testcontainers, OIDC, jose tokens"),
    ("E02 Conversation core", "NestJS, WebSocket, Postgres sequences, outbox"),
    ("E03 Website chat", "Preact Web Component, JWT sessions, Redis rate limits"),
    ("E04 Knowledge and RAG", "S3, ClamAV, pg-boss, pgvector with full-text"),
    ("E05 AI orchestration", "State machine, LLM adapter, AbortController, Langfuse"),
    ("E06 Safe business tools", "Ajv, connector adapters, idempotency keys, audit table"),
]
epics_b = [
    ("E07 Human handoff", "SKIP LOCKED claims, WebSocket updates, React console"),
    ("E08 Tickets", "Postgres, keyset pagination, TanStack Table"),
    ("E09 Voice MVP", "LiveKit, STT and TTS adapters, voice activity detection"),
    ("E10 Workflow, routing, SLA", "Workflow state machine, pg-boss timers, Temporal evaluated"),
    ("E11 Integrations and channels", "Secret manager, HMAC webhooks, email and messaging adapters"),
    ("E12 Observability, evaluation, usage", "OpenTelemetry, Grafana, promptfoo, Langfuse"),
]
sprints = [
    ("Sprint 0", "Docker Compose, CI, Terraform skeleton, migrations, secrets"),
    ("Sprint 1", "NestJS, row-level security, audit table, OpenTelemetry, Testcontainers"),
    ("Sprint 2", "Preact widget, WebSocket gateway, JWT sessions, Playwright"),
    ("Sprint 3", "Object storage, ClamAV, parsers, pg-boss ingestion, pgvector"),
    ("Sprint 4", "LLM adapter, structured outputs, citations, evaluation harness"),
    ("Sprint 5", "Ajv tool registry, connector with breaker, React console inbox"),
    ("Sprint 6", "Dashboards, k6, backup drill, feature flags, evaluation gate"),
    ("Sprint 7", "LiveKit, voice activity detection, STT and TTS or speech-to-speech"),
    ("Sprint 8", "Transcript sync, barge-in cancellation, cost and latency dashboard"),
]
out.append(stack("9 · Technology by task",
    opener(9, "Technology by task", "Which technologies each epic and Sprint relies on."),
    sl('<div class="kicker">Epics 1 to 6</div><h2>Technology by epic</h2>' + table(["Epic", "Key technologies"], epics_a)),
    sl('<div class="kicker">Epics 7 to 12</div><h2>Technology by epic</h2>' + table(["Epic", "Key technologies"], epics_b)),
    sl('<div class="kicker">Arrival order</div><h2>Technology by Sprint</h2>' + table(["Sprint", "Introduced"], sprints)),
    sl('<h2>When each technology arrives</h2>' + img("tech-release", "When each technology arrives", "short",
       "Release 1 carries the core stack, voice adds real-time pieces, operations adds channels and workflows"), 'data-transition="fade"'),
    sl('''<div class="kicker">Per story</div><h2>43 stories, each with its technologies</h2>
<p>The report lists the technologies and the approach for every user story and every Sprint.</p>
<p class="small muted">See the rapport, Part V, chapter "Technology by Task".</p>'''),
))

# ---------------------------------------------------------------- 10 decisions
decisions_a = [
    ("LLM provider and routing", "Two or three providers and model sizes", "Sprint 4"),
    ("Vector search", "pgvector against a dedicated engine", "Sprint 3"),
    ("Queue and outbox", "pg-boss against Redis with BullMQ", "Sprints 0 and 1"),
    ("Authentication", "Keycloak, Auth0, Cognito", "Sprint 1"),
    ("Hosting", "Managed containers, Fly.io or Render, Kubernetes", "Sprint 0"),
]
decisions_b = [
    ("Speech strategy", "Modular STT and TTS against speech-to-speech", "Sprint 7"),
    ("Voice transport and telephony", "LiveKit, Twilio, Daily", "Sprint 7"),
    ("Retention and consent", "Audio and transcript retention models", "Sprint 7"),
    ("Workflow engine", "Custom state machine against Temporal", "Release 3"),
]
lock = [
    ("LLM provider", "Medium", "Adapter, provider-neutral tool schemas, evaluation suite to compare models"),
    ("Embedding model", "Medium", "Store the model version per chunk and keep a re-index job"),
    ("Speech and voice", "High for speech-to-speech", "One strategy first, thin adapters, measure before committing"),
    ("PostgreSQL and pgvector", "Low to medium", "Standard SQL, retrieval behind an interface, documented switch trigger"),
    ("Cloud services", "Medium", "Containers, Terraform modules, S3-compatible API"),
    ("Observability and flags", "Low", "OpenTelemetry and OpenFeature as the client layers"),
]
out.append(stack("10 · Decisions and risks",
    opener(10, "Decisions and risks", "What we still have to validate, and how we limit lock-in.", "linear-gradient(135deg,#0f2b46,#2E7D32 150%)"),
    sl('<div class="kicker">Validate with evidence</div><h2>Decisions to make first</h2>' + table(["Decision", "Options to compare", "When"], decisions_a)),
    sl('<div class="kicker">Validate with evidence</div><h2>Decisions to make later</h2>' + table(["Decision", "Options to compare", "When"], decisions_b)),
    sl('<div class="kicker">Keeping options open</div><h2>Lock-in and mitigation</h2>' + table(["Technology", "Lock-in", "Mitigation"], lock)),
))

# ---------------------------------------------------------------- close
out.append('''<section class="on-dark" data-transition="zoom" data-background-gradient="%s">
  <div class="hero"><h1>Choose boring where it matters</h1>
  <p>Spend the novelty on AI behavior, and keep everything else proven, portable and observable.</p>
  <p class="small">Full detail: <a href="assets/rapport.pdf">rapport.pdf</a>, Part V.</p></div>
</section>
''' % GRAD)

out.append(FOOT)
OUT.write_text("".join(out))
print("wrote", OUT, "sections:", "".join(out).count("<section"))

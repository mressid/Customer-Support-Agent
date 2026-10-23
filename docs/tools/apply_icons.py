#!/usr/bin/env python3
"""Apply the icon system to the decks (safe to re-run).

* replaces emoji with Lucide line icons (inlined as an SVG sprite, works offline)
* adds icon chips to cards and tiles using the title -> icon map below
* generates the dark-slide background art in assets/bg/
* adds the logo mark to each deck's title slide
Icons: Lucide (ISC license), copied to assets/icons/.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
ICONS = ROOT / "assets" / "icons"
BG = ROOT / "assets" / "bg"
DECKS = ["scrum.html", "product.html", "engineering.html", "technologies.html"]

EMOJI_ICON = {"🙋": "user", "🎧": "headset", "📊": "chart-column", "🛠️": "wrench", "🩺": "activity",
              "🎲": "dice-5", "🔌": "plug", "🔒": "lock", "✔": "circle-check", "📚": "book-open-check",
              "🎯": "target", "⚡": "gauge"}

TITLE_ICON = {
    # why scrum / roles
    "AI behaviour is uncertain": "dice-5", "Vendors drive risk": "plug", "Security is not a phase": "lock",
    "Product Owner": "compass", "Scrum Master": "life-buoy", "Developers": "code-xml",
    "Every item": "list-checks", "AI items add": "bot", "Voice items add": "mic",
    "Text support MVP": "message-square", "Voice MVP": "mic", "Operations expansion": "workflow",
    "Architecture decisions to write (ADRs)": "file-text", "Do not decide yet": "circle-pause",
    # vision / users
    "Faster correct answers": "zap", "Humans stay one step away": "users", "Auditable AI": "scroll-text",
    "Customer": "user", "Support agent": "headset", "Support lead": "chart-column", "Org admin": "settings",
    "Admin": "settings", "Platform operator": "activity", "Lead and operator": "chart-column",
    "In the MVP (text)": "rocket", "Later": "clock",
    # modules
    "Customer interaction": "messages-square", "AI and voice": "bot", "Support operations": "headset",
    "Integrations and insight": "plug", "Platform": "layers",
    # ai engine
    "The model may": "bot", "The application enforces": "shield-check", "Never": "ban",
    "Evidence is good": "circle-check", "Evidence is missing or conflicting": "circle-help",
    # integrations
    "Known identity": "user-check", "Verified proof": "shield-check", "No proof": "user-x",
    "Retry with backoff": "refresh-cw", "Never retry blindly": "octagon-alert", "Not retryable": "ban",
    "Happy path": "circle-check", "When it goes wrong": "triangle-alert",
    "AI provider": "cpu", "Retrieval": "search", "A business tool": "wrench",
    "A · Modular pipeline": "workflow", "B · Speech to speech": "audio-lines",
    # human
    "What happened": "file-text", "What we know": "lightbulb", "What to watch": "eye",
    "Conversation": "messages-square", "Ticket": "ticket", "Routing": "route", "SLA": "timer", "Workflows": "workflow",
    "Secrets": "key-round", "Data": "database", "Platform ": "layers",
    # quality
    "AI and RAG": "brain-circuit", "Voice": "mic", "AI evaluation": "clipboard-check",
    "Unit and integration": "flask-conical", "Contract tests": "file-check", "Tenant and authz tests": "shield-check",
    "Resilience": "refresh-ccw", "Load and recovery": "gauge", "Demo": "play",
    # engineering
    "TurnOrchestrator": "workflow", "ContextBuilder": "layers", "Planner": "route", "PolicyEngine": "scale",
    "ResponseGenerator": "pen-line", "OutputGuard": "shield-check", "ModelProvider": "cpu",
    "SpeechProvider": "audio-lines", "Connector": "plug", "VectorIndex": "database", "SecretManager": "key-round",
    "Queue": "list-ordered",
    # tiles: principles
    "Conversation first": "message-square", "Same brain for text and voice": "audio-lines",
    "Grounded answers": "book-open-check", "Safe actions": "shield-check", "Human escape hatch": "life-buoy",
    "Tenant isolation by default": "building-2", "Observable and testable": "eye", "Provider portability": "repeat",
    # tiles: reliability
    "Durable inbox": "inbox", "Transactional outbox": "send", "Idempotency keys": "key-round",
    "Bounded retries": "refresh-cw", "Dead-letter queue": "archive", "Timeouts and breakers": "timer",
    "Health checks": "heart-pulse", "Honest degradation": "triangle-alert",
    # tiles: data model
    "Access": "users", "Customer and channel": "radio", "Agent": "bot", "Knowledge": "library", "Tools": "wrench",
    "Handoff and tickets": "ticket", "Workflow and SLA": "workflow", "Audit and usage": "scroll-text",
    # technology deck
    "TypeScript and NestJS": "code-xml", "PostgreSQL 16": "database", "Row-level security": "shield-check",
    "pgvector and full-text": "search", "pg-boss": "list-ordered", "Redis and S3 storage": "server",
    "LLM adapter": "cpu", "Embedding adapter": "layers", "Hybrid retrieval": "library", "Tool contracts": "file-check",
    "AI regression evaluation": "clipboard-check", "LLM tracing": "eye",
    "Small model": "zap", "Mid-size model": "cpu", "Large model": "brain",
    "Preact widget": "message-square", "React console": "settings", "WebSocket and SSE": "radio",
    "OIDC provider": "key-round", "JWT sessions": "lock", "Email and messaging adapters": "send",
    "LiveKit and WebRTC": "mic", "STT and TTS adapters": "audio-lines", "Speech-to-speech": "bot",
    "Connector adapters": "plug", "Secret manager": "key", "Webhook verification": "shield-check",
    "Zod and Ajv": "check", "File safety": "shield", "Retries and breakers": "refresh-cw",
    "Vitest and Testcontainers": "flask-conical", "Playwright and k6": "play", "Security scanners": "shield-check",
    "OpenTelemetry and Grafana": "activity", "CI/CD and Docker": "git-branch", "Terraform and OpenFeature": "sliders-horizontal",
    "Fits the team": "users", "Proven where it matters": "shield-check", "Security first": "lock",
    "Portable core": "repeat", "Reasonable cost": "gauge",
}
EPIC_ICON = {"E01": "building-2", "E02": "messages-square", "E03": "globe", "E04": "library", "E05": "brain-circuit",
             "E06": "wrench", "E07": "hand-helping", "E08": "ticket", "E09": "mic", "E10": "git-branch",
             "E11": "plug-zap", "E12": "chart-line"}
LOGO_ICON = "message-square"

USED = set()


def ico(name):
    USED.add(name)
    return '<svg class="ico" aria-hidden="true"><use href="#i-%s"/></svg>' % name


def chip(name, extra=""):
    return '<div class="chip%s">%s</div>' % ((" " + extra) if extra else "", ico(name))


def sprite():
    parts = []
    for name in sorted(USED):
        svg = (ICONS / (name + ".svg")).read_text()
        inner = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
        inner = re.sub(r"^\s*<svg[^>]*>", "", inner.strip(), flags=re.S)
        inner = re.sub(r"</svg>\s*$", "", inner).strip()
        parts.append('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (name, re.sub(r"\s+", " ", inner)))
    return ('<!--ICON-SPRITE--><svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" '
            'aria-hidden="true">%s</svg><!--/ICON-SPRITE-->' % "".join(parts))


def bg_svg(variant, num):
    glow2 = {"blue": ("#1b9a68", .30), "title": ("#1b9a68", .45), "green": ("#1b9a68", .50), "red": ("#c24235", .45)}[variant]
    glow1 = {"blue": ("#3585d4", .55), "title": ("#3585d4", .55), "green": ("#2bb383", .30), "red": ("#3585d4", .35)}[variant]
    base = {"blue": ("#06182a", "#0e3560", "#10466a"), "title": ("#06182a", "#0e3560", "#0f4f63"),
            "green": ("#06182a", "#0b3b4a", "#0f5a4c"), "red": ("#0a1626", "#16294a", "#3a1f2e")}[variant]
    text = ""
    if num:
        text = ('<text x="1262" y="712" text-anchor="end" font-family="Inter, Helvetica, Arial, sans-serif" font-weight="800" '
                'font-size="440" letter-spacing="-20" fill="#ffffff" fill-opacity=".055">%s</text>' % num)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{base[0]}"/><stop offset=".62" stop-color="{base[1]}"/><stop offset="1" stop-color="{base[2]}"/></linearGradient>
<radialGradient id="a" cx=".86" cy=".08" r=".62"><stop offset="0" stop-color="{glow1[0]}" stop-opacity="{glow1[1]}"/><stop offset="1" stop-color="{glow1[0]}" stop-opacity="0"/></radialGradient>
<radialGradient id="b" cx=".04" cy=".98" r=".58"><stop offset="0" stop-color="{glow2[0]}" stop-opacity="{glow2[1]}"/><stop offset="1" stop-color="{glow2[0]}" stop-opacity="0"/></radialGradient>
<pattern id="d" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#fff" fill-opacity=".12"/></pattern>
<linearGradient id="m" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="mk"><rect width="1280" height="720" fill="url(#m)"/></mask>
</defs>
<rect width="1280" height="720" fill="url(#g)"/>
<rect width="1280" height="720" fill="url(#a)"/>
<rect width="1280" height="720" fill="url(#b)"/>
<rect width="1280" height="720" fill="url(#d)" mask="url(#mk)"/>
<g fill="none" stroke="#fff" stroke-opacity=".07" stroke-width="1.5"><circle cx="1130" cy="110" r="250"/><circle cx="1130" cy="110" r="370"/><circle cx="1130" cy="110" r="490"/></g>
{text}
</svg>
'''


def variant_of(gradient):
    if "b3382c" in gradient:
        return "red"
    if gradient.startswith("linear-gradient(135deg,#0f2b46,#2E7D32"):
        return "green"
    if "62%" in gradient:
        return "title"
    return "blue"


def process(path):
    html = path.read_text()
    # drop previous sprite so it is rebuilt
    html = re.sub(r"<!--ICON-SPRITE-->.*?<!--/ICON-SPRITE-->\s*", "", html, flags=re.S)
    USED.clear()

    # 1. emoji icons in cards
    html = re.sub(r'<div class="icon">([^<]+)</div>',
                  lambda m: chip(EMOJI_ICON[m.group(1).strip()]) if m.group(1).strip() in EMOJI_ICON else m.group(0), html)
    html = re.sub(r'<div class="big">([^<]+)</div>',
                  lambda m: chip(EMOJI_ICON[m.group(1).strip()], "lg") if m.group(1).strip() in EMOJI_ICON else m.group(0), html)
    html = html.replace('data-n="✓"', 'data-n="6"')
    html = html.replace('<div class="card stat">', '<div class="card stat">')

    # 2. card icons from titles (only where the card starts with its h3)
    def card(m):
        title = m.group(3).strip()
        icon = TITLE_ICON.get(title)
        if not icon:
            return m.group(0)
        return m.group(1) + m.group(2) + chip(icon) + m.group(4) + m.group(3) + m.group(5)
    html = re.sub(r'(<div class="card[^"]*"[^>]*>)(\s*)(<h3>)([^<]+)(</h3>)',
                  lambda m: (lambda t, ic: m.group(0) if not ic else m.group(1) + m.group(2) + chip(ic) + m.group(3) + m.group(4) + m.group(5))(m.group(4).strip(), TITLE_ICON.get(m.group(4).strip())), html)

    # 3. tile icons
    def tile(m):
        title = m.group(2).strip()
        icon = EPIC_ICON.get(title[:3]) if re.match(r"E\d\d", title) else TITLE_ICON.get(title)
        if not icon:
            return m.group(0)
        return '%s%s<div><b>%s</b><span>%s</span></div></div>' % (m.group(1), chip(icon, "sm"), m.group(2), m.group(3))
    html = re.sub(r'(<div class="tile[^"]*"[^>]*>)<b>([^<]+)</b><span>([^<]*)</span></div>', tile, html)

    # 4. dark slide backgrounds
    BG.mkdir(parents=True, exist_ok=True)

    def dark(m):
        attrs_before, gradient, attrs_after, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        variant = variant_of(gradient)
        num = ""
        c = re.search(r"Chapter (\d+)", tail)
        if c:
            num = "%02d" % int(c.group(1))
        p = re.search(r"Part (two|three)", tail)
        if p:
            num = {"two": "02", "three": "03"}[p.group(1)]
        name = "bg-%s-%s.svg" % (variant, num or "none")
        (BG / name).write_text(bg_svg(variant, num))
        return '<section class="on-dark"%sdata-background-image="assets/bg/%s" data-background-size="cover"%s>%s' % (
            attrs_before, name, attrs_after, tail)
    html = re.sub(r'<section class="on-dark"([^>]*?)data-background-gradient="([^"]+)"([^>]*)>(.{0,400})', dark, html, flags=re.S)

    # 5. logo on the first dark slide
    if "brandbar" not in html:
        html = html.replace('<div class="hero">', '<div class="hero"><div class="brandbar"><span class="logo-mark">%s</span>'
                            '<span>AI Customer Support Platform</span></div>' % ico(LOGO_ICON), 1)

    # 6. sprite right after <body> (include icons already present in the markup, not only new ones)
    USED.update(re.findall(r'<use href="#i-([\w-]+)"', html))
    html = html.replace("<body>", "<body>\n" + sprite() + "\n", 1)
    left = re.findall("[\U0001F300-\U0001FAFF☀-➿⭐✅️]", html)
    path.write_text(html)
    print("%s: icons used %d, emoji left %d" % (path.name, len(USED), len(left)))


if __name__ == "__main__":
    for d in DECKS:
        process(ROOT / d)

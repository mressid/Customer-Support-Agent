#!/usr/bin/env python3
"""Generate LaTeX chapters for the Scrum artifacts report.

Reads the Markdown docs and the rendered Mermaid PDFs, writes
  latex-scrum/chapters/p*.tex   (chapters)
  latex-scrum/figures/**.pdf    (only the diagrams actually used)

Standard library only. Run from anywhere:  python3 tools/build_chapters.py
Requires `pdfinfo` (poppler) to choose portrait or landscape per diagram.
"""
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
ROOT = OUT.parent
PACK = ROOT / "diagrams" / "mermaid"
REND = PACK / "rendered"
MMD = PACK / "mmd"
CH_DIR = OUT / "chapters"
FIG_DIR = OUT / "figures"

COUNT = [0]
USED = {}          # rel path -> (w, h, orientation)
WARN = []

# ----------------------------------------------------------------- escaping
UNI = {"→": r"\ensuremath{\rightarrow}", "↔": r"\ensuremath{\leftrightarrow}",
       "≥": r"\ensuremath{\geq}", "≤": r"\ensuremath{\leq}", "·": r"\textperiodcentered{}",
       "–": "--", "—": "---", "…": r"\ldots{}", "’": "'", "“": "``", "”": "''", "×": r"\ensuremath{\times}"}


def esc(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append(r"\textbackslash{}")
        elif ch in "&%$#_{}":
            out.append("\\" + ch)
        elif ch == "~":
            out.append(r"\textasciitilde{}")
        elif ch == "^":
            out.append(r"\textasciicircum{}")
        elif ch in UNI:
            out.append(UNI[ch])
        else:
            out.append(ch)
    s = "".join(out)
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    return s


def code(s):
    t = esc(s)
    t = t.replace(r"\_", r"\_\allowbreak{}")
    t = re.sub(r"\.(?=[A-Za-z])", r".\\allowbreak{}", t)
    t = t.replace("/", r"/\allowbreak{}")
    return r"\code{" + t + "}"


DOCREF = {
    "01-product-vision.md": "the product vision chapter", "02-module-catalog.md": "the module catalog chapter",
    "03-system-architecture.md": "the architecture chapter", "04-module-communication.md": "the communication chapter",
    "05-domain-model.md": "the domain model chapter", "06-ai-conversation-engine.md": "the AI engine chapter",
    "07-voice-and-multimodal.md": "the voice chapter", "08-integrations-and-tools.md": "the integrations chapter",
    "09-security-privacy-reliability.md": "the security chapter", "10-observability-and-evaluation.md": "the observability chapter",
    "03-ai-engine.md": "the AI engine diagrams", "02-cross-cutting-flows.md": "the cross-cutting flow diagrams",
    "04-voice-multimodal.md": "the voice diagrams",
}


def inline(s):
    stash = []

    def keep(m):
        stash.append(m.group(1))
        return "\x00%d\x00" % (len(stash) - 1)

    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\emph{\1}", s)

    def back(m):
        txt = stash[int(m.group(1))]
        if txt.endswith(".md") or "../" in txt:
            return DOCREF.get(txt.split("/")[-1], "the design reference chapters")
        return code(txt)

    return re.sub(r"\x00(\d+)\x00", back, s)


def slug(s):
    return re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")


# ----------------------------------------------------------------- headings
def clean_heading(t):
    t = t.strip()
    t = re.sub(r"^(?:U)?\d+\s+[—-]\s+", "", t)         # "01 — Title", "U1 — Title"
    t = re.sub(r"^(?:U\d+\.\d+|\d+(?:\.\d+)+)\s+(?=\S)", "", t)   # "2.5 Title", "U1.1 Title"
    t = re.sub(r"^\d+\.\s+(?=\S)", "", t)              # "1. Title"
    return t


LEVELS = ["chapter", "section", "subsection", "subsubsection", "paragraph"]

# ----------------------------------------------------------------- figures
def pdf_size(pdf):
    try:
        o = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
        m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", o)
        return float(m.group(1)), float(m.group(2))
    except Exception:
        return 600.0, 400.0


def choose(w, h):
    sp = min(470 / w, 600 / h, 1.0)
    sl = min(690 / w, 420 / h, 1.0)
    orient = "L" if (sp < 0.72 and sl > sp * 1.25) else "P"
    return orient, (sl if orient == "L" else sp)


def figure_tex(rel, caption):
    pdf = REND / (rel + ".pdf")
    if not pdf.exists():
        WARN.append("missing pdf " + rel)
        return "%% missing figure %s\n" % rel
    w, h = pdf_size(pdf)
    orient, scale = choose(w, h)
    USED[rel] = (w, h, orient, scale)
    cmd = r"\mmdfigL" if orient == "L" else r"\mmdfig"
    COUNT[0] += 1
    return "%s{%s}{%s}{fig:%s-%d}\n\n" % (cmd, rel, inline(caption), slug(rel)[-50:], COUNT[0])


def mmd_files(folder):
    d = MMD / folder
    return sorted(d.glob("*.mmd"))


def mm(folder, idx, cap=None):
    """Reference diagram number idx (1-based) of an mmd folder."""
    files = mmd_files(folder)
    f = files[idx - 1]
    if cap is None:
        first = f.read_text().splitlines()[0]
        cap = clean_heading(first.split(" - ", 1)[-1])
    return (str(f.relative_to(MMD).with_suffix("")), cap)


def figs_tex(items):
    return "".join(figure_tex(rel, cap) for rel, cap in items)


# ----------------------------------------------------------------- backlog data
def parse_backlog():
    txt = (ROOT / "scrum" / "01-epics-and-backlog.md").read_text()
    epics, stories, cur = {}, {}, None
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^## Epic (E\d+) — (.*)", ln)
        if m:
            cur = m.group(1)
            epics[cur] = {"title": m.group(2).strip(), "goal": "", "stories": []}
        elif cur and ln.startswith("**Goal:**"):
            epics[cur]["goal"] = ln.replace("**Goal:**", "").strip()
        m = re.match(r"^- \*\*(US-\d+)\*\* (.*)", ln)
        if m and cur:
            sid, stmt, acc = m.group(1), m.group(2).strip(), ""
            j = i + 1
            while j < len(lines) and lines[j].startswith("  "):
                a = re.match(r"\s+- Acceptance:\s*(.*)", lines[j])
                if a:
                    acc = a.group(1).strip()
                j += 1
            stories[sid] = {"epic": cur, "story": stmt, "acc": acc}
            epics[cur]["stories"].append(sid)
        i += 1
    order = []
    for ln in lines:
        m = re.match(r"^\d+\. (E\d+) ", ln)
        if m:
            order.append(m.group(1))
    return epics, stories, order


EPICS, STORIES, ORDER = parse_backlog()
SPRINT = {}
for s, ids in {
    "S1": "001 003 010 011", "S2": "020 021 022 013", "S3": "030 031 032", "S4": "040 033 041 042",
    "S5": "050 051 053 060 061 062", "S6": "070 071 043 110 112", "S7": "080 081", "S8": "082 083 084",
}.items():
    for n in ids.split():
        SPRINT["US-" + n] = s
RELEASE = {"E01": "R1", "E02": "R1", "E03": "R1", "E04": "R1", "E05": "R1", "E06": "R1", "E07": "R1",
           "E08": "R1", "E09": "R2", "E10": "R3", "E11": "R3", "E12": "R1/R3"}


def table_tex(header, rows, widths, small=True):
    n = len(header)
    spec = "".join(
        r">{\raggedright\arraybackslash}p{\dimexpr%.3f\linewidth-2\tabcolsep\relax}" % w for w in widths)
    o = ["{\\small" if small else "{", "\\begin{longtable}{@{}%s@{}}" % spec, "\\toprule",
         " & ".join(r"\textbf{%s}" % esc(h) for h in header) + r" \\", "\\midrule", "\\endhead",
         "\\bottomrule", "\\endfoot"]
    for r in rows:
        o.append(" & ".join(c.replace("\x01", "") for c in r) + r" \\")
    o += ["\\end{longtable}", "}", ""]
    return "\n".join(o)


# ----------------------------------------------------------------- md -> tex
def convert(path, shift=0, drop_intro=False, pack=False, epic=None, after_intro="", inserts=None,
            append=None, caption_prefix=""):
    inserts = inserts or {}
    append = append or []
    md = pathlib.Path(path).read_text()
    lines = md.splitlines()
    out = []
    pending = []             # figures waiting for next heading
    h2 = h3 = ""
    seen_h2 = False
    in_intro = True          # before first level-2 heading
    first_h1 = True
    fig_idx = 0
    mdfigs = []
    if pack:
        folder = pathlib.Path(path).resolve().relative_to(PACK).with_suffix("")
        mdfigs = mmd_files(folder)
    stack = []               # open lists: (indent, env)
    para = []
    i = 0

    def flush_para():
        nonlocal para
        if para:
            out.append(" ".join(para) + "\n")
            para = []

    def close_lists(to=0):
        while len(stack) > to:
            _, env = stack.pop()
            out.append("\\end{%s}" % env)
        if to == 0 and not stack:
            pass

    def flush_pending():
        nonlocal pending
        if pending:
            out.append(figs_tex(pending))
            pending = []

    while i < len(lines):
        ln = lines[i]

        # code fence
        m = re.match(r"^```(\w*)\s*$", ln)
        if m:
            lang = m.group(1)
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].startswith("```"):
                body.append(lines[j])
                j += 1
            i = j + 1
            flush_para()
            close_lists()
            if lang == "mermaid":
                if pack:
                    if fig_idx >= len(mdfigs):
                        WARN.append("%s: more blocks than mmd files" % path)
                    else:
                        f = mdfigs[fig_idx]
                        rel = str(f.relative_to(MMD).with_suffix(""))
                        cap = ": ".join(x for x in [caption_prefix, h2, h3] if x) or clean_heading(first_h1 or "")
                        out.append(figure_tex(rel, cap))
                    fig_idx += 1
            else:
                out.append("\\begin{lstlisting}\n" + "\n".join(body) + "\n\\end{lstlisting}\n")
            continue

        # heading
        m = re.match(r"^(#{1,5})\s+(.*)", ln)
        if m:
            flush_para()
            close_lists()
            lvl = len(m.group(1))
            raw = m.group(2).strip()
            text = clean_heading(raw)
            if lvl == 1 and drop_intro:
                first_h1 = raw
                i += 1
                continue
            if lvl == 1:
                first_h1 = text
            flush_pending()
            if lvl == 2 and not seen_h2:
                seen_h2 = True
                in_intro = False
                if after_intro:
                    out.append(after_intro)
            elif lvl == 2:
                seen_h2 = True
            if lvl == 2:
                h2, h3 = text, ""
            elif lvl == 3:
                h3 = text
            eff = min(lvl - 1 + shift, 4)
            out.append("\\%s{%s}\n" % (LEVELS[eff], inline(text)))
            for key, figs in inserts.items():
                if lvl >= 2 and text.startswith(key):
                    pending = list(figs)
            # story card
            sm = re.match(r"^(US-\d+)", text)
            if epic and sm and sm.group(1) in STORIES:
                st = STORIES[sm.group(1)]
                out.append("\\begin{storybox}{User story %s}\n\\textbf{Story.} %s\\par\n\\textbf{Acceptance.} %s\n\\end{storybox}\n"
                           % (sm.group(1), inline(st["story"]), inline(st["acc"])))
            i += 1
            continue

        if drop_intro and in_intro:
            i += 1
            continue

        if epic and ln.strip().startswith("Acceptance:"):
            i += 1
            continue

        # table
        if ln.startswith("|"):
            flush_para()
            close_lists()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            header, body = rows[0], rows[2:]
            lens = [max(len(header[k]), *(len(r[k]) for r in body)) if body else len(header[k]) for k in range(len(header))]
            lens = [min(max(l, 8), 60) for l in lens]
            tot = float(sum(lens))
            widths = [l / tot for l in lens]
            body = [["\x01" + inline(c) for c in r] for r in body]
            out.append(table_tex(header, body, widths))
            continue

        # list item
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", ln)
        if m:
            flush_para()
            indent = len(m.group(1))
            env = "enumerate" if m.group(2)[0].isdigit() else "itemize"
            while stack and indent < stack[-1][0]:
                _, e = stack.pop()
                out.append("\\end{%s}" % e)
            if not stack or indent > stack[-1][0]:
                stack.append((indent, env))
                out.append("\\begin{%s}" % env)
            elif stack[-1][1] != env:
                _, e = stack.pop()
                out.append("\\end{%s}" % e)
                stack.append((indent, env))
                out.append("\\begin{%s}" % env)
            txt = m.group(3)
            out.append("\\item " + inline(txt.rstrip()))
            i += 1
            continue

        # blank
        if not ln.strip():
            flush_para()
            i += 1
            continue

        # continuation inside list
        if stack and ln.startswith("  "):
            out[-1] = out[-1] + " " + inline(ln.strip())
            i += 1
            continue

        close_lists()
        text = inline(ln.strip())
        if ln.endswith("  ") and i + 1 < len(lines) and lines[i + 1].strip():
            text += r" \\"
        para.append(text)
        i += 1

    flush_para()
    close_lists()
    flush_pending()
    out.append(figs_tex(append))
    return "\n".join(keep_with_figure(out)) + "\n"



HEAD_RE = re.compile(r"\\(section|subsection|subsubsection)\{")


def keep_with_figure(items):
    """Move headings (and story cards) onto the landscape page of the figure that follows,
    or reserve space before them for a portrait figure, so a heading is never stranded."""
    flat = []
    for it in items:
        flat.extend(x for x in re.split(r"(?=^\\mmdfigL?\{)", it, flags=re.M) if x.strip())
    res = []
    for it in flat:
        land = it.startswith("\\mmdfigL{")
        port = it.startswith("\\mmdfig{")
        if land or port:
            pre = []
            while res and (HEAD_RE.match(res[-1]) or res[-1].startswith("\\begin{storybox}")):
                pre.insert(0, res.pop())
            if land and pre:
                it = "\\mmdfigLH{" + "\n".join(pre) + "}" + it[len("\\mmdfigL"):]
            elif pre:
                rel = it[len("\\mmdfig{"):].split("}", 1)[0]
                w, h, orient, scale = USED.get(rel, (600, 400, "P", 1.0))
                need = int(h * scale) + 60 + (90 if any(x.startswith("\\begin{storybox}") for x in pre) else 0)
                res.append("\\Needspace{%dpt}" % min(need, 640))
                res.extend(pre)
            else:
                pass
        res.append(it)
    return res


def write(name, text):
    CH_DIR.mkdir(parents=True, exist_ok=True)
    (CH_DIR / name).write_text(text)


def md(rel):
    return ROOT / rel


def pack_md(rel):
    return PACK / rel


# ----------------------------------------------------------------- chapters
def build():
    # ===== Part I
    write("p1-01-product-vision.tex",
          convert(md("01-product-vision.md"), append=[mm("01-architecture", 1, "System context"),
                                                      mm("scrum-existing/S5-scrum-mermaid-artifacts", 1, "Product roadmap")]))

    charter = convert(md("scrum/00-scrum-charter.md"),
                      inserts={"Scrum setup": [mm("07-scrum-release-risks", 1, "Scrum roles and accountabilities")],
                               "Sprint approach": [mm("07-scrum-release-risks", 2, "Scrum events within a Sprint"),
                                                   mm("scrum-existing/S5-scrum-mermaid-artifacts", 4, "Scrum workflow")]})
    events = convert(md("scrum/04-events-and-ceremonies.md"), shift=1)
    write("p1-02-scrum-charter.tex", charter + "\n" + events)

    # backlog overview (generated from the parsed backlog)
    o = ["\\chapter{Product Backlog Overview}", "",
         "The Product Backlog is an ordered list of everything needed to reach the Product Goal. It is emergent: this is a starter backlog, not a commitment. IDs are stable references for planning. Story points are team-specific estimates and are shown as TBD until the team estimates them.", "",
         "\\section{Epics}"]
    rows = []
    for e, d in EPICS.items():
        rows.append([e, inline(d["title"]), inline(d["goal"]), str(len(d["stories"])), RELEASE.get(e, "")])
    o.append(table_tex(["Epic", "Title", "Goal", "Stories", "Release"],
                       [["\x01" + c for c in r] for r in rows], [0.07, 0.24, 0.51, 0.08, 0.10]))
    o.append("\\section{Suggested order of work}")
    o.append("\\begin{enumerate}")
    for e in ORDER:
        o.append("\\item %s %s" % (e, inline("— " + EPICS[e]["title"])))
    o.append("\\end{enumerate}")
    o.append("Reorder based on user research, risk, technical dependencies and Sprint Review feedback.")
    o.append(figs_tex([mm("scrum-existing/S5-scrum-mermaid-artifacts", 2, "Epic dependency graph"),
                       mm("07-scrum-release-risks", 11, "Epic delivery map by release"),
                       mm("scrum-existing/S5-scrum-mermaid-artifacts", 8, "Module-to-epic coverage"),
                       mm("scrum-existing/S5-scrum-mermaid-artifacts", 5, "User story lifecycle")]))
    o.append("\\begin{lscapepage}")
    o.append("\\section{Full Product Backlog}")
    o.append("Sprint column shows the provisional assignment from the Sprint plan; ``Backlog'' means not yet scheduled.")
    brow = []
    for sid, s in STORIES.items():
        brow.append([sid, s["epic"], inline(s["story"]), inline(s["acc"]), SPRINT.get(sid, "Backlog"), "TBD"])
    o.append(table_tex(["ID", "Epic", "User story", "Acceptance criteria", "Sprint", "Points"],
                       [["\x01" + c for c in r] for r in brow], [0.07, 0.06, 0.34, 0.35, 0.09, 0.09]))
    o.append("\\end{lscapepage}")
    write("p1-03-backlog-overview.tex", "\n".join(o) + "\n")

    # ===== Part II epics
    for f in sorted((PACK / "epics").glob("E*.md")):
        code_ = f.name.split("-")[0]
        d = EPICS[code_]
        rows = [[sid, inline(STORIES[sid]["story"]), SPRINT.get(sid, "Backlog")] for sid in d["stories"]]
        intro = ("\\section*{Stories in this epic}\n" +
                 table_tex(["ID", "User story", "Sprint"], [["\x01" + c for c in r] for r in rows], [0.09, 0.78, 0.13]))
        write("p2-%s.tex" % code_, convert(f, pack=True, epic=code_, caption_prefix=code_, after_intro=intro))

    # ===== Part III
    rel = convert(md("scrum/06-release-goals-and-risks.md"), pack=False,
                  inserts={"R1 —": [mm("07-scrum-release-risks", 5, "Release 1 exit criteria")],
                           "R2 —": [mm("07-scrum-release-risks", 6, "Release 2 exit criteria")],
                           "Initial risks": [mm("07-scrum-release-risks", 8, "Risk map")],
                           "Architecture decision records": [mm("07-scrum-release-risks", 9, "ADR dependency order")],
                           "Decisions not to make": [mm("07-scrum-release-risks", 10, "Decisions to defer")]},
                  append=[mm("07-scrum-release-risks", 7, "Rollout and rollback"),
                          mm("scrum-existing/S5-scrum-mermaid-artifacts", 6, "Release acceptance flow")])
    write("p3-01-release-plan.tex", rel)

    sprint_ins = {}
    for n in range(9):
        sprint_ins["Sprint %d" % n] = [mm("06-sprints", 4 + n, "Sprint %d detail" % n)]
    spr = convert(md("scrum/02-sprint-plan.md"),
                  after_intro=figs_tex([mm("06-sprints", 1, "Sprint sequence and goals"),
                                        mm("06-sprints", 2, "What the demo can show after each Sprint"),
                                        mm("06-sprints", 3, "Provisional timeline (placeholder dates)")]),
                  inserts=sprint_ins,
                  append=[mm("06-sprints", 13, "Story-to-Sprint traceability"),
                          mm("scrum-existing/S5-scrum-mermaid-artifacts", 7, "Sprint Review demo path for the Text MVP")])
    write("p3-02-sprint-plan.tex", spr)

    dod = convert(md("scrum/03-definition-of-ready-done.md"),
                  inserts={"Definition of Ready": [mm("07-scrum-release-risks", 3, "Definition of Ready check")]},
                  append=[mm("07-scrum-release-risks", 4, "Definition of Done layers")])
    write("p3-03-dor-dod.tex", dod)

    # ===== Part IV
    arch = convert(md("03-system-architecture.md"))
    arch += convert(pack_md("01-architecture.md"), shift=0, pack=True, drop_intro=True)
    write("p4-01-architecture.tex", arch)
    write("p4-02-module-catalog.tex", convert(md("02-module-catalog.md")))
    comm = convert(md("04-module-communication.md"))
    comm += "\\section{Cross-cutting flow diagrams}\n" + convert(pack_md("02-cross-cutting-flows.md"), shift=1, pack=True, drop_intro=True)
    write("p4-03-communication.tex", comm)
    dom = convert(md("05-domain-model.md"))
    dom += "\\section{Data model diagrams}\n" + convert(pack_md("05-data-model.md"), shift=1, pack=True, drop_intro=True)
    write("p4-04-domain-model.tex", dom)
    ai = convert(md("06-ai-conversation-engine.md"))
    ai += "\\section{AI engine diagrams}\n" + convert(pack_md("03-ai-engine.md"), shift=1, pack=True, drop_intro=True)
    write("p4-05-ai-engine.tex", ai)
    vo = convert(md("07-voice-and-multimodal.md"))
    vo += "\\section{Voice and multimodal diagrams}\n" + convert(pack_md("04-voice-multimodal.md"), shift=1, pack=True, drop_intro=True)
    write("p4-06-voice.tex", vo)
    write("p4-07-integrations.tex", convert(md("08-integrations-and-tools.md"),
                                            append=[mm("epics/E06-safe-business-tools", 2, "Three-layer connector architecture")]))
    write("p4-08-security.tex", convert(md("09-security-privacy-reliability.md")))
    write("p4-09-observability.tex", convert(md("10-observability-and-evaluation.md")))

    # ===== Part V UML
    for f in sorted((PACK / "uml").glob("U*.md")):
        write("p5-%s.tex" % f.name.split("-")[0], convert(f, pack=True))


def finish():
    # copy used figures
    if FIG_DIR.exists():
        shutil.rmtree(FIG_DIR)
    for rel in USED:
        dst = FIG_DIR / (rel + ".pdf")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REND / (rel + ".pdf"), dst)
    L = [r for r, v in USED.items() if v[2] == "L"]
    small = sorted([(v[3], r) for r, v in USED.items() if v[3] < 0.5])
    print("figures used: %d (landscape %d)" % (len(USED), len(L)))
    print("figures with scale < 0.50 (may be hard to read):", len(small))
    for sc, r in small:
        print("  %.2f %s" % (sc, r))
    for w in WARN:
        print("WARN", w)


if __name__ == "__main__":
    build()
    finish()

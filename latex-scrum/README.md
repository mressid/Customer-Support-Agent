# Scrum Artifacts - LaTeX project (Overleaf ready)

## Use on Overleaf

1. Upload `latex-scrum-overleaf.zip` (in the parent folder) with **New Project > Upload Project**. It contains `main.tex`, `preamble.tex`, `chapters/`, `figures/` and this README. A compiled preview is in `build/Scrum-Artifacts-preview.pdf`.
2. Menu > **Main document**: `main.tex`. **Compiler**: pdfLaTeX (default). No special fonts or shell escape needed.
3. Edit the title-page placeholders at the top of `main.tex` (`\TeamName`, `\ProductOwner`, `\ScrumMaster`, `\Developers`, `\Institution`, `\DocVersion`).

A local compile pass takes about 6 seconds (273 pages, 205 diagrams). If Overleaf ever shows a timeout on the first compile, use **Recompile from scratch** once.

## Layout

```
main.tex            document structure and metadata
preamble.tex        packages and macros (\mmdfig, \mmdfigL, storybox, \code)
chapters/           00-frontmatter.tex is hand-written; p*.tex are generated
figures/            rendered diagram PDFs (same tree as diagrams/mermaid/rendered)
tools/              build_chapters.py (regenerates chapters and copies figures)
```

Parts: I Product and Scrum framework, II Epics and user stories, III Release and sprint planning, IV Architecture and design reference, V UML models.

## Regenerate after changing the Markdown or diagrams (local only)

```bash
# 1. edit diagrams/mermaid/**/*.md, then from diagrams/mermaid/:
#      python3 tools/extract_mmd.py .        # md -> mmd/
#      tools/render_all.sh                   # mmd -> rendered/*.pdf, *.svg (needs mmdc and Chrome)
# 2. rebuild the LaTeX chapters and figure folder
python3 latex-scrum/tools/build_chapters.py
# 3. compile locally (optional)
cd latex-scrum && latexmk -pdf main.tex
```

`build_chapters.py` needs Python 3 and `pdfinfo` (poppler-utils). It decides per diagram whether to use a portrait figure or a landscape page.

## Rendering diagrams (one-time, local)

Diagrams are rendered with the Mermaid CLI (`@mermaid-js/mermaid-cli`, `mmdc`) using Chrome, e.g.

```bash
npm i -g @mermaid-js/mermaid-cli
cd diagrams/mermaid && tools/render_all.sh      # use --missing to render only new diagrams
```

Settings live in `diagrams/mermaid/tools/` (`mermaid.json` compact layout, `mermaid-class.json` fallback for class diagrams, `puppeteer.json` for the Chrome path).

The PDFs and SVGs are already saved in `diagrams/mermaid/rendered/`.

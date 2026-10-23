# Presentations (reveal.js)

Three decks, a launcher, and PDF handouts. Everything is local: no CDN, no server needed.

| File | Audience | Size |
|---|---|---|
| `index.html` | launcher | |
| `scrum.html` | team and stakeholders | 28 slides |
| `product.html` | everyone | 12 chapters, 75 slides (includes an Integrations and tools chapter) |
| `engineering.html` | developers | 6 chapters, 28 slides |
| `pdf/*.pdf` | handouts | one page per slide, no animation |

## Open

Double-click `index.html` (or any deck) in Chrome, Edge, Firefox or Safari.

## Keys

`→` `←` next/previous · `↓` `↑` details inside a chapter · `Esc` overview map · `S` speaker notes (second window) · `F` full screen · `I` back to the presentations list · `?` all shortcuts · click a diagram to enlarge (click again or `Esc` to close) · `Alt`+click zoom.

`product.html` and `engineering.html` use vertical stacks: chapters run left to right, details run top to bottom.

## Look

Flat design, no drop shadows. Inter and JetBrains Mono are bundled in `vendor/fonts/`. Icons are Lucide line icons inlined as an SVG sprite. Dark slides use generated background art in `assets/bg/`.

## Maintain

```bash
# after re-rendering diagrams (diagrams/mermaid/tools/render_all.sh):
python3 presentations/tools/copy_assets.py     # refresh assets/*.svg from rendered diagrams
python3 presentations/tools/apply_icons.py     # icons, chips, backgrounds (safe to re-run)
```

To export PDFs, open a deck with `?print-pdf` appended (for example `scrum.html?print-pdf`) and print to PDF with background graphics on, margins none, paper 1280x720.

Add a card icon: put the title in `TITLE_ICON` in `tools/apply_icons.py` and copy the Lucide SVG into `assets/icons/`.

## Licenses

reveal.js MIT (`vendor/reveal/LICENSE`) · Lucide icons ISC (`assets/icons/LICENSE.txt`) · Inter and JetBrains Mono SIL OFL (`vendor/fonts/LICENSE-*.txt`).

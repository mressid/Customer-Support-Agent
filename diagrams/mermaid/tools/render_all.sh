#!/usr/bin/env bash
# Render every .mmd under diagrams/mermaid/mmd to PDF (for LaTeX) and SVG.
# Needs the Mermaid CLI: npm i -g @mermaid-js/mermaid-cli   (or set MMDC to its path)
# Class diagrams that fail with the compact config are retried with tools/mermaid-class.json.
# Edit tools/puppeteer.json if Chrome/Chromium is not at /usr/bin/google-chrome-stable.
# Usage: tools/render_all.sh            render everything
#        tools/render_all.sh --missing  render only diagrams without a PDF and SVG yet
set -euo pipefail
cd "$(dirname "$0")/.."
MMDC="${MMDC:-mmdc}"
JOBS="${JOBS:-6}"

render_one() {
  local f="$1" rel base ext
  rel="${f#mmd/}"; base="rendered/${rel%.mmd}"
  mkdir -p "$(dirname "$base")"
  for ext in pdf svg; do
    local extra=(); [ "$ext" = pdf ] && extra=(--pdfFit)
    "$MMDC" -i "$f" -o "$base.$ext" -p tools/puppeteer.json -c tools/mermaid.json -q "${extra[@]}" >/dev/null 2>&1 \
      || { grep -q '^classDiagram' "$f" \
           && "$MMDC" -i "$f" -o "$base.$ext" -p tools/puppeteer.json -c tools/mermaid-class.json -q "${extra[@]}" >/dev/null 2>&1; } \
      || echo "FAIL $f ($ext)"
  done
}
export -f render_one; export MMDC

list=$(find mmd -name '*.mmd' | sort)
if [ "${1:-}" = "--missing" ]; then
  list=$(for f in $list; do b="rendered/${f#mmd/}"; b="${b%.mmd}"; [ -s "$b.pdf" ] && [ -s "$b.svg" ] || echo "$f"; done)
fi
echo "$list" | xargs -P "$JOBS" -I{} bash -c 'render_one {}'
echo "done: $(find rendered -name '*.pdf' | wc -l) pdf, $(find rendered -name '*.svg' | wc -l) svg"

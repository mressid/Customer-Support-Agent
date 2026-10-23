#!/usr/bin/env python3
"""Cache-busting for the deck's shared CSS and JS.

GitHub Pages serves css/theme.css and js/deck.js with a multi-hour cache, so after an edit
visitors can keep seeing the old files. This script appends ?v=<hash of both files> to the
references in every page, so the URL changes whenever the content does.

Run after editing css/theme.css or js/deck.js:   python3 docs/tools/bump_assets.py
"""
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = ["css/theme.css", "js/deck.js"]

digest = hashlib.sha1(b"".join((ROOT / f).read_bytes() for f in FILES)).hexdigest()[:8]
changed = 0
for page in sorted(ROOT.glob("*.html")):
    text = page.read_text()
    new = text
    for f in FILES:
        new = re.sub(r'(%s)(\?v=[0-9a-f]+)?(?=")' % re.escape(f), r"\1?v=" + digest, new)
    if new != text:
        page.write_text(new)
        changed += 1
print("version", digest, "- updated", changed, "page(s)")

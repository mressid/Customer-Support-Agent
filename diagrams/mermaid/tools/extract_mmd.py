import re, sys, pathlib
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve(); out = root / "mmd"
def slug(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:60].strip("-") or "diagram"
n = 0
for md in sorted(root.rglob("*.md")):
    if "mmd" in md.relative_to(root).parts or md.name == "00-index.md": continue
    rel = md.relative_to(root)
    folder = out / rel.parent / md.stem
    heading, count, in_block, buf = md.stem, 0, False, []
    for line in md.read_text().splitlines():
        if not in_block:
            m = re.match(r"^(#{2,4})\s+(.*)", line)
            if m: heading = m.group(2)
            if line.strip() == "```mermaid": in_block, buf = True, []
        elif line.strip() == "```":
            in_block = False; count += 1; n += 1
            folder.mkdir(parents=True, exist_ok=True)
            f = folder / f"{count:02d}-{slug(heading)}.mmd"
            f.write_text(f"%% Source: {rel} - {heading}\n" + "\n".join(buf) + "\n")
        else: buf.append(line)
print("wrote", n)

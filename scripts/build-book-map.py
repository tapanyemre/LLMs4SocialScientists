#!/usr/bin/env python3
"""Regenerate the link-network data inside book-map.qmd.

Parses every chapter listed in _quarto-full.yml for internal references
(@sec- crossrefs and residual .qmd links), builds a node/edge graph, and
rewrites the JSON between the BOOK-MAP-DATA markers in book-map.qmd.

Run from the book root after adding chapters or links:

    python3 scripts/build-book-map.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FULL_CONFIG = ROOT / "_quarto-full.yml"
MAP_PAGE = ROOT / "book-map.qmd"

SKIP = {"index.qmd", "roadmap.qmd", "references.qmd", "book-map.qmd"}


def parse_config():
    """Yield (part_title, chapter_path) from _quarto-full.yml, in order."""
    part = "Front matter"
    for line in FULL_CONFIG.read_text().splitlines():
        m_part = re.match(r'\s*-\s*part:\s*"?([^"]+?)"?\s*$', line)
        if m_part:
            part = m_part.group(1)
            continue
        m_ch = re.match(r"\s*-\s*([\w./-]+\.qmd)\s*$", line)
        if m_ch and m_ch.group(1) not in SKIP:
            yield part, m_ch.group(1)


def main():
    chapters = list(parse_config())
    if not chapters:
        sys.exit("No chapters found in _quarto-full.yml")

    anchor_of, node_of = {}, {}
    nodes = []
    for part, path in chapters:
        text = (ROOT / path).read_text()
        m = re.search(r"^#\s+(.+?)\s*\{#(sec-[\w-]+)\}", text, re.M)
        if not m:
            print(f"  ! no {{#sec-...}} anchor in {path}, skipped")
            continue
        title, anchor = m.group(1), m.group(2)
        status_m = re.search(r"Status:\s*`(\w+)`", text)
        node = {
            "id": anchor,
            "title": title,
            "part": part,
            "status": status_m.group(1) if status_m else "drafted",
            "href": path.replace(".qmd", ".html"),
        }
        anchor_of[path] = anchor
        node_of[anchor] = node
        nodes.append(node)

    edges = {}
    for part, path in chapters:
        src = anchor_of.get(path)
        if not src:
            continue
        text = (ROOT / path).read_text()
        # strip code blocks so code comments never count as references
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        targets = set(re.findall(r"@(sec-[\w-]+)", text))
        for link in re.findall(r"\]\(([\w./-]+\.qmd)[#)]", text):
            resolved = (ROOT / path).parent.joinpath(link).resolve()
            try:
                rel = str(resolved.relative_to(ROOT))
            except ValueError:
                continue
            if rel in anchor_of:
                targets.add(anchor_of[rel])
        targets.discard(src)
        for t in targets:
            if t in node_of:
                edges[(src, t)] = edges.get((src, t), 0) + 1

    data = {
        "nodes": nodes,
        "links": [{"source": s, "target": t} for (s, t) in sorted(edges)],
    }

    page = MAP_PAGE.read_text()
    new_block = (
        "// BOOK-MAP-DATA-START\n"
        f"window.BOOK_MAP = {json.dumps(data, indent=1)};\n"
        "// BOOK-MAP-DATA-END"
    )
    page, n = re.subn(
        r"// BOOK-MAP-DATA-START.*?// BOOK-MAP-DATA-END",
        new_block.replace("\\", "\\\\"),
        page,
        flags=re.S,
    )
    if n != 1:
        sys.exit("Could not find BOOK-MAP-DATA markers in book-map.qmd")
    MAP_PAGE.write_text(page)
    print(f"book-map.qmd updated: {len(nodes)} chapters, {len(data['links'])} links")


if __name__ == "__main__":
    main()

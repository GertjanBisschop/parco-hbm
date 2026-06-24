#!/usr/bin/env python3
"""Rewrite WIDOCO PEH term fragments to stable local-name anchors."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


ID_PATTERN = re.compile(r'id="(?P<iri>https://w3id\.org/peh/terms/(?P<local>[^"#]+))"')
HREF_PATTERN = re.compile(r'href="#(?P<iri>https://w3id\.org/peh/terms/(?P<local>[^"#]+))"')
ANY_ID_PATTERN = re.compile(r'id="(?P<id>[^"]+)"')


def find_anchor_collisions(html: str) -> list[str]:
    ids = [match.group("id") for match in ANY_ID_PATTERN.finditer(html)]
    rewritten_ids = {
        match.group("iri"): match.group("local")
        for match in ID_PATTERN.finditer(html)
    }
    unchanged_ids = set(ids) - set(rewritten_ids)
    candidate_counts = Counter(rewritten_ids.values())

    collisions = [local for local, count in candidate_counts.items() if count > 1]
    collisions.extend(local for local in candidate_counts if local in unchanged_ids)
    return sorted(set(collisions))


def rewrite_html(path: Path) -> int:
    html = path.read_text()
    collisions = find_anchor_collisions(html)
    if collisions:
        joined = ", ".join(collisions)
        raise ValueError(f"{path}: local anchor collision after rewrite: {joined}")

    html, id_count = ID_PATTERN.subn(lambda match: f'id="{match.group("local")}"', html)
    html, href_count = HREF_PATTERN.subn(lambda match: f'href="#{match.group("local")}"', html)

    if 'id="https://w3id.org/peh/terms/' in html or 'href="#https://w3id.org/peh/terms/' in html:
        raise ValueError(f"{path}: PEH term fragment rewrite was incomplete")

    path.write_text(html)
    return id_count + href_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", type=Path)
    args = parser.parse_args()

    total = 0
    for path in sorted(args.site_dir.glob("*.html")):
        total += rewrite_html(path)
    index_en = args.site_dir / "index-en.html"
    if index_en.exists():
        (args.site_dir / "index.html").write_text(index_en.read_text())
    print(f"Rewrote {total} PEH term fragment anchors in {args.site_dir}.")


if __name__ == "__main__":
    main()

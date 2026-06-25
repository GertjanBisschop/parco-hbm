#!/usr/bin/env python3
"""Rewrite WIDOCO PEH term fragments to stable local-name anchors."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from html import escape
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import RDFS, SKOS


ID_PATTERN = re.compile(r'id="(?P<iri>https://w3id\.org/peh/terms/(?P<local>[^"#]+))"')
HREF_PATTERN = re.compile(r'href="#(?P<iri>https://w3id\.org/peh/terms/(?P<local>[^"#]+))"')
ANY_ID_PATTERN = re.compile(r'id="(?P<id>[^"]+)"')
ALSO_DEFINED_AS_NAMED_INDIVIDUAL_PATTERN = re.compile(
    r'\n?\s*<dt>\s*is also defined as\s*</dt>\s*'
    r'<dd>\s*<a href="#[^"]+">named individual</a>\s*</dd>',
    re.IGNORECASE,
)
INJECTED_DESCRIPTION_PATTERN = re.compile(
    r'\n\s*<p class="widoco-term-description" data-widoco-description="true">.*?</p>',
    re.DOTALL,
)
ENTITY_IRI_PATTERN = re.compile(
    r'(?P<header><div class="entity" id="[^"]+">\s*'
    r'<h3>.*?</h3>\s*'
    r'<p><strong>IRI:</strong>\s*(?P<iri>[^<]+)</p>)',
    re.DOTALL,
)


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


def load_term_descriptions(site_dir: Path) -> dict[str, str]:
    ontology_path = site_dir / "ontology.ttl"
    if not ontology_path.exists():
        return {}

    graph = Graph().parse(ontology_path, format="turtle")
    descriptions: dict[str, str] = {}
    for subject in set(graph.subjects()):
        description = next(graph.objects(subject, RDFS.comment), None)
        if description is None:
            description = next(graph.objects(subject, SKOS.definition), None)
        if description is not None:
            descriptions[str(subject)] = str(description)
    return descriptions


def inject_term_descriptions(html: str, descriptions: dict[str, str]) -> tuple[str, int]:
    html = INJECTED_DESCRIPTION_PATTERN.sub("", html)

    def replace(match: re.Match[str]) -> str:
        iri = match.group("iri").strip()
        description = descriptions.get(iri)
        if not description:
            return match.group("header")
        escaped_description = escape(description, quote=False)
        return (
            f'{match.group("header")}\n'
            f'  <p class="widoco-term-description" data-widoco-description="true">'
            f"{escaped_description}</p>"
        )

    return ENTITY_IRI_PATTERN.subn(replace, html)


def rewrite_html(path: Path, descriptions: dict[str, str]) -> int:
    html = path.read_text()
    collisions = find_anchor_collisions(html)
    if collisions:
        joined = ", ".join(collisions)
        raise ValueError(f"{path}: local anchor collision after rewrite: {joined}")

    html, id_count = ID_PATTERN.subn(lambda match: f'id="{match.group("local")}"', html)
    html, href_count = HREF_PATTERN.subn(lambda match: f'href="#{match.group("local")}"', html)
    html, individual_crossref_count = ALSO_DEFINED_AS_NAMED_INDIVIDUAL_PATTERN.subn("", html)
    html, description_count = inject_term_descriptions(html, descriptions)

    if 'id="https://w3id.org/peh/terms/' in html or 'href="#https://w3id.org/peh/terms/' in html:
        raise ValueError(f"{path}: PEH term fragment rewrite was incomplete")

    path.write_text(html)
    return id_count + href_count + individual_crossref_count + description_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", type=Path)
    args = parser.parse_args()

    total = 0
    descriptions = load_term_descriptions(args.site_dir)
    for path in sorted(args.site_dir.glob("*.html")):
        total += rewrite_html(path, descriptions)
    index_en = args.site_dir / "index-en.html"
    if index_en.exists():
        (args.site_dir / "index.html").write_text(index_en.read_text())
    print(f"Applied {total} WIDOCO HTML postprocess rewrites in {args.site_dir}.")


if __name__ == "__main__":
    main()

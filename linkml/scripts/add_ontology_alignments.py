#!/usr/bin/env python3
"""Add PEH ontology alignment axioms to generated RDF graphs."""

from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL


IOP = Namespace("https://w3id.org/iadopt/ont/")
PEHTERMS = Namespace("https://w3id.org/peh/terms/")

CLASS_EQUIVALENCES = (
    (PEHTERMS.Indicator, IOP.Variable),
)

ALIGNMENT_COMMENT = "# PEH ontology alignment axioms"


def bind_alignment_prefixes(graph: Graph) -> None:
    graph.bind("iop", IOP)
    graph.bind("owl", OWL)
    graph.bind("pehterms", PEHTERMS)


def apply_ontology_alignments(graph: Graph) -> Graph:
    """Add shared ontology alignment axioms used by canonical and docs graphs."""
    bind_alignment_prefixes(graph)
    for local_class, external_class in CLASS_EQUIVALENCES:
        graph.add((local_class, OWL.equivalentClass, external_class))
    return graph


def equivalence_triple(local_class: URIRef, external_class: URIRef) -> str:
    return f"<{local_class}> <{OWL.equivalentClass}> <{external_class}> ."


def append_ontology_alignments(input_path: Path, output_path: Path) -> int:
    graph = Graph().parse(input_path, format="turtle")
    existing_text = input_path.read_text()
    additions: list[str] = []

    for local_class, external_class in CLASS_EQUIVALENCES:
        if (local_class, OWL.equivalentClass, external_class) not in graph:
            additions.append(equivalence_triple(local_class, external_class))

    if not additions:
        if output_path != input_path:
            output_path.write_text(existing_text)
        return len(graph)

    text = existing_text.rstrip()
    text = f"{text}\n\n{ALIGNMENT_COMMENT}\n" + "\n".join(additions) + "\n"
    output_path.write_text(text)
    return len(graph) + len(additions)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    output = args.output or args.input
    triple_count = append_ontology_alignments(args.input, output)
    print(f"Wrote {output} with {triple_count} triples.")


if __name__ == "__main__":
    main()

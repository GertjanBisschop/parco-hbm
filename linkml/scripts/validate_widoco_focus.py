#!/usr/bin/env python3
"""Validate the focused WIDOCO input ontology against its profile."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from rdflib import Graph, RDF, RDFS, URIRef
from rdflib.namespace import OWL

from build_widoco_focus import (
    PRIMITIVE_RANGES,
    class_uri,
    display_slot_uri,
    documented_classes,
    focused_slot_names,
    is_datatype_property,
    load_profile,
    load_schema,
    projected_range,
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def expand_curie(value: str, schema: dict[str, Any]) -> URIRef:
    prefixes = schema["prefixes"]
    if "://" in value:
        return URIRef(value)
    prefix, local = value.split(":", 1)
    base = prefixes[prefix]
    if isinstance(base, dict):
        base = base["prefix_reference"]
    return URIRef(f"{base}{local}")


def validate(schema: dict[str, Any], profile: dict[str, Any], graph: Graph) -> list[str]:
    errors: list[str] = []
    classes = schema["classes"]
    slots = schema["slots"]
    enums = schema.get("enums", {})

    expected_classes = documented_classes(schema, profile)
    for class_name in expected_classes:
        if (class_uri(class_name), RDF.type, OWL.Class) not in graph:
            fail(errors, f"Missing documented class: {class_name}")

    for class_name in profile.get("forbidden_classes", []):
        if (class_uri(class_name), RDF.type, OWL.Class) in graph:
            fail(errors, f"Forbidden helper class is documented: {class_name}")

    for enum_name, enum_def in enums.items():
        for permissible_value in (enum_def.get("permissible_values") or {}):
            enum_value_uri = URIRef(f"{class_uri(enum_name)}#{permissible_value}")
            if (enum_value_uri, RDF.type, OWL.Class) in graph:
                fail(errors, f"Enum value serialized as class: {enum_name}#{permissible_value}")

    for core_class in profile["core_classes"]:
        for slot_name in focused_slot_names(core_class, classes, profile):
            slot_def = slots[slot_name]
            prop_uri = display_slot_uri(slot_name, slot_def, schema["prefixes"], schema.get("default_prefix", "pehterms"))
            range_name = projected_range(slot_def.get("range", schema.get("default_range", "string")), profile)
            expected_type = OWL.DatatypeProperty if is_datatype_property(range_name, enums) else OWL.ObjectProperty
            if (prop_uri, RDF.type, expected_type) not in graph:
                fail(errors, f"Missing property from slot_uri for {core_class}.{slot_name}: {prop_uri}")
            fallback_uri = class_uri(slot_name)
            if fallback_uri != prop_uri and (
                (fallback_uri, RDF.type, OWL.ObjectProperty) in graph
                or (fallback_uri, RDF.type, OWL.DatatypeProperty) in graph
            ):
                fail(errors, f"LinkML slot name leaked as property IRI: {slot_name}")

    for prop_uri in graph.subjects(RDF.type, OWL.ObjectProperty):
        for range_uri in graph.objects(prop_uri, RDFS.range):
            if str(range_uri).startswith(str(class_uri(""))) and (range_uri, RDF.type, OWL.Class) not in graph:
                fail(errors, f"Object property range is not documented locally: {prop_uri} -> {range_uri}")

    for shape in profile.get("required_property_shapes", []):
        prop_uri = expand_curie(shape["property"], schema)
        domain_uri = class_uri(shape["domain"])
        range_name = shape["range"]
        range_uri = PRIMITIVE_RANGES.get(range_name, class_uri(range_name))
        if (prop_uri, RDFS.domain, domain_uri) not in graph:
            fail(errors, f"Missing required domain: {shape['property']} -> {shape['domain']}")
        if (prop_uri, RDFS.range, range_uri) not in graph:
            fail(errors, f"Missing required range: {shape['property']} -> {shape['range']}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ttl", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    args = parser.parse_args()

    graph = Graph().parse(args.ttl, format="turtle")
    errors = validate(load_schema(args.schema), load_profile(args.profile), graph)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"WIDOCO focus contract OK: {args.ttl} ({len(graph)} triples).")


if __name__ == "__main__":
    main()

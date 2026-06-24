#!/usr/bin/env python3
"""Build a focused WIDOCO input ontology from the PEH LinkML schema."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS, OWL, SKOS, XSD


PRIMITIVE_RANGES = {
    "boolean": XSD.boolean,
    "date": XSD.date,
    "datetime": XSD.dateTime,
    "decimal": XSD.decimal,
    "double": XSD.double,
    "float": XSD.float,
    "integer": XSD.integer,
    "string": XSD.string,
    "time": XSD.time,
    "uri": XSD.anyURI,
    "uriorcurie": XSD.anyURI,
}

PEH = Namespace("https://w3id.org/peh/")
PEHTERMS = Namespace("https://w3id.org/peh/terms/")
PAV = Namespace("http://purl.org/pav/")
SCHEMA = Namespace("http://schema.org/")


def load_schema(path: Path) -> dict[str, Any]:
    with path.open() as stream:
        return yaml.safe_load(stream)


def load_profile(path: Path) -> dict[str, Any]:
    with path.open() as stream:
        return yaml.safe_load(stream)


def expand_curie(value: str, prefixes: dict[str, Any], default_prefix: str) -> URIRef:
    if "://" in value:
        return URIRef(value)
    if ":" not in value:
        return URIRef(f"{prefixes[default_prefix]}{value}")
    prefix, local = value.split(":", 1)
    base = prefixes[prefix]
    if isinstance(base, dict):
        base = base["prefix_reference"]
    return URIRef(f"{base}{local}")


def local_name(uri: URIRef) -> str:
    text = str(uri)
    if "#" in text:
        return text.rsplit("#", 1)[1]
    return text.rstrip("/").rsplit("/", 1)[-1]


def class_uri(class_name: str) -> URIRef:
    return URIRef(f"{PEHTERMS}{class_name}")


def inherited_slots(class_name: str, classes: dict[str, Any]) -> list[str]:
    class_def = classes[class_name] or {}
    slot_names: list[str] = []

    parent = class_def.get("is_a")
    if parent in classes:
        slot_names.extend(inherited_slots(parent, classes))

    for mixin in class_def.get("mixins", []) or []:
        if mixin in classes:
            slot_names.extend(inherited_slots(mixin, classes))
            slot_names.extend(classes[mixin].get("slots", []) or [])

    slot_names.extend(class_def.get("slots", []) or [])
    return dedupe(slot_names)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def display_slot_uri(
    slot_name: str, slot_def: dict[str, Any], prefixes: dict[str, Any], default_prefix: str
) -> URIRef:
    return expand_curie(slot_def.get("slot_uri", f"{default_prefix}:{slot_name}"), prefixes, default_prefix)


def projected_range(range_name: str, profile: dict[str, Any]) -> str:
    return profile.get("helper_class_projections", {}).get(range_name, range_name)


def is_enum(range_name: str, enums: dict[str, Any]) -> bool:
    return range_name in enums


def is_datatype_property(range_name: str, enums: dict[str, Any]) -> bool:
    return range_name in PRIMITIVE_RANGES or is_enum(range_name, enums)


def camel_to_words(name: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r" \1", name).strip()


def add_property(
    graph: Graph,
    prop_uri: URIRef,
    slot_name: str,
    slot_def: dict[str, Any],
    domain_class: str,
    range_name: str,
    enums: dict[str, Any],
    profile: dict[str, Any],
) -> None:
    range_name = projected_range(range_name, profile)
    graph.add((prop_uri, RDF.type, OWL.DatatypeProperty if is_datatype_property(range_name, enums) else OWL.ObjectProperty))
    graph.add((prop_uri, RDFS.label, Literal(local_name(prop_uri))))
    graph.add((prop_uri, RDFS.domain, class_uri(domain_class)))

    description = slot_def.get("description")
    if description:
        graph.add((prop_uri, SKOS.definition, Literal(description)))

    if is_enum(range_name, enums):
        graph.add((prop_uri, RDFS.range, XSD.string))
        graph.add((prop_uri, SKOS.scopeNote, Literal(f"Controlled value set: {range_name}.")))
    elif range_name in PRIMITIVE_RANGES:
        graph.add((prop_uri, RDFS.range, PRIMITIVE_RANGES[range_name]))
    else:
        graph.add((prop_uri, RDFS.range, class_uri(range_name)))

    if slot_def.get("multivalued"):
        graph.add((prop_uri, SKOS.scopeNote, Literal("Multivalued property.")))
    if slot_name != local_name(prop_uri):
        graph.add((prop_uri, DCTERMS.identifier, Literal(slot_name)))


def focused_slot_names(class_name: str, classes: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    slot_names = inherited_slots(class_name, classes)
    extra_source = profile.get("extra_slot_sources", {}).get(class_name)
    if extra_source:
        slot_names.extend(inherited_slots(extra_source, classes))
    return dedupe(slot_names)


def range_dependency_classes(schema: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    classes = schema["classes"]
    slots = schema["slots"]
    enums = schema.get("enums", {})
    dependencies: list[str] = []

    for class_name in profile["core_classes"]:
        for slot_name in focused_slot_names(class_name, classes, profile):
            range_name = projected_range(slots[slot_name].get("range", schema.get("default_range", "string")), profile)
            if range_name in PRIMITIVE_RANGES or range_name in enums:
                continue
            if range_name not in classes:
                continue
            if range_name not in dependencies:
                dependencies.append(range_name)

    return dependencies


def documented_classes(schema: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    classes = list(profile["core_classes"])
    if profile.get("range_dependencies", "direct") != "direct":
        raise ValueError("Only direct range dependencies are currently supported.")
    for class_name in range_dependency_classes(schema, profile):
        if class_name not in classes:
            classes.append(class_name)
    return classes


def build_graph(schema: dict[str, Any], profile: dict[str, Any]) -> Graph:
    graph = Graph()
    prefixes = schema["prefixes"]
    default_prefix = schema.get("default_prefix", "pehterms")

    namespace_bindings = {
        "dcterms": DCTERMS,
        "owl": OWL,
        "pav": PAV,
        "peh": PEH,
        "pehterms": PEHTERMS,
        "rdf": RDF,
        "rdfs": RDFS,
        "schema": SCHEMA,
        "skos": SKOS,
        "xsd": XSD,
    }
    for prefix, namespace in namespace_bindings.items():
        graph.bind(prefix, namespace)

    ontology_uri = URIRef(profile["ontology_uri"])
    graph.add((ontology_uri, RDF.type, OWL.Ontology))
    graph.add((ontology_uri, RDFS.label, Literal(profile["title"])))
    graph.add((ontology_uri, PAV.version, Literal(str(schema.get("version", "")))))
    graph.add((ontology_uri, OWL.versionInfo, Literal(str(schema.get("version", "")))))
    graph.add((ontology_uri, SKOS.definition, Literal(schema.get("description", ""))))
    graph.add((ontology_uri, DCTERMS.source, URIRef(schema["id"])))

    classes = schema["classes"]
    slots = schema["slots"]
    enums = schema.get("enums", {})
    class_names = documented_classes(schema, profile)

    for class_name in class_names:
        class_def = classes[class_name]
        uri = class_uri(class_name)
        graph.add((uri, RDF.type, OWL.Class))
        graph.add((uri, RDFS.label, Literal(class_name)))
        graph.add((uri, SKOS.prefLabel, Literal(camel_to_words(class_name))))
        if class_def.get("description"):
            graph.add((uri, SKOS.definition, Literal(class_def["description"])))
        graph.add((uri, SKOS.inScheme, ontology_uri))

        parent = projected_range(class_def.get("is_a", ""), profile)
        if parent in class_names:
            graph.add((uri, RDFS.subClassOf, class_uri(parent)))
        else:
            graph.add((uri, RDFS.subClassOf, OWL.Thing))

    for class_name in profile["core_classes"]:
        for slot_name in focused_slot_names(class_name, classes, profile):
            slot_def = slots[slot_name]
            range_name = slot_def.get("range", schema.get("default_range", "string"))
            prop_uri = display_slot_uri(slot_name, slot_def, prefixes, default_prefix)
            add_property(graph, prop_uri, slot_name, slot_def, class_name, range_name, enums, profile)

    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    graph = build_graph(load_schema(args.schema), load_profile(args.profile))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=args.output, format="turtle")
    print(f"Wrote {args.output} with {len(graph)} triples.")


if __name__ == "__main__":
    main()

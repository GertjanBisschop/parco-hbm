#!/usr/bin/env python
"""
Nanopub Batch Upload GitHub Action Script

"""

import sys
import click
import datetime
import logging
import nanopub
import nanopub.definitions
import pathlib
import rdflib
import re
import requests
import yaml

from enum import Enum, Flag, auto
from pydantic import BaseModel, field_validator
from rdflib.namespace import SKOS, RDF
from typing import List, Optional, Mapping, Union

from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


BASE_NAMESPACE = rdflib.Namespace("https://w3id.org/peh/terms/")
PEH_NAMESPACE = "https://w3id.org/peh/"
TERM_NAMESPACE = "https://w3id.org/peh/terms/"

NAMESPACES = {
    "iop": "https://w3id.org/iadopt/ont/",
    "linkml": "https://w3id.org/linkml/",
    "pav": "http://purl.org/pav/",
    "peh": "https://w3id.org/peh/",
    "pehterms": "https://w3id.org/peh/terms/",
    "qudtqk": "http://qudt.org/2.1/vocab/quantitykind/",
    "qudtunit": "https://qudt.org/vocab/unit/",
    "schema1": "http://schema.org/",
}

CREATORS = [
    "https://orcid.org/0000-0002-6514-0173",  # Dirk Devriendt
    "https://orcid.org/0000-0001-8327-0142",  # Gertjan Bisschop
]


class ElementTypeEnum(str, Enum):
    CLASS = "class"
    SLOT = "slot"

    @classmethod
    def name_to_value(cls, name) -> str:
        if isinstance(name, cls):
            return name.value
        elif isinstance(name, str):
            try:
                ret = cls[name]
            except (KeyError, ValueError):
                return name
            return ret.value
        else:
            raise NotImplementedError


class SchemaElements(Flag):
    CLASS = auto()
    SLOT = auto()
    ALL = CLASS | SLOT


class Element(BaseModel):
    term_uri: str
    action: str = "added"
    linkml_element_type: Union[str, ElementTypeEnum]

    @field_validator("linkml_element_type", mode="after")
    @classmethod
    def map_long_enum(cls, value: Optional[Union[str, ElementTypeEnum]]) -> str:
        ret = None
        if value is not None:
            ret = ElementTypeEnum.name_to_value(value)

        return ret


class NanopubGenerator:
    def __init__(
        self,
        orcid_id: str,
        name: str,
        private_key: str,
        public_key: str,
        intro_nanopub_uri: str,
        test_server: bool,
    ):
        self.profile = nanopub.Profile(
            orcid_id=orcid_id,
            name=name,
            private_key=private_key,
            public_key=public_key,
            introduction_nanopub_uri=intro_nanopub_uri,
        )

        self.np_conf = nanopub.NanopubConf(
            profile=self.profile,
            use_test_server=test_server,
            add_prov_generated_time=True,
            attribute_publication_to_profile=True,
        )

    def create_nanopub(self, assertion: rdflib.Graph) -> nanopub.Nanopub:
        return nanopub.Nanopub(conf=self.np_conf, assertion=assertion)

    def update_nanopub(self, np_uri: str, assertion: rdflib.Graph) -> nanopub.Nanopub:
        new_np = nanopub.NanopubUpdate(
            uri=np_uri,
            conf=self.np_conf,
            assertion=assertion,
        )
        new_np.sign()
        return new_np

    @classmethod
    def is_nanopub_id(cls, key: str):
        allowed_prefixes = [
            "http://purl.org",
            "https://purl.org",
            "http://w3id.org",
            "https://w3id.org",
        ]
        for prefix in allowed_prefixes:
            if key.startswith(prefix):
                return True
        return False

    def check_nanopub_existence(self, entity: YAMLRoot) -> bool:
        try:
            # np_conf = self.np_conf
            url = getattr(entity, "id", None)
            if url is not None:
                return self.is_nanopub_id(url)
            else:
                raise ValueError("Entity id is None.")

        except Exception as e:
            logger.error(f"Error in check_nanopub_existence: {e}")
            sys.exit(1)


def get_property_mapping(
    data: List, schema_view: SchemaView, base: rdflib.Namespace
) -> Mapping:
    """
    Mapping of the kind: {property_name: slot_uri}
    example: {'name': rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#altLabel')}
    """
    namespace_mapping = {}
    for entity in data:
        if getattr(entity, "translations") is not None:
            for translation in entity.translations:
                if translation.property_name not in namespace_mapping:
                    property_name = translation.property_name
                    slot_def = schema_view.all_slots().get(property_name)
                    curie_str = getattr(slot_def, "slot_uri")
                    if curie_str is None:
                        curie_str = base[property_name]
                    uri_str = schema_view.expand_curie(curie_str)
                    namespace_mapping[property_name] = rdflib.term.URIRef(uri_str)

    return namespace_mapping


def add_translation_to_graph(
    g: rdflib.Graph, property_mapping: Mapping
) -> rdflib.Graph:
    try:
        if len(property_mapping) == 0:
            logger.info("LinkML schema does not contain translations.")
            return g

        #  Iterate over the triples and perform the transformation and removal
        for s, _, o in g.triples((None, BASE_NAMESPACE.translations, None)):
            language = g.value(o, BASE_NAMESPACE.language)
            property_name = str(g.value(o, BASE_NAMESPACE.property_name))
            translated_value = g.value(o, BASE_NAMESPACE.translated_value)
            # Apply the mapping
            if property_name in property_mapping:
                mapped_property = property_mapping[property_name]
                g.add(
                    (
                        s,
                        mapped_property,
                        rdflib.Literal(translated_value, lang=language),
                    )
                )

            # Remove the unnecessary blank node triples
            g.remove((o, None, None))
            g.remove((None, None, o))

        return g

    except Exception as e:
        logging.error(f"Error in add_translation_to_graph: {e}")
        raise


def add_vocabulary_membership(
    g: rdflib.Graph, vocab_uri: str, subject_type: rdflib.URIRef
) -> rdflib.Graph:
    """
    Adds vocabulary membership information to each concept in the graph.

    Args:
        g: An rdflib Graph instance containing vocabulary terms
        vocab_uri: URI string of the vocabulary collection

    Returns:
        The modified graph with vocabulary membership added
    """
    try:
        # Create a URI reference for the vocabulary
        vocabulary = rdflib.URIRef(vocab_uri)
        concepts = list(g.subjects(RDF.type, subject_type))
        SKOS_COLLECTION = SKOS.inScheme
        # Add the membership triple to each concept
        for concept in concepts:
            g.add((concept, SKOS_COLLECTION, vocabulary))

        return g
    except Exception as e:
        logging.error(f"Error in add_vocabulary_membership: {e}")
        raise


def extract_id(url: str):
    return url.replace(TERM_NAMESPACE, "", 1).lstrip("/")


def generate_htaccess(redirects: List, type_prefix: Optional[str]):
    """Generate .htaccess content."""

    rules = []

    for source, target in redirects:
        local_path = extract_id(source)
        if local_path:
            rules.append(f"RewriteRule ^{local_path}$ {target} [R=302,L]")

    return "\n".join(rules)


def update_htaccess(
    redirects: List, output_file: str, type_prefix: Optional[str] = None
):
    # example header
    # """Generate or update an .htaccess file."""
    # header = """RewriteEngine On
    #
    ## PEH redirections
    ## Format: Local ID to nanopub
    # """

    if not redirects:
        logger.error("No valid redirects found in input file.", file=sys.stderr)
        sys.exit(1)

    new_content = generate_htaccess(redirects, type_prefix=type_prefix)

    with open(output_file, "w") as f:
        f.write(new_content)

    logger.info(f"Successfully wrote .htaccess to {output_file}")
    logger.info(f"Added {len(redirects)} redirect rules")


def dump_identifier_pairs(pairs: List[tuple], file_name: str):
    try:
        with open(file_name, "w") as outfile:
            for pair in pairs:
                w3id_uri, nanopub_uri = pair
                print(f"{w3id_uri}, {nanopub_uri}", file=outfile)
    except Exception as e:
        logging.error(f"Error in dump_identifier_pairs: {e}")
        raise


def add_domain_statement(g: rdflib.Graph, term_uri: str, domain_uris: List[str]):
    """
    Adds RDF statements to define an OWL ObjectProperty with a union of domain classes.
    """
    term = rdflib.URIRef(term_uri)
    domain_refs = [rdflib.URIRef(uri) for uri in domain_uris]
    domain_node = rdflib.BNode()
    union_list_node = rdflib.BNode()

    if len(domain_refs) == 1:
        # Directly assign the domain if there's only one term
        g.add((term, rdflib.RDFS.domain, domain_refs[0]))

    else:
        g.add((domain_node, RDF.type, rdflib.OWL.Class))
        g.add((domain_node, rdflib.OWL.unionOf, union_list_node))

        # Construct the OWL:unionOf list
        prev_node = None
        for domain_ref in domain_refs:
            list_node = rdflib.BNode()
            g.add((list_node, RDF.first, domain_ref))
            if prev_node:
                g.add((prev_node, RDF.rest, list_node))
            else:
                g.add((union_list_node, RDF.first, domain_ref))
            prev_node = list_node

        # Close the RDF list structure
        g.add((prev_node, RDF.rest, RDF.nil))

        # Set the domain property
        g.add((term, rdflib.RDFS.domain, domain_node))

    return True


def build_new_graph() -> rdflib.Graph:
    g = rdflib.Graph()
    # bind custom namespaces
    for prefix, uri in NAMESPACES.items():
        g.bind(prefix, rdflib.Namespace(uri))

    return g


def adjust_linkml_graph(
    term_uri: str, element_type: str, sv: SchemaView
) -> Optional[rdflib.Graph]:
    g = None
    if element_type == "slot":
        g = build_new_graph()
        term = term_uri.replace(TERM_NAMESPACE, "", 1)
        name_slot = sv.get_slot(term)
        all_classes = sv.get_classes_by_slot(name_slot)
        domain_uris = [BASE_NAMESPACE[a] for a in all_classes]
        _ = add_domain_statement(g, term_uri, domain_uris)
        exact_match = str(getattr(name_slot, "slot_uri", None))
        if exact_match is not None:
            if not exact_match.startswith("http"):
                prefix, exact_match_term = exact_match.split(":")
                namespaces = sv.namespaces()
                exact_match = rdflib.URIRef(namespaces[prefix] + exact_match_term)
        else:
            exact_match = rdflib.URIRef(exact_match)
        g.add((BASE_NAMESPACE[term], rdflib.SKOS.exactMatch, exact_match))
    return g


def skolemize_blank_nodes(graph: rdflib.Graph):
    # Counter for unique Skolemized URIs
    skolem_counter = 1
    blank_node_mapping = {}

    # Iterate over graph triples
    for s, p, o in list(graph):
        # Replace blank nodes in Subject
        if isinstance(s, rdflib.BNode):
            if s not in blank_node_mapping:
                blank_node_mapping[s] = rdflib.URIRef(
                    f"{TERM_NAMESPACE}skolem{skolem_counter}"
                )
                skolem_counter += 1
            new_s = blank_node_mapping[s]
        else:
            new_s = s

        # Replace blank nodes in Object
        if isinstance(o, rdflib.BNode):
            if o not in blank_node_mapping:
                blank_node_mapping[o] = rdflib.URIRef(
                    f"{TERM_NAMESPACE}skolem{skolem_counter}"
                )
                skolem_counter += 1
            new_o = blank_node_mapping[o]
        else:
            new_o = o

        # Add updated triples
        graph.remove((s, p, o))  # Remove original triple
        graph.add((new_s, p, new_o))  # Add skolemized triple


def is_valid_assertion_graph(g: rdflib.Graph) -> bool:
    # TODO: add more checks
    return 0 < len(g) < nanopub.definitions.MAX_TRIPLES_PER_NANOPUB


def collect_related_bnodes(graph, start_node, visited=None):
    """Recursively collect all triples related to a blank node, especially rdf:Lists"""
    if visited is None:
        visited = set()
    if not isinstance(start_node, rdflib.BNode) or start_node in visited:
        return set()

    visited.add(start_node)
    related_triples = set()

    for s, p, o in graph.triples((start_node, None, None)):
        related_triples.add((s, p, o))
        if isinstance(o, rdflib.BNode):
            related_triples.update(collect_related_bnodes(graph, o, visited))

    return related_triples


def collect_subgraph(graph, subject):
    """Collect all triples about a subject, including recursively nested BNodes"""
    subgraph = set()
    for s, p, o in graph.triples((subject, None, None)):
        subgraph.add((s, p, o))
        if isinstance(o, rdflib.BNode):
            subgraph.update(collect_related_bnodes(graph, o))
    return subgraph


def build_rdf_graph(
    schema_graph: rdflib.Graph,
    term_uri: str,
    additional_statements: rdflib.Graph,
) -> rdflib.Graph:
    try:
        g = build_new_graph()
        term_uri = rdflib.URIRef(term_uri)
        collected_triples = collect_subgraph(schema_graph, term_uri)
        for s, p, o in collected_triples:
            g.add((s, p, o))

        # add additional staments
        if additional_statements is not None:
            g += additional_statements

        # skolemization step
        _ = skolemize_blank_nodes(g)

        if is_valid_assertion_graph(g):
            return g
        else:
            raise AssertionError("Assertion Graph is invalid.")
    except Exception as e:
        logger.debug(f"Error in build_rdf_graph: {e}")
        raise


def add_term(
    term_uri: str,
    schema_graph: rdflib.Graph,
    np_generator: NanopubGenerator,
    dry_run: bool,
    identifier_pairs: list,
    additional_statements: Optional[rdflib.Graph] = None,
) -> nanopub.Nanopub:
    term = term_uri.replace(TERM_NAMESPACE, "", 1)
    # build rdf graph
    graph = build_rdf_graph(schema_graph, term_uri, additional_statements)
    # publish nanopub
    np = np_generator.create_nanopub(assertion=graph)
    np.sign()
    logger.info("Nanopub signed")
    np_uri = np.metadata.np_uri
    if np_uri is None:
        raise ValueError("no URI returned by nanpub server.")
    logger.info(f"Nanopub signed for entity: {term}")
    if not dry_run:
        publication_info = np.publish()
        logger.info(f"Nanopub published: {publication_info}")
    # create w3id - nanopub pairs
    identifier_pairs.append((term_uri, np_uri))

    return np


def modify_term() -> nanopub.Nanopub:
    pass


def deprecate_term() -> nanopub.Nanopub:
    pass


def nanopub_identifier_args(f):
    f = click.option(
        "--orcid-id",
        required=True,
        envvar="NANOPUB_ORCID_ID",
        help="ORCID ID for nanopub profile",
    )(f)
    f = click.option(
        "--name", required=True, envvar="NANOPUB_NAME", help="Name for nanopub profile"
    )(f)
    f = click.option(
        "--private-key",
        required=True,
        envvar="NANOPUB_PRIVATE_KEY",
        help="Private key for nanopub profile",
    )(f)
    f = click.option(
        "--public-key",
        required=True,
        envvar="NANOPUB_PUBLIC_KEY",
        help="Public key for nanopub profile",
    )(f)
    f = click.option(
        "--intro-nanopub-uri",
        required=True,
        envvar="NANOPUB_INTRO_URI",
        help="Introduction nanopub URI",
    )(f)
    return f


@click.group()
def cli():
    """Main entry point"""
    pass


@click.command()
@click.option(
    "--schema",
    "-s",
    "schema_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the YAML schema file",
)
@click.option(
    "--output",
    "-o",
    "output_file",
    required=True,
    type=click.Path(writable=True),
    help="Path to the output YAML file",
)
@click.option(
    "--subset",
    "subset",
    required=False,
    type=str,
    help="Filter terms based on schema subsets.",
)
@click.option(
    "--schema-element",
    "-e",
    "schema_element",
    required=False,
    default=SchemaElements.ALL.name,
    help="Schema element type: CLASS, SLOT, or ALL (default: all).",
)
# add bool click option to filter deprecated elements
def list_terms(
    schema_path: str, output_file: str, schema_element: str, subset: Optional[str]
):
    """Main function to parse schema and serialize data to YAML."""
    schema_view = SchemaView(schema_path)
    elements = []
    schema_element_enum = SchemaElements[schema_element]

    # Function to collect elements
    def collect_elements(source, element_type: ElementTypeEnum, subset: str):
        for name, definition in source.items():
            if schema_view.get_uri(name).startswith("peh"):
                term_uri = TERM_NAMESPACE + name
                if subset is not None:
                    if hasattr(definition, "in_subset"):
                        in_subset_list = getattr(definition, "in_subset")
                        if subset in in_subset_list:
                            elements.append(
                                Element(
                                    term_uri=term_uri, linkml_element_type=element_type
                                )
                            )
                else:
                    elements.append(
                        Element(term_uri=term_uri, linkml_element_type=element_type)
                    )

    # Filter on subset
    if subset is not None:
        all_subsets = schema_view.all_subsets()
        if all_subsets.get(subset, None) is None:
            click.echo(f"{subset} is not a valid subset.")
            sys.exit(1)

    # Collect all classes and slots
    if schema_element_enum & SchemaElements.CLASS:
        collect_elements(schema_view.all_classes(), ElementTypeEnum.CLASS, subset)
    if schema_element_enum & SchemaElements.SLOT:
        collect_elements(schema_view.all_slots(), ElementTypeEnum.SLOT, subset)

    # Check if elements were found
    if not elements:
        click.echo("No matching elements found with 'peh' prefix.")
        return

    # Serialize the elements list to a YAML file
    terms_dict = {"terms": [element.model_dump() for element in elements]}
    with open(output_file, "w") as yaml_file:
        yaml.dump(terms_dict, yaml_file, default_flow_style=False, sort_keys=False)

    click.echo(f"Serialized data written to {output_file}")


@click.command()
@click.option(
    "--schema",
    "-s",
    "schema_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the LinkML schema from which to publish terms.",
)
@click.option(
    "--graph",
    "-g",
    "graph_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the rdf graph from which to publish terms.",
)
@click.option(
    "--changelog",
    "-c",
    "changelog_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to changelog",
)
@click.option(
    "--orcid-id",
    required=True,
    envvar="NANOPUB_ORCID_ID",
    help="ORCID ID for nanopub profile",
)
@click.option(
    "--name", required=True, envvar="NANOPUB_NAME", help="Name for nanopub profile"
)
@click.option(
    "--private-key",
    required=True,
    envvar="NANOPUB_PRIVATE_KEY",
    help="Private key for nanopub profile",
)
@click.option(
    "--public-key",
    required=True,
    envvar="NANOPUB_PUBLIC_KEY",
    help="Public key for nanopub profile",
)
@click.option(
    "--intro-nanopub-uri",
    required=True,
    envvar="NANOPUB_INTRO_URI",
    help="Introduction nanopub URI",
)
@click.option("--dry-run", is_flag=True, help="Prepare nanopubs but do not publish")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--htaccess-path",
    "htaccess_path",
    required=False,
    type=click.Path(),
    help="Path to output identifier nanopub pairs",
    default=None,
)
def publish(
    schema_path: str,
    graph_path: str,
    changelog_path: str,
    orcid_id: str,
    name: str,
    private_key: str,
    public_key: str,
    intro_nanopub_uri: str,
    dry_run: bool = False,
    verbose: bool = False,
    htaccess_path: str = None,
):
    """
    Create and publish nanopublications from changelog.
    """
    # Set logging level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        identifier_pairs = []
        # Count for reporting
        processed = 0
        published = 0
        updated = 0

        # import linkml schema:
        schema_graph = build_new_graph()
        schema_graph.parse(graph_path)
        schema_view = SchemaView(schema_path)
        nanopub_generator = NanopubGenerator(
            orcid_id=orcid_id,
            name=name,
            private_key=private_key,
            public_key=public_key,
            intro_nanopub_uri=intro_nanopub_uri,
            test_server=dry_run,
        )

        logger.info(f"Processing terms from {changelog_path} as part of {graph_path}")

        # Load YAML file
        click.echo("Validating changelog ...")
        with open(changelog_path, "r") as f:
            changelog = yaml.safe_load(f)

        # iterate across changes
        for change in changelog["changes"]:
            if change["action"] == "added":
                # generate nanopub and publish
                term_uri = change["term_uri"]
                element_type = change["linkml_element_type"]
                additional_statements = adjust_linkml_graph(
                    term_uri, element_type, schema_view
                )
                np = add_term(
                    term_uri,
                    schema_graph,
                    nanopub_generator,
                    dry_run,
                    identifier_pairs,
                    additional_statements=additional_statements,
                )
                processed += 1
                if not dry_run:
                    published += 1

            elif change["action"] == "modified":
                # get nanopub id from term id and update
                np = modify_term(term_uri)
                processed += 1
            elif change["action"] == "deprecated":
                # action TBD
                np = deprecate_term(term_uri)
                processed += 1
            else:
                logger.error(
                    f"Action {change['action']} for term {change['term_uri']} not implemented"
                )
                sys.exit(1)

        # Report summary
        logger.info(
            f"Processing complete. Processed: {processed}, "
            f"Published: {published}, Updated: {updated}"
        )

        # dump identifier_pairs
        if htaccess_path is None:
            htaccess_path = "./htaccess.txt"
        htaccess_path = pathlib.Path(htaccess_path).resolve()
        _ = update_htaccess(identifier_pairs, htaccess_path)

    except Exception as e:
        logger.error(f"Error in processing: {e}")
        sys.exit(1)


@click.command()
@click.option(
    "--schema",
    "-s",
    "schema_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the LinkML schema from which to publish terms.",
)
@click.option(
    "--graph",
    "-g",
    "graph_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the rdf graph from which to publish terms.",
)
@click.option(
    "--orcid-id",
    required=True,
    envvar="NANOPUB_ORCID_ID",
    help="ORCID ID for nanopub profile",
)
@click.option(
    "--name", required=True, envvar="NANOPUB_NAME", help="Name for nanopub profile"
)
@click.option(
    "--private-key",
    required=True,
    envvar="NANOPUB_PRIVATE_KEY",
    help="Private key for nanopub profile",
)
@click.option(
    "--public-key",
    required=True,
    envvar="NANOPUB_PUBLIC_KEY",
    help="Public key for nanopub profile",
)
@click.option(
    "--intro-nanopub-uri",
    required=True,
    envvar="NANOPUB_INTRO_URI",
    help="Introduction nanopub URI",
)
@click.option(
    "--example-for",
    "example",
    required=True,
    type=str,
    help="Serialize single nanopub for specified term.",
    default=None,
)
@click.option(
    "--element-type",
    "linkml_element_type",
    required=True,
    type=str,
    help="class, enum or slot",
)
@nanopub_identifier_args
def example(
    schema_path: str,
    graph_path: str,
    orcid_id: str,
    name: str,
    private_key: str,
    public_key: str,
    intro_nanopub_uri: str,
    example: str,
    linkml_element_type: str,
):
    """
    Create and publish nanopublications from changelog.
    """
    try:

        schema_graph = build_new_graph()
        schema_graph.parse(graph_path)
        sv = SchemaView(schema_path)

        nanopub_generator = NanopubGenerator(
            orcid_id=orcid_id,
            name=name,
            private_key=private_key,
            public_key=public_key,
            intro_nanopub_uri=intro_nanopub_uri,
            test_server=True,
        )

        logger.info(f"Serialize single example of type {example} from {graph_path}")
        temp_pairs = []
        dry_run = True
        additional_statement = adjust_linkml_graph(example, linkml_element_type, sv)

        np = add_term(
            example,
            schema_graph,
            nanopub_generator,
            dry_run,
            temp_pairs,
            additional_statement,
        )
        term = example.replace(TERM_NAMESPACE, "", 1)
        with open(f"example-{term}.trig", "w") as file:
            print(np, file=file)

    except Exception as e:
        logger.error(f"Error in processing: {e}")
        sys.exit(1)


def get_np_uri_from_linkml(uri: str) -> str:
    # TODO: this requires testing!!!
    try:
        response = requests.get(uri, allow_redirects=True)
        response.raise_for_status()
        return response.url
    except requests.RequestException as e:
        logger.error(f"An error occurred in get_np_uri_from_linkml: {e}")
        sys.exit(1)


@click.command()
@click.option(
    "--schema",
    "-s",
    "schema_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the LinkML schema from which to publish terms.",
)
@click.option(
    "--htaccess-file",
    "htaccess_file",
    required=False,
    type=click.Path(exists=True),
    default=None,
)
@click.option("--dry-run", is_flag=True, help="Prepare index but do not publish")
@nanopub_identifier_args
def push_index(
    schema_path: str,
    orcid_id: str,
    name: str,
    private_key: str,
    public_key: str,
    intro_nanopub_uri: str,
    htaccess_file: Optional[str] = None,
    dry_run: bool = True,
):
    logger.info(f"Running dry run is set to {dry_run}. Starting ...")
    uri_mapping = {}

    schema_view = SchemaView(schema_path)
    version = schema_view.schema.version
    if version is None:
        logger.error("Schema does not contain a version key.")
        sys.exit(1)
    model_title = schema_view.schema.title
    model_description = schema_view.schema.description

    nanopub_generator = NanopubGenerator(
        orcid_id=orcid_id,
        name=name,
        private_key=private_key,
        public_key=public_key,
        intro_nanopub_uri=intro_nanopub_uri,
        test_server=True,
    )
    if htaccess_file is not None:
        logger.info(f"Fetching nanopub uris for statements in {htaccess_file}")
        with open(htaccess_file, "r") as file:
            for line in file:
                # Example content of uri_pairs
                # RewriteRule ^EntityList$ http://purl.org/np/RAucNj8-CjIWhDt8y8arZ-Sgcr_-roQBzAohHRHww7bWQ [R=302,L]
                rewrite_rule = line.rstrip().split(" ")
                nanopub_uri = rewrite_rule[-2]
                term = rewrite_rule[1].replace("^", "", 1)
                term = re.sub(r"\$", "", term, count=1)
                uri_mapping[term] = nanopub_uri

    ## iterate over schema and add each of terms to index.
    # STEPS:
    # 1/ check if term in htaccess_file
    # 2/ check if nanopub can be found (request)
    logger.info(f"Collecting all terms that are part of the ontology version {version}")
    for cls in schema_view.all_classes():
        if cls not in uri_mapping:
            uri_mapping[cls] = get_np_uri_from_linkml(cls)
    for slot in schema_view.all_slots():
        if slot not in uri_mapping:
            uri_mapping[slot] = get_np_uri_from_linkml(slot)
    for enum in schema_view.all_enums():
        if enum not in uri_mapping:
            uri_mapping[enum] = get_np_uri_from_linkml(enum)

    np_uri_list = list(uri_mapping.values())
    np_list = nanopub.create_nanopub_index(
        nanopub_generator.np_conf,
        np_uri_list,
        model_title,
        model_description,
        datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
        CREATORS,
    )
    # add version info
    top_np = np_list[-1]
    SCHEMA_NS = rdflib.Namespace(NAMESPACES["schema1"])
    top_np.assertion.bind("schema1", SCHEMA_NS)
    top_np.assertion.add(
        (
            top_np.metadata.np_uri,
            rdflib.URIRef(SCHEMA_NS["version"]),
            rdflib.Literal(version),
        )
    )
    # publish the lot
    if not dry_run:
        logger.info("Publishing the signed nanopub(s) that make(s) up the index.")
        for np in np_list:
            np.publish()
        logger.info(f"Index is published at {np_list[-1].metadata.np_uri}")
    print(np_list[-1])
    return True


cli.add_command(list_terms)
cli.add_command(publish)
cli.add_command(example)
cli.add_command(push_index)

if __name__ == "__main__":
    cli()

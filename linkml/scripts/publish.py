#!/usr/bin/env python
"""
Nanopub Batch Upload GitHub Action Script

"""

import sys
import click
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

###### listing terms


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
    element_type: Union[str, ElementTypeEnum]

    @field_validator("element_type", mode="after")
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
    return url.lstrip(TERM_NAMESPACE).lstrip('/')    


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
        print("No valid redirects found in input file.", file=sys.stderr)
        sys.exit(1)

    new_content = generate_htaccess(redirects, type_prefix=type_prefix)

    with open(output_file, "w") as f:
        f.write(new_content)

    print(f"Successfully wrote .htaccess to {output_file}")
    print(f"Added {len(redirects)} redirect rules")


def dump_identifier_pairs(pairs: List[tuple], file_name: str):
    try:
        with open(file_name, "w") as outfile:
            for pair in pairs:
                w3id_uri, nanopub_uri = pair
                print(f"{w3id_uri}, {nanopub_uri}", file=outfile)
    except Exception as e:
        logging.error(f"Error in dump_identifier_pairs: {e}")
        raise


def build_graph_metadata():
    return None


def is_valid_assertion_graph(g: rdflib.Graph) -> bool:
    # TODO: add more checks
    return 0 < len(g) < nanopub.definitions.MAX_TRIPLES_PER_NANOPUB


def build_rdf_graph(
    schema_graph: rdflib.Graph,
    term_uri: str,
    additional_statements: rdflib.Graph,
) -> rdflib.Graph:
    try:
        g = rdflib.Graph()
        term_uri = rdflib.URIRef(term_uri)
        for s, p, o in schema_graph.triples((term_uri, None, None)):
            g.add((s, p, o))
        # add additional staments
        if additional_statements is not None:
            g += additional_statements
        if is_valid_assertion_graph(g):
            return g
        else:
            raise AssertionError("Assertion Graph is invalid.")
    except Exception as e:
        logger.debug(f"Error in build_rdf_graph: {e}")
        raise


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
                                Element(term_uri=term_uri, element_type=element_type)
                            )
                else:
                    elements.append(
                        Element(term_uri=term_uri, element_type=element_type)
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
    "--output-pairs",
    "output_path_pairs",
    required=False,
    type=click.Path(),
    help="Path to output identifier nanopub pairs",
    default=None,
)
@click.option(
    "--schema-uri",
    "schema_uri",
    required=False,
    type=str,
    help="URI for the schema this term is part of.",
    default=None,
)
def publish(
    schema_path: str,
    changelog_path: str,
    orcid_id: str,
    name: str,
    private_key: str,
    public_key: str,
    intro_nanopub_uri: str,
    dry_run: bool = False,
    verbose: bool = False,
    output_path_pairs: str = None,
    schema_uri: str = None,
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
        schema_graph = rdflib.Graph()
        schema_graph.parse(schema_path)

        nanopub_generator = NanopubGenerator(
            orcid_id=orcid_id,
            name=name,
            private_key=private_key,
            public_key=public_key,
            intro_nanopub_uri=intro_nanopub_uri,
            test_server=dry_run,
        )

        logger.info(f"Processing terms from {changelog_path} as part of {schema_path}")

        # Load YAML file
        click.echo("Validating changelog ...")
        with open(changelog_path, "r") as f:
            changelog = yaml.safe_load(f)

        # iterate across changes
        for change in changelog["changes"]:
            if change["action"] == "added":
                # generate nanopub and publish
                term_uri = change["term_uri"]
                term = term_uri.lstrip(TERM_NAMESPACE)
                # build rdf graph
                additional_statements = build_graph_metadata()
                graph = build_rdf_graph(schema_graph, term_uri, additional_statements)
                # publish nanopub
                np = nanopub_generator.create_nanopub(assertion=graph)
                np.sign()
                logger.info(f"Nanopub {processed} signed")
                np_uri = np.metadata.np_uri
                if np_uri is None:
                    raise ValueError("no URI returned by nanpub server.")

                logger.info(f"Nanopub signed: {np_uri} for entity: {term}")
                if not dry_run:
                    publication_info = np.publish()
                    published += 1
                    logger.info(f"Nanopub {processed} published: {publication_info}")

                # create w3id - nanopub pairs
                identifier_pairs.append((term_uri, np_uri))

            elif change["action"] == "modified":
                # get nanopub id from term id and update
                pass
            elif change["action"] == "deprecated":
                # action TBD
                pass
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
        if output_path_pairs is None:
            output_path_pairs = "./pairs.txt"
        output_path_pairs = pathlib.Path(output_path_pairs).resolve()
        _ = update_htaccess(identifier_pairs, output_path_pairs)

    except Exception as e:
        logger.error(f"Error in processing: {e}")
        sys.exit(1)


cli.add_command(list_terms)
cli.add_command(publish)

if __name__ == "__main__":
    cli()

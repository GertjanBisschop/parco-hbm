#!/usr/bin/env python3
"""
Vocabulary Change Log Management Tools

This script provides utilities for managing vocabulary term changes through
structured changelog files.
"""

import click
import yaml
import logging
import sys

from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from typing import Dict, List, Tuple, Optional

ACTIONS = ["added", "modified", "deprecated"]

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("changelog_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--schema",
    "-s",
    "schema_path",
    type=click.Path(exists=True, path_type=Path),
    help="Path to the JSON schema file for validation",
)
def validate_changelog(
    changelog_file: Path, schema_path: Path = None
) -> Tuple[bool, List[str]]:
    """
    Validate that a changelog file meets the required schema using JSON Schema

    """
    errors = []

    with open(schema_path, "r") as f:
        if schema_path.suffix == ".yaml" or schema_path.suffix == ".yml":
            schema = yaml.safe_load(f)
        else:
            raise ValueError

    try:
        # Load YAML file
        click.echo("Validating changelog ...")
        with open(changelog_file, "r") as f:
            data = yaml.safe_load(f)

        # Validate against schema
        validate(instance=data, schema=schema)

        # All validations passed
        click.echo("Changelog validated.")
        return True, []

    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML format: {str(e)}")
        logger.error(f"Invalid YAML format: {str(e)}")
        sys.exit(1)
    except ValidationError as e:
        # Extract the specific validation error information
        path = ".".join(str(p) for p in e.path) if e.path else "root"
        errors.append(f"Validation error at {path}: {e.message}")
        logger.error(f"Validation error at {path}: {e.message}")
        sys.exit(1)
    except Exception as e:
        errors.append(f"Error validating changelog: {str(e)}")
        logger.error(f"Error validating changelog: {str(e)}")
        sys.exit(1)

    return False, errors


@click.command()
@click.argument("changelog_file", type=click.Path(exists=True, path_type=Path))
def extract_version(changelog_file: Path):
    with open(changelog_file, "r") as f:
        data = yaml.safe_load(f)
    return data["version"]


@click.command()
@click.option("--maintainer", "-m", required=True, help="Maintainer email address")
@click.option(
    "--changelog-dir",
    "-d",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory where changelog files will be stored",
)
@click.option(
    "--version",
    "-v",
    required=False,
    help="Version number (e.g., 1.0.0)",
    default=None,
)
def init_new_changelog(maintainer: str, changelog_dir: Path, version: str) -> Dict:
    """
    Initialize a new changelog file with the given version and maintainer.
    """
    # Create directory if it doesn't exist
    changelog_dir.mkdir(parents=True, exist_ok=True)

    # Create the content dictionary
    version_str = "X.X.X" if version is None else version
    content = {
        "version": version_str,
        "release_date": "XXXX-XX-XX",
        "maintainer": maintainer,
        "changes": [],
    }

    # Generate the filename with the version
    if version is not None:
        changelog_path = changelog_dir / f"v{version}.yaml"
    else:
        changelog_path = changelog_dir / "_upcoming_unvalidated.yaml"

    # Write the YAML content to the file
    with open(changelog_path, "w") as f:
        yaml.dump(content, f, default_flow_style=False, sort_keys=False)

    click.echo(f"Created new changelog at: {changelog_path}")
    return content


@click.command()
@click.option("--changelog-file", "-f", required=True, type=click.Path(path_type=Path))
@click.option("--output-dir", "-o", required=False, type=click.Path(path_type=Path))
def generate_release_notes(changelog_file: Path, output_dir: Optional[Path]) -> str:
    """
    Generate human-readable release notes from a changelog file
    """
    with open(changelog_file, "r") as f:
        data = yaml.safe_load(f)

    version = data.get("version", "unknown")
    release_date = data.get("release_date", "unknown")
    maintainer = data.get("maintainer", "unknown")

    notes = [
        f"# Release {version}",
        f"Released on: {release_date}",
        f"Maintainer: {maintainer}",
        "",
        "## Changes",
        "",
    ]

    # Group changes by action
    added = []
    modified = []
    deprecated = []

    for change in data.get("changes", []):
        term_uri = change.get("term_uri", "unknown")
        term_id = term_uri.split("/")[-1]  # Extract term ID from URI
        action = change.get("action")
        description = change.get("description", "")

        if action == "added":
            added.append(f"- {term_id}: {description}")
        elif action == "modified":
            mod_props = []
            for prop in change.get("modified_properties", []):
                prop_name = prop.get("property", "").split(":")[
                    -1
                ]  # Extract local name
                mod_props.append(prop_name)

            prop_text = ", ".join(mod_props) if mod_props else "properties"
            modified.append(f"- {term_id}: Updated {prop_text}. {description}")
        elif action == "deprecated":
            replacement = change.get("replacement_term")
            if replacement:
                replacement_id = replacement.split("/")[-1]
                deprecated.append(
                    f"- {term_id}: Deprecated in favor of {replacement_id}. {description}"
                )
            else:
                deprecated.append(f"- {term_id}: Deprecated. {description}")

    if added:
        notes.append("### Added")
        notes.extend(added)
        notes.append("")

    if modified:
        notes.append("### Modified")
        notes.extend(modified)
        notes.append("")

    if deprecated:
        notes.append("### Deprecated")
        notes.extend(deprecated)
        notes.append("")

    click.echo("Release notes generated.")
    output_path = Path(f"v{version}-notes.txt")
    if output_dir is not None:
        output_path = Path(output_dir) / output_path
    with output_path.open("w") as f:
        print("\n".join(notes), file=f)

    return "\n".join(notes)


@click.group
def cli():
    pass


cli.add_command(init_new_changelog)
cli.add_command(validate_changelog)
cli.add_command(generate_release_notes)
cli.add_command(extract_version)

if __name__ == "__main__":
    cli()

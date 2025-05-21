import click
import yaml
import toml


@click.command()
@click.option(
    "--yaml-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the YAML schema file.",
)
@click.option(
    "--toml-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the TOML project file.",
)
def sync_version(yaml_file, toml_file):
    """Sync version from YAML schema to pyproject.toml"""

    # Load version from YAML schema
    with open(yaml_file, "r") as f:
        yaml_data = yaml.safe_load(f)
    yaml_version = yaml_data["version"]

    # Load and update TOML file
    with open(toml_file, "r") as f:
        toml_data = toml.load(f)

    toml_data["project"]["version"] = yaml_version  # Update version

    # Write back to TOML
    with open(toml_file, "w") as f:
        toml.dump(toml_data, f)

    click.echo(f"Updated {toml_file} version to {yaml_version}")


if __name__ == "__main__":
    sync_version()

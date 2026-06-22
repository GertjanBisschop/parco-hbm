import click
import yaml
from pathlib import Path
import re


VERSION_PATTERN = re.compile(r'(__version__\s*=\s*)["\'][^"\']+["\']')
TOML_VERSION_PATTERN = re.compile(r'^(\s*version\s*=\s*)["\'][^"\']+["\'](.*)$')


def replace_project_version(toml_content, version):
    in_project = False
    replacements = 0
    updated_lines = []

    for line in toml_content.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"

        if in_project:
            line, count = TOML_VERSION_PATTERN.subn(
                rf'\g<1>"{version}"\2',
                line,
                count=1,
            )
            replacements += count

        updated_lines.append(line)

    if replacements != 1:
        raise click.ClickException("Could not find project.version assignment in TOML file")

    return "".join(updated_lines)


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
@click.option(
    "--init-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the package __init__.py file.",
)
def sync_version(yaml_file, toml_file, init_file):
    """Sync version from YAML schema to package metadata files."""

    # Load version from YAML schema
    with open(yaml_file, "r") as f:
        yaml_data = yaml.safe_load(f)
    yaml_version = yaml_data["version"]

    toml_path = Path(toml_file)
    toml_path.write_text(replace_project_version(toml_path.read_text(), yaml_version))
    click.echo(f"Updated {toml_file} version to {yaml_version}")

    init_path = Path(init_file)
    init_content = init_path.read_text()
    updated_init_content, replacements = VERSION_PATTERN.subn(
        rf'\g<1>"{yaml_version}"',
        init_content,
        count=1,
    )
    if replacements != 1:
        raise click.ClickException(f"Could not find __version__ assignment in {init_file}")

    init_path.write_text(updated_init_content)
    click.echo(f"Updated {init_file} __version__ to {yaml_version}")


if __name__ == "__main__":
    sync_version()

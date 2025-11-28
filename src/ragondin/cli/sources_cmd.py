
import click

from ragondin.cli.main import cli
from ragondin.cli.utils import require_active_project

from ragondin.core.project.model import Project
from ragondin.core.project.analyse import estimate_source_recursive



@cli.group()
def source():
    """Manage sources inside the active project."""
    pass

@source.command(name="add")
@click.argument("path")
def add_source(path):
    """Add a source folder to the active project."""
    info = estimate_source_recursive(path)

    size_mb = info["total_size_bytes"] / (1024 * 1024)

    click.echo("Source size estimation :")
    click.echo(f"  - Files: {info['files']}")
    click.echo(f"  - Size: {size_mb:.2f} MB")
    click.echo(f"  - Characters: {info['chars']:,}")
    click.echo(f"  - Tokens (~): {info['tokens']:,}")
    click.echo(f"  - Estimated chunks: {info['chunks']:,}")
    proj = require_active_project()
    proj.add_source(path)
    click.echo(f"Added source: {path}")


@source.command(name="del")
@click.argument("path")
def delete_source(path):
    """Remove a source from the active project."""
    proj = require_active_project()
    proj.remove_source(path)
    click.echo(f"Removed source: {path}")


@source.command(name="list")
def list_sources():
    """List sources for the active project."""
    proj = require_active_project()

    sources = proj.list_sources()
    if not sources:
        click.echo("No sources defined.")
        return

    for s in sources:
        click.echo(f"- {s}")

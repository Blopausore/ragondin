
from ragondin.cli.main import cli


from .utils import require_active_project
import click
from ragondin.core.project.model import Project


@cli.group()
def source():
    """Manage sources inside the active project."""
    pass

@source.command(name="add")
@click.argument("path")
def add_source(path):
    """Add a source folder to the active project."""
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

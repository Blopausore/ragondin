import click

from ragondin.cli.main import cli

from ragondin.core.project.model import Project
from ragondin.core.project.active import get_active_project, load_active_project

from .utils import require_active_project

@cli.command()
@click.argument("dir_path")
def add(dir_path):
    """Add a directory as a source to the active project."""
    project = require_active_project()
    project.add_source(dir_path)
    click.echo(f"Added source: {dir_path}")

@cli.command()
def list():
    """List all source directories of the active project."""
    project = require_active_project()

    paths = project.list_sources()
    if not paths:
        click.echo("No sources added.")
    for p in paths:
        click.echo(f" - {p}")
        
        
@cli.command(name="del")
@click.argument("dir_path")
def delete_source(dir_path):
    """Remove a directory source from the active project."""
    project = require_active_project()
    project.remove_source(dir_path)
    click.echo(f"Removed source: {dir_path}")


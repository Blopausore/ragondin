import click

from ragondin.cli.main import cli

from ragondin.core.project import add_source, list_sources, remove_source
from ragondin.core.active import get_active_project


@cli.command()
@click.argument("dir_path")
def add(dir_path):
    """Add a directory as a source to the active project."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected. Use `ragondin connect NAME`.")
        return

    add_source(proj, dir_path)
    click.echo(f"Added source: {dir_path}")

@cli.command()
def list():
    """List all source directories of the active project."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    paths = list_sources(proj)
    if not paths:
        click.echo("No sources added.")
    for p in paths:
        click.echo(f" - {p}")
        
        
@cli.command(name="del")
@click.argument("dir_path")
def delete_source(dir_path):
    """Remove a directory source from the active project."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    remove_source(proj, dir_path)
    click.echo(f"Removed source: {dir_path}")


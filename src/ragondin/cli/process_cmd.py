import shutil
import click

from ragondin.cli.main import cli

from ragondin.core.indexing.pipeline import process_project
from . import utils

@cli.command()
def process():
    """Run the full incremental indexation pipeline on the active project."""
    project = utils.require_active_project()

    if project is None:
        click.echo("No active project. Use: ragondin switch <name>")
        return

    click.echo(f"Processing project: {project.name}")
    new_index = process_project(project)

    click.echo(f"Indexed {len(new_index['files'])} files.")
    click.echo("Processing complete.")


@cli.command()
def rebuild():
    """Delete FAISS index and fully rebuild the project."""
    project = utils.require_active_project()

    if project is None:
        click.echo("No active project.")
        return

    index_dir = project.root / "index"
    if index_dir.exists():
        click.echo(f"Deleting index directory: {index_dir}")
        shutil.rmtree(index_dir)

    click.echo("Rebuilding index from scratch...")
    process_project(project)

    click.echo("Rebuild complete.")

import click

from ragondin.cli.main import cli

from ragondin.core.project import BASE_DIR, create_project, add_source, list_sources, remove_source
from ragondin.core.active import set_active_project, get_active_project, disconnect, get_status


@cli.command()
@click.argument("project_name")
def create(project_name):
    """Create a new project."""
    create_project(project_name)
    click.echo(f"Project '{project_name}' created.")

@cli.command()
@click.argument("project_name")
def connect(project_name):
    """Connect to a project, making it active."""
    set_active_project(project_name)
    click.echo(f"Connected to '{project_name}'.")
    
@cli.command()
def disconnect():
    """Disconnect from the current active project."""
    if get_active_project() is None:
        click.echo("No active project to disconnect.")
        return

    proj = get_active_project()
    disconnect()
    click.echo(f"Disconnected from '{proj}'.")

@cli.command()
def status():
    """Show the current active project and its sources."""
    proj = get_status()
    if proj is None:
        click.echo("No active project.")
        return

    click.echo(f"Active project: {proj}\n")
    paths = list_sources(proj)

    if not paths:
        click.echo("No sources added.")
        return

    click.echo("Sources:")
    for p in paths:
        click.echo(f" - {p}")

    # Vérification index
    from pathlib import Path
    idx = BASE_DIR / proj / "index" / "index.faiss"
    if idx.exists():
        click.echo("\nIndex: ✔ present")
    else:
        click.echo("\nIndex: ✘ missing (run `ragondin process`)")

    # Nombre de raw docs
    raw_dir = BASE_DIR / proj / "raw_docs"
    if raw_dir.exists():
        count = len(list(raw_dir.glob("*")))
        click.echo(f"Raw docs: {count}")

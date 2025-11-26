
import click

from ragondin.cli.main import cli


from ragondin.core.project.model import Project
from ragondin.core.project.active import load_active_project, set_active_project, get_active_project, disconnect, get_status
from ragondin.core.project.manager import get_list_projects

@cli.command(name="create")
@click.argument("project_name")
def create(project_name):
    """Create a new project."""
    Project.create(project_name)
    click.echo(f"Project '{project_name}' created.")

@cli.command(name="connect")
@click.argument("project_name")
def connect(project_name):
    """Connect to a project, making it active."""
    set_active_project(project_name)
    click.echo(f"Connected to '{project_name}'.")
    
@cli.command(name="disconnect")
def disconnect_project():
    """Disconnect from the current active project."""
    if get_active_project() is None:
        click.echo("No active project to disconnect.")
        return

    project_name = get_active_project()
    disconnect()
    click.echo(f"Disconnected from '{project_name}'.")

@cli.command()
def status():
    """Show the current active project and its sources."""
    project = load_active_project()
    
    # Project connected
    if project is None:
        click.echo(f"No active project.")
        return
    
    click.echo(f"Active project: {project.name}\n")

    # Project sources
    paths = project.list_sources()

    if not paths:
        click.echo("No sources added.")
        return

    click.echo("Sources:")
    for p in paths:
        click.echo(f" - {p}")

    # Index check
    from pathlib import Path
    idx = project.index_dir / "index.faiss"
    if idx.exists():
        click.echo("\nIndex: Present")
    else:
        click.echo("\nIndex: Missing (run `ragondin process`)")

    # Number of rows
    raw_dir = project.root / "raw_docs"
    if raw_dir.exists():
        count = len(list(raw_dir.glob("*")))
        click.echo(f"Raw docs: {count}")


@cli.command(name="list")
def list_projects():
    """List projects."""
    project_list = get_list_projects()
    if project_list:
        click.echo("List of projects :")
        for project_name in project_list:
            click.echo(f" - {project_name}")
    else:
        click.echo("No project created.")
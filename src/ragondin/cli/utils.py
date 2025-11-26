import click

from ragondin.core.project.active import load_active_project 


def require_active_project():
    """Return the active Project or abort with a clean CLI message."""
    try:
        project = load_active_project()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}")
        raise click.Abort()
    except RuntimeError as e:
        click.echo(f"Error: {e}")
        raise click.Abort()
    except ValueError as e:
        click.echo(f"Error: {e}")
        raise click.Abort()
    except Exception as e:
        # Catch-all for any unexpected internal bug
        click.echo(f"Unexpected error: {e}")
        raise click.Abort()

    if project is None:
        click.echo("No active project. Use `ragondin connect NAME`.")
        raise click.Abort()

    return project
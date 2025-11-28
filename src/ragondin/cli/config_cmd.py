import click
from ragondin.cli.main import cli
from ragondin.config.manager import get_config, set_value, set_config 
from ragondin.config.manager import DEFAULT_CONFIG

default_help = "\n".join(
    f"  {k}: {v}" for k, v in DEFAULT_CONFIG.items()
)


@cli.group(help=f"""
View or modify Ragondin configuration.

Default configuration:
{default_help}
""")
def config():
    """View or modify Ragondin configuration."""
    pass

@config.command()
def show():
    """Show full configuration."""
    cfg = get_config()
    for k, v in cfg.items():
        click.echo(f"{k}: {v}")

@config.command()
@click.argument("value")
def reranker(value):
    """Enable or disable reranker."""
    boolean = value.lower() in ("true", "1", "yes", "on")
    set_value("use_reranker", boolean)
    click.echo(f"Reranker set to {boolean}")

@config.command()
@click.argument("model")
def embedding(model):
    """Set embedding model."""
    set_value("embedding_model", model)
    click.echo(f"Embedding model set to {model}")

@config.command()
@click.argument("n", type=int)
def k(n):
    """Set the retriever top-k."""
    set_value("retriever_k", n)
    click.echo(f"Retriever k set to {n}")

@config.command(name="set-default")
def set_default():
    """Reset configuration to default values."""
    set_config(DEFAULT_CONFIG.copy())
    click.echo("Configuration reset to default values.")
import click
from ragondin.cli.main import cli
from ragondin.core.config.manager import get_config, set_value

@cli.group()
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

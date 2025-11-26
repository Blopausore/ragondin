import click


@click.group()
def cli():
    """Ragondin CLI — Local Personal RAG."""
    pass

from .ask_cmd import ask
from .debug_cmd import (
    debug, embeddings, 
    retriever, cli
    )
from .process_cmd import process, rebuild
from .project_cmd import (
    create, connect, disconnect, status
    )
from .sources_cmd import (
    add, list, delete_source
    )
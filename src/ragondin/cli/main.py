import click

@click.group()
def cli():
    """Ragondin CLI — Local Personal RAG."""
    pass



# from . import ask_cmd
# from . import process_cmd
# from . import project_cmd
# from . import sources_cmd
# from . import config_cmd
# from . import debug_cmd
# from . import utils

from .ask_cmd import ask
from .debug_cmd import (
    debug, embeddings, retriever
    )
from .process_cmd import process, rebuild
from .project_cmd import (
    create, connect, disconnect, status, list_projects
    )
from .sources_cmd import (
    add_source, list_sources, delete_source
    )

from .config_cmd import (
    config, show, reranker, embedding, k
    ) 


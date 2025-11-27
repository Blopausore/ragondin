import click

from ragondin.cli.main import cli

from ragondin.core.indexing import vectordb
from ragondin.core.retrieval import retriever
from ragondin.core.rag_chain import prompt_builder

from . import utils


@cli.command()
@click.argument("question")
def ask(question):
    """Ask a question using the active project."""
    click.echo("[ASK] Starting ask command")

    project = utils.require_active_project()
    click.echo(f"[ASK] Loaded project: {project}")

    try:
        db = vectordb.load_vector_db(project)
        click.echo(f"[ASK] Loaded vector DB: {db}")
    except Exception as e:
        click.echo(f"[ASK] ERROR loading vector DB: {e}")
        raise

    try:
        r = retriever.build_retriever(db)
        click.echo(f"[ASK] Retriever built: {r}")
    except Exception as e:
        click.echo(f"[ASK] ERROR building retriever: {e}")
        raise

    try:
        docs = r.invoke(question)
        click.echo(f"[ASK] Retrieved docs: {docs}")
    except Exception as e:
        click.echo(f"[ASK] ERROR retrieving docs: {e}")
        raise

    try:
        context = retriever.format_docs(docs)
        click.echo(f"[ASK] Formatted context: {context}")
    except Exception as e:
        click.echo(f"[ASK] ERROR formatting docs: {e}")
        raise

    try:
        prompt = prompt_builder.build_final_prompt(question, context)
        click.echo(f"[ASK] Final prompt: {prompt}")
    except Exception as e:
        click.echo(f"[ASK] ERROR building final prompt: {e}")
        raise

    click.echo(prompt)

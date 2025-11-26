import click

from ragondin.cli.main import cli

from ragondin.core.indexing.vectordb import load_vector_db
from ragondin.core.retrieval.retriever import build_retriever, format_docs
from ragondin.core.rag_chain.prompt_builder import build_final_prompt

from .utils import require_active_project


@cli.command()
@click.argument("question")
def ask(question):
    """Ask a question using the active project."""
    click.echo("[ASK] Starting ask command")

    project = require_active_project()
    click.echo(f"[ASK] Loaded project: {project}")

    try:
        db = load_vector_db(project)
        click.echo(f"[ASK] Loaded vector DB: {db}")
    except Exception as e:
        click.echo(f"[ASK] ERROR loading vector DB: {e}")
        raise

    try:
        retriever = build_retriever(db)
        click.echo(f"[ASK] Retriever built: {retriever}")
    except Exception as e:
        click.echo(f"[ASK] ERROR building retriever: {e}")
        raise

    try:
        docs = retriever.invoke(question)
        click.echo(f"[ASK] Retrieved docs: {docs}")
    except Exception as e:
        click.echo(f"[ASK] ERROR retrieving docs: {e}")
        raise

    try:
        context = format_docs(docs)
        click.echo(f"[ASK] Formatted context: {context}")
    except Exception as e:
        click.echo(f"[ASK] ERROR formatting docs: {e}")
        raise

    try:
        prompt = build_final_prompt(question, context)
        click.echo(f"[ASK] Final prompt: {prompt}")
    except Exception as e:
        click.echo(f"[ASK] ERROR building final prompt: {e}")
        raise

    click.echo(prompt)

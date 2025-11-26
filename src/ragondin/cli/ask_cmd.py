import click

from ragondin.cli.main import cli

from ragondin.core.active import get_active_project
from ragondin.core.vectordb import load_vector_db
from ragondin.core.retriever import build_retriever, format_docs
from ragondin.core.prompt_builder import build_final_prompt

@cli.command()
@click.argument("question")
def ask(question):
    """Ask a question to the active project (outputs a prompt for ChatGPT)."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    db = load_vector_db(proj)
    retriever = build_retriever(db, k=10, fetch_k=20, lambda_mult=0.5)
    docs = retriever.invoke(question)
    
    print("=== RETRIEVED CHUNKS ===")
    for d in docs:
        print("•", d.metadata.get("path"))

    ctx = format_docs(docs)
    prompt = build_final_prompt(question, ctx)
    
    click.echo(prompt)


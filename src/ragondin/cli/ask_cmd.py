import click

from ragondin.cli.main import cli

from ragondin.core.indexing.vectordb import load_vector_db
from ragondin.core.retrieval.retriever import build_retriever, format_docs
from ragondin.core.rag_chain.prompt_builder import build_final_prompt

from .utils import require_active_project

@cli.command()
@click.argument("question")
def ask(question):
    """Ask a question to the active project (outputs a prompt for ChatGPT)."""
    project = require_active_project()
    
    db = load_vector_db(project)
    retriever = build_retriever(db, k=10, fetch_k=20, lambda_mult=0.5)
    docs = retriever.invoke(question)
    
    print("=== RETRIEVED CHUNKS ===")
    for d in docs:
        print("•", d.metadata.get("path"))

    ctx = format_docs(docs)
    prompt = build_final_prompt(question, ctx)
    
    click.echo(prompt)



import click
from pathlib import Path
import numpy as np

from ragondin.cli.main import cli

from ragondin.core.project.model import Project
from ragondin.core.indexing.splitter import load_and_split_file
from ragondin.core.indexing.vectordb import load_vector_db
from ragondin.core.retrieval.retriever import build_retriever

from .utils import require_active_project

@cli.group()
def debug():
    """Debug tools for inspecting Ragondin internals."""
    pass


@debug.command()
@click.option("--sample", default=5, help="Number of chunks to inspect")
def embeddings(sample):
    """Inspect embeddings (norm, head of vector, metadata)."""
    project = require_active_project()
    
    db = load_vector_db(project)
    
    emb = db.embedding_function

    vectors = db.index.reconstruct_n(0, sample)

    for i in range(min(sample, len(vectors))):
        v = vectors[i]
        norm = np.linalg.norm(v)
        doc = db.docstore.search(str(i))  # document ID
        
        click.echo(f"\n=== Embedding #{i} ===")
        click.echo(f"Norm: {norm:.6f}")
        click.echo(f"Dims head: {v[:5]}")
        click.echo(f"Metadata: {doc.metadata}")


@debug.command()
@click.argument("query")
def retriever(query):
    """Debug the FAISS/MMR retrieval for a specific query."""
    project = require_active_project()
    

    db = load_vector_db(project)
    retr = build_retriever(db, k=5, fetch_k=20)

    emb = db.embedding_function.embed_query(query)
    click.echo(f"Query norm: {np.linalg.norm(emb):.6f}\n")

    # Raw FAISS search
    scores, idxs = db.index.search(np.array([emb]).astype("float32"), 20)

    click.echo("=== RAW FETCH (FAISS) ===")
    for score, idx in zip(scores[0], idxs[0]):
        doc = db.docstore.search(str(idx))
        click.echo(f"{score:.3f} | {doc.metadata.get('path')}")

    # MMR results
    click.echo("\n=== MMR FINAL K ===")
    docs = retr.invoke(query)
    for d in docs:
        click.echo(f"• {d.metadata.get('path')}")



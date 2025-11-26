
import click
from pathlib import Path
import numpy as np

from ragondin.cli.main import cli

from ragondin.core.project import BASE_DIR
from ragondin.core.active import get_active_project
from ragondin.core.splitter import load_and_split_file
from ragondin.core.vectordb import load_vector_db
from ragondin.core.retriever import build_retriever

@cli.group()
def debug():
    """Debug tools for inspecting Ragondin internals."""
    pass


@debug.command()
def chunks():
    """Show generated document chunks before indexing."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return
    
    base = BASE_DIR / proj
    paths_file = base / "paths.txt"

    if not paths_file.exists():
        click.echo("No collected files found. Run: ragondin collect")
        return
    
    project_root = base
    files = [Path(p) for p in paths_file.read_text().splitlines()]
    
    click.echo(f"Found {len(files)} files. Splitting...\n")

    for file in files:
        docs = load_and_split_file(file, project_root)
        click.echo(f"\n=== {file} ===")
        for i, d in enumerate(docs, 1):
            click.echo(f"\n--- Chunk {i} ({len(d.page_content)} chars) ---")
            click.echo(d.page_content[:600] + "\n[...]")

@debug.command()
@click.option("--sample", default=5, help="Number of chunks to inspect")
def embeddings(sample):
    """Inspect embeddings (norm, head of vector, metadata)."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return
    
    db = load_vector_db(proj)
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
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    db = load_vector_db(proj)
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



@debug.command()
def debug_cli(query=""):
    """Debug the CLI. See if changes are reflected."""
    click.echo(f"CLI debug command received query: {query}")
    return 
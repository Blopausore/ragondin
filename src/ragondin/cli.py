import click
from .core.project import BASE_DIR, create_project, add_source, list_sources, remove_source
from .core.active import set_active_project, get_active_project, disconnect, get_status
from .core.collector import collect_files
from .core.splitter import load_and_split_file
from .core.vectordb import build_vector_db, load_vector_db
from .core.retriever import build_retriever, format_docs
from .core.prompt_builder import build_final_prompt

@click.group()
def cli():
    """Ragondin CLI — Local Personal RAG."""
    pass

# ---------------------------
#  CREATE + CONNECT
# ---------------------------

@cli.command()
@click.argument("project_name")
def create(project_name):
    """Create a new project."""
    create_project(project_name)
    click.echo(f"Project '{project_name}' created.")

@cli.command()
@click.argument("project_name")
def connect(project_name):
    """Connect to a project, making it active."""
    set_active_project(project_name)
    click.echo(f"Connected to '{project_name}'.")
    
@cli.command()
def disconnect():
    """Disconnect from the current active project."""
    if get_active_project() is None:
        click.echo("No active project to disconnect.")
        return

    proj = get_active_project()
    disconnect()
    click.echo(f"Disconnected from '{proj}'.")

@cli.command()
def status():
    """Show the current active project and its sources."""
    proj = get_status()
    if proj is None:
        click.echo("No active project.")
        return

    click.echo(f"Active project: {proj}\n")
    paths = list_sources(proj)

    if not paths:
        click.echo("No sources added.")
        return

    click.echo("Sources:")
    for p in paths:
        click.echo(f" - {p}")

    # Vérification index
    from pathlib import Path
    idx = BASE_DIR / proj / "index" / "index.faiss"
    if idx.exists():
        click.echo("\nIndex: ✔ present")
    else:
        click.echo("\nIndex: ✘ missing (run `ragondin process`)")

    # Nombre de raw docs
    raw_dir = BASE_DIR / proj / "raw_docs"
    if raw_dir.exists():
        count = len(list(raw_dir.glob("*")))
        click.echo(f"Raw docs: {count}")


# ---------------------------
#  MANAGE SOURCES
# ---------------------------

@cli.command()
@click.argument("dir_path")
def add(dir_path):
    """Add a directory as a source to the active project."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected. Use `ragondin connect NAME`.")
        return

    add_source(proj, dir_path)
    click.echo(f"Added source: {dir_path}")

@cli.command()
def list():
    """List all source directories of the active project."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    paths = list_sources(proj)
    if not paths:
        click.echo("No sources added.")
    for p in paths:
        click.echo(f" - {p}")
        
        
@cli.command(name="del")
@click.argument("dir_path")
def delete_source(dir_path):
    """Remove a directory source from the active project."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    remove_source(proj, dir_path)
    click.echo(f"Removed source: {dir_path}")


# ---------------------------
#  PROCESS (indexation)
# ---------------------------

@cli.command()
def process():
    """Process the active project: collect files, split, embed, index."""
    proj = get_active_project()
    if proj is None:
        click.echo("No project connected.")
        return

    click.echo("Collecting files...")
    files = collect_files(proj)

    click.echo(f"Found {len(files)} files. Splitting into chunks...")
    
    all_chunks = []
    warned=False
    for f in files:
        try:
            all_chunks.extend(load_and_split_file(f))
        except Exception as e:
            if not warned:
                click.echo(f"  - Error processing {f}: {e}")
                warned=True
            continue

    click.echo(f"Total chunks: {len(all_chunks)}")
    click.echo("Building FAISS index...")
    build_vector_db(proj, all_chunks)

    click.echo("Processing complete.")

# ---------------------------
#  ASK
# ---------------------------

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



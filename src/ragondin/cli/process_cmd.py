
import shutil
import click

from ragondin.cli.main import cli

from ragondin.core.project import BASE_DIR
from ragondin.core.active import get_active_project
from ragondin.core.collector import collect_files
from ragondin.core.splitter import load_and_split_file
from ragondin.core.vectordb import build_vector_db

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


@cli.command()
def rebuild():
    """
    Delete and rebuild the vector index for the active project.
    """
    proj = get_active_project()
    if proj is None:
        click.echo("No active project.")
        return

    project_dir = BASE_DIR / proj

    index_dir = project_dir / "index"
    raw_docs_dir = project_dir / "raw_docs"
    paths_file = project_dir / "paths.txt"

    if index_dir.exists():
        click.echo(f"Removing index: {index_dir}")
        shutil.rmtree(index_dir)

    if raw_docs_dir.exists():
        click.echo(f"Removing raw_docs: {raw_docs_dir}")
        shutil.rmtree(raw_docs_dir)

    if paths_file.exists():
        click.echo(f"Removing paths.txt: {paths_file}")
        paths_file.unlink()

    click.echo("Rebuilding project…")

    # Re-collect raw files
    source_paths = get_source_paths_for_project(proj)
    if not source_paths:
        click.echo("No source paths saved for this project.")
        return

    from ..core.collector import collect_paths
    collect_paths(source_paths, proj)

    # Rebuild index
    from ..core.collector import build_index
    build_index(proj)

    click.echo("Rebuild complete!")

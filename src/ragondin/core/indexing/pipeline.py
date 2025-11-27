from pathlib import Path

from ..project.model import Project

from .collector import collect_files
from .splitter import load_and_split_file
from .hashing import (
    load_chunk_index, save_chunk_index,
    compute_file_hash, compute_chunk_hash,
)
from .vectordb import build_vector_db



def process_project(project: Project):
    """
    Full incremental pipeline using Project object:
    - project.name : identifier
    - project.root : Path to project directory
    """


    old_index = load_chunk_index(project.root)
    old_files = old_index.get("files", {})

    # Collect files with the Project-aware collector
    all_files = collect_files(project)

    new_index = {"files": {}}
    all_chunks = []

    # Process each file
    for (source_root, file_path) in all_files:
        text = file_path.read_text(errors="ignore")
        file_hash = compute_file_hash(text)

        entry_old = old_files.get(str(file_path))
        if entry_old and entry_old["file_hash"] == file_hash:
            new_index["files"][str(file_path)] = entry_old
            continue

        
        # Splitting now needs project.root for relative paths
        docs = load_and_split_file(file_path, source_root=source_root)
        chunk_hashes = [compute_chunk_hash(doc.page_content) for doc in docs]

        new_index["files"][str(file_path)] = {
            "file_hash": file_hash,
            "chunks": chunk_hashes,
        }

        all_chunks.extend(docs)
    if not all_chunks:
        print(f">>> WARNING: No new or modified documents detected for project '{project.name}'. Skipping vector DB build.")
        return new_index
    
    print(f">>> INFO: {len(all_chunks)} chunk ready to process")
    # 6. Vector DB now uses a project identifier (up to you: name or path)
    build_vector_db(project, all_chunks)

    # 7. Save index
    save_chunk_index(project.root, new_index)

    return new_index

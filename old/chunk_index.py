import json
from pathlib import Path
import hashlib


CHUNK_FILE = "chunks.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_chunk_index(project_dir: Path):
    path = project_dir / CHUNK_FILE
    if path.exists():
        return json.loads(path.read_text())
    return {"files": {}}


def save_chunk_index(project_dir: Path, index):
    path = project_dir / CHUNK_FILE
    path.write_text(json.dumps(index, indent=2))


def compute_file_hash(text: str) -> str:
    return sha256(text)


def compute_chunk_hash(chunk_text: str) -> str:
    return sha256(chunk_text)


def diff_file_chunks(old_chunks, new_chunks):
    """
    old_chunks: ["hash1", "hash2", ...]
    new_chunks: ["hash1", "hashX", ...]
    
    Returns:
        to_add: list of new chunk hashes
        to_delete: list of hashes that disappeared
    """
    old_set = set(old_chunks)
    new_set = set(new_chunks)

    to_add = list(new_set - old_set)
    to_delete = list(old_set - new_set)

    return to_add, to_delete

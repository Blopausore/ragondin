import json
import hashlib
from pathlib import Path

CHUNK_FILE = "chunks.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()



def load_chunk_index(project_dir: Path):
    """
    Return structure:
    {
        "files": {
            "/abs/path/to/file": {
                "file_hash": "...",
                "chunks": ["hash1", "hash2", ...]
            }
        }
    }
    """
    path = project_dir / CHUNK_FILE
    base_index = {"files": {}}
    if path.exists():
        stored = json.loads(path.read_text() or "{}")
        # Ensure we always have the expected structure
        if isinstance(stored, dict):
            base_index.update({"files": stored.get("files", {})})
            return base_index
    return base_index



def save_chunk_index(project_dir: Path, index):
    path = project_dir / CHUNK_FILE
    path.write_text(json.dumps(index, indent=2))


def compute_file_hash(text: str) -> str:
    return sha256(text)


def compute_chunk_hash(chunk_text: str) -> str:
    return sha256(chunk_text)


def diff_file_chunks(old_chunks, new_chunks):
    old_set = set(old_chunks)
    new_set = set(new_chunks)

    to_add = list(new_set - old_set)
    to_delete = list(old_set - new_set)
    return to_add, to_delete

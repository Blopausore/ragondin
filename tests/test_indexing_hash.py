from ragondin.core.indexing.hashing import (
    sha256, compute_chunk_hash, compute_file_hash,
    diff_file_chunks, load_chunk_index, save_chunk_index
)
from pathlib import Path
import tempfile
import shutil
import json


def test_sha256_stable():
    assert sha256("abc") == sha256("abc")
    assert sha256("abc") != sha256("abcd")


def test_compute_hashes():
    assert compute_file_hash("hello") == compute_chunk_hash("hello")


def test_diff_file_chunks():
    old = ["a", "b", "c"]
    new = ["b", "c", "d"]

    to_add, to_delete = diff_file_chunks(old, new)

    assert to_add == ["d"]
    assert to_delete == ["a"]


def test_save_and_load_chunk_index():
    tmp = Path(tempfile.mkdtemp())
    proj = tmp

    index = {
        "files": {
            "/abs/path": {
                "file_hash": "123",
                "chunks": ["a", "b"]
            }
        }
    }

    save_chunk_index(proj, index)

    loaded = load_chunk_index(proj)
    assert loaded == index

    shutil.rmtree(tmp)

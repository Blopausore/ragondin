# tests/test_indexing/test_hashing.py

from ragondin.core.indexing.hashing import (
    compute_chunk_hash,
    compute_file_hash,
    diff_file_chunks,
)


def test_compute_chunk_hash_changes():
    h1 = compute_chunk_hash("hello")
    h2 = compute_chunk_hash("hello world")
    assert h1 != h2


def test_compute_file_hash_changes():
    h1 = compute_file_hash("abc")
    h2 = compute_file_hash("abcd")
    assert h1 != h2


def test_diff_file_chunks():
    old = ["a", "b", "c"]
    new = ["b", "c", "d"]

    to_add, to_del = diff_file_chunks(old, new)

    assert "d" in to_add
    assert "a" in to_del

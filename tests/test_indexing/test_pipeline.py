# tests/test_indexing/test_pipeline.py

import json
from pathlib import Path

from ragondin.core.indexing.pipeline import process_project
from ragondin.core.project.model import Project
from ragondin.core.indexing.hashing import load_chunk_index

# inject our mocks
from tests.test_indexing.fake_vectordb import FakeVectorDB
from tests.test_indexing.fake_embeddings import FakeEmbeddings

import ragondin.core.indexing.vectordb as vectordb_module


def test_pipeline_first_index(tmp_path, monkeypatch):
    monkeypatch.setattr(vectordb_module, "FAISS", FakeVectorDB)
    monkeypatch.setattr(vectordb_module, "NormalizedEmbeddings", FakeEmbeddings)

    # create project
    proj = Project.create("p", base_dir=tmp_path)

    # create file
    f = tmp_path / "src"
    f.mkdir()
    file1 = f / "a.md"
    file1.write_text("# Hello")

    proj.add_source(f)

    result = process_project(proj)

    idx = load_chunk_index(proj.root)
    assert "files" in idx
    assert str(file1) in idx["files"]

    # ensure chunks created
    entry = idx["files"][str(file1)]
    assert len(entry["chunks"]) >= 1


def test_pipeline_incremental(tmp_path, monkeypatch):
    monkeypatch.setattr(vectordb_module, "FAISS", FakeVectorDB)
    monkeypatch.setattr(vectordb_module, "NormalizedEmbeddings", FakeEmbeddings)

    proj = Project.create("p", base_dir=tmp_path)

    src = tmp_path / "src"
    src.mkdir()
    f = src / "a.md"
    f.write_text("# Hello")
    proj.add_source(src)

    process_project(proj)
    idx1 = load_chunk_index(proj.root)

    # no change → no new chunks
    process_project(proj)
    idx2 = load_chunk_index(proj.root)

    assert idx1 == idx2  # fully unchanged index

    # modify file → new index
    f.write_text("# Hello world")
    process_project(proj)
    idx3 = load_chunk_index(proj.root)

    assert idx3 != idx2

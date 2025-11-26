# tests/test_vectordb.py
from ragondin.core.vectordb import build_vector_db, load_vector_db
from tests.fake_embeddings import FakeEmbeddings
from ragondin.core.splitter import load_and_split_file
from pathlib import Path
import shutil, tempfile
import json

def test_faiss_index_build_and_load(temp_project_dir):
    temp_ragondin = Path(tempfile.mkdtemp())
    project_name = "demo"

    # Simulate ragondin paths
    project_dir = temp_ragondin / project_name
    project_dir.mkdir(parents=True)

    docs = []
    for file in temp_project_dir.glob("**/*"):
        if file.is_file():
            docs.extend(load_and_split_file(file, temp_project_dir))

    # Patch embedding inside the vector db
    build_vector_db(project_name, docs, emb_cls=FakeEmbeddings, base_dir=temp_ragondin)

    # Load index
    db = load_vector_db(project_name, emb_cls=FakeEmbeddings, base_dir=temp_ragondin)

    results = db.similarity_search("hello", k=3)
    assert len(results) == 3

    shutil.rmtree(temp_ragondin)

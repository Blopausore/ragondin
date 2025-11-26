# tests/test_retriever.py
from ragondin.core.retriever import build_retriever
from tests.fake_embeddings import FakeEmbeddings
from ragondin.core.vectordb import build_vector_db, load_vector_db
from ragondin.core.splitter import load_and_split_file
from pathlib import Path
import shutil, tempfile

def test_retriever_basic(temp_project_dir):

    base = Path(tempfile.mkdtemp())
    proj = "demo"
    (base / proj).mkdir()

    docs = []
    for f in temp_project_dir.glob("**/*"):
        if f.is_file():
            docs.extend(load_and_split_file(f, temp_project_dir))

    build_vector_db(proj, docs, emb_cls=FakeEmbeddings, base_dir=base)
    db = load_vector_db(proj, emb_cls=FakeEmbeddings, base_dir=base)

    retriever = build_retriever(db, k=3)
    res = retriever.invoke("test")

    assert len(res) == 3

    shutil.rmtree(base)

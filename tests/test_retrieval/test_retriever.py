# tests/test_retrieval/test_retriever.py

from ragondin.config.manager import set_value
from ragondin.core.retrieval.retriever import build_retriever
from langchain_community.docstore.document import Document

from tests.test_indexing.fake_vectordb import FakeVectorDB
from tests.test_indexing.fake_embeddings import FakeEmbeddings

import ragondin.core.retrieval.retriever as retriever_module
import ragondin.core.retrieval.reranker as reranker_module


class FakeReranker:
    def __init__(self):
        pass

    def compress_documents(self, docs, query=None):
        # always keep only the first doc for test
        return docs[:1]


class FakeCompressionRetriever:
    """
    Simule un ContextualCompressionRetriever
    """

    def __init__(self, base_retriever, reranker):
        self.base_retriever = base_retriever
        self.reranker = reranker

    def get_relevant_documents(self, query):
        docs = self.base_retriever.get_relevant_documents(query)
        return self.reranker.compress_documents(docs, query)


def FakeApplyReranker(base_retriever, reranker):
    return FakeCompressionRetriever(base_retriever, reranker)


def test_retriever_no_reranker(monkeypatch):
    # patch vectorstore.as_retriever
    db = FakeVectorDB()
    docs = [Document(page_content=f"doc{i}") for i in range(3)]
    db.add_documents(docs)

    retr = db.as_retriever(search_kwargs={"k": 2})

    # disable reranker
    set_value("use_reranker", False)
    set_value("retriever_k", 2)

    r = build_retriever(db)

    # Should return first 2 documents (FakeVectorDB behavior)
    result = r.get_relevant_documents("hi")

    assert len(result) == 2
    assert result[0].page_content == "doc0"
    assert result[1].page_content == "doc1"


def test_retriever_with_reranker(monkeypatch):
    db = FakeVectorDB()
    docs = [Document(page_content=f"D{i}") for i in range(4)]
    db.add_documents(docs)

    # patch imports
    monkeypatch.setattr(reranker_module, "build_reranker", lambda *a, **k: FakeReranker())
    monkeypatch.setattr(reranker_module, "apply_reranker", FakeApplyReranker)

    set_value("use_reranker", True)
    set_value("retriever_k", 4)

    r = build_retriever(db)

    out = r.get_relevant_documents("q")

    # FakeReranker keeps only 1 result
    assert len(out) == 1
    assert out[0].page_content == "D0"

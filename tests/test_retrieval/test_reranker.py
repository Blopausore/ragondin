# tests/test_retrieval/test_reranker.py

from ragondin.core.retrieval.retriever import build_retriever
from ragondin.core.config.manager import set_value, get_value
from ragondin.core.retrieval.reranker import apply_reranker
from langchain_community.docstore.document import Document


class FakeBaseRetriever:
    """
    Returns docs in fixed order: [A, B, C].
    """

    def __init__(self):
        self.docs = [
            Document(page_content="A"),
            Document(page_content="B"),
            Document(page_content="C")
        ]

    def get_relevant_documents(self, query):
        return self.docs


class FakeReranker:
    """
    Simple reranker that reverses the docs.
    """
    def rerank(self, query, docs):
        return list(reversed(docs))

    def compress_documents(self, docs, query=None):
        return docs[::-1]


def test_reranker_applies_order():
    base = FakeBaseRetriever()
    reranker = FakeReranker()

    comp = apply_reranker(base, reranker)

    out = comp.get_relevant_documents("query")

    assert out[0].page_content == "C"
    assert out[1].page_content == "B"
    assert out[2].page_content == "A"

# tests/test_indexing/fake_embeddings.py

class FakeEmbeddings:
    """
    Mock embedding model returning deterministic vectors.
    Used to avoid calling HuggingFace models.
    """

    def embed_documents(self, texts):
        # deterministic vector = length-based
        return [[len(t) * 0.01 for _ in range(8)] for t in texts]

    def embed_query(self, text):
        return [len(text) * 0.01 for _ in range(8)]

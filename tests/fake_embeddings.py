# tests/fake_embeddings.py
from langchain_core.embeddings import Embeddings
import numpy as np

class FakeEmbeddings(Embeddings):
    """Deterministic embedding to test FAISS without downloading models."""

    def embed_documents(self, texts):
        return [self._encode(t) for t in texts]

    def embed_query(self, text):
        return self._encode(text)

    def _encode(self, text):
        # Very cheap deterministic vector
        v = np.zeros(32, dtype="float32")
        v[0] = len(text)
        v[1] = sum(ord(c) for c in text) % 97
        return v.tolist()

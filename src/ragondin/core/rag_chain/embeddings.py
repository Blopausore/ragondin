import numpy as np
from typing import List
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

def _normalize(mat: np.ndarray) -> np.ndarray:
    mat = np.asarray(mat)
    if mat.ndim == 1:
        mat = mat.reshape(1, -1)

    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12
    return mat / norms


class NormalizedEmbeddings(Embeddings):
    def __init__(self, model="BAAI/bge-base-en-v1.5"):
        print(">>> LOADING MODEL:", model)
        self.base = HuggingFaceEmbeddings(model_name=model)
        print(">>> MODEL PATH:", self.base.model_name)


    def embed_documents(self, texts: List[str]):
        return _normalize(self.base.embed_documents(texts))

    def embed_query(self, text: str):
        return _normalize([self.base.embed_query(text)])[0]
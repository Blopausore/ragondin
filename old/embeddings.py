import numpy as np
from typing import List
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

def _normalize(mat: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12
    return mat / norms

class NormalizedEmbeddings(Embeddings):
    def __init__(self, model="BAAI/bge-base-en-v1.5"):
        print(">>> LOADING MODEL:", model)
        self.base = HuggingFaceEmbeddings(model_name=model)
        print(">>> MODEL PATH:", self.base.model_name)


    def embed_documents(self, texts: List[str]):
        X = np.array(self.base.embed_documents(texts), dtype="float32")
        return _normalize(X).tolist()

    def embed_query(self, text: str):
        x = np.array(self.base.embed_query(text), dtype="float32")[None, :]
        return _normalize(x)[0].tolist()

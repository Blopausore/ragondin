from pathlib import Path

try:  # Optional dependency, allow tests to monkeypatch when missing
    import faiss  # noqa: F401
    from langchain_community.vectorstores import FAISS
    from langchain_community.docstore.in_memory import InMemoryDocstore
except ModuleNotFoundError:  # pragma: no cover - exercised implicitly via tests
    FAISS = None
    InMemoryDocstore = None

from ..project.model import Project
from ..rag_chain.embeddings import NormalizedEmbeddings

def build_vector_db(project: Project, docs, emb_cls=None):

    # Detect Project object
    if not isinstance(project, Project):
        raise TypeError(f"{type(project)} is not a Project")

    if FAISS is None:
        raise ImportError("FAISS is required to build the vector database. Install 'faiss-cpu'.")

    # Permet d’injecter FakeEmbeddings dans les tests
    emb = emb_cls() if emb_cls else NormalizedEmbeddings()

    vector_store = FAISS.from_documents(docs, emb)

    vector_store.save_local(str(project.index_dir))
    
    
def load_vector_db(project: Project, emb_cls=None) -> FAISS:

    if not isinstance(project, Project):
        raise TypeError(f"{type(project)} is not a Project")

    if FAISS is None:
        raise ImportError("FAISS is required to load the vector database. Install 'faiss-cpu'.")

    emb = emb_cls() if emb_cls else NormalizedEmbeddings()

    return FAISS.load_local(
        str(project.index_dir),
        emb,
        allow_dangerous_deserialization=True
    )
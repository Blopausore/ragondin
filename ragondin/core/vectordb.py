import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from pathlib import Path
from .project import BASE_DIR
from .embeddings import NormalizedEmbeddings

def build_vector_db(project: str, docs):
    emb = NormalizedEmbeddings()

    probe = emb.embed_query("probe")
    dim = len(probe)
    index = faiss.IndexFlatIP(dim)

    vector_store = FAISS(
        embedding_function=emb,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )

    vector_store.add_documents(docs)
    vector_store.save_local(str(BASE_DIR / project / "index"))

def load_vector_db(project: str):
    emb = NormalizedEmbeddings()

    return FAISS.load_local(
        str(BASE_DIR / project / "index"),
        emb,
        allow_dangerous_deserialization=True
    )

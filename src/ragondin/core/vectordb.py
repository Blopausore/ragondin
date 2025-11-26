import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from pathlib import Path
from .project import BASE_DIR
from .embeddings import NormalizedEmbeddings



# def build_vector_db(project: str, docs):
#     emb = NormalizedEmbeddings()

#     probe = emb.embed_query("probe")
#     dim = len(probe)
#     index = faiss.IndexFlatIP(dim)

#     vector_store = FAISS(
#         embedding_function=emb,
#         index=index,
#         docstore=InMemoryDocstore(),
#         index_to_docstore_id={}
#     )

#     vector_store.add_documents(docs)
#     vector_store.save_local(str(BASE_DIR / project / "index"))


def build_vector_db(project: str, docs, emb_cls=None, base_dir: Path = None):
    base_dir = base_dir or BASE_DIR

    # Permet d’injecter FakeEmbeddings dans les tests
    if emb_cls is None:
        emb = NormalizedEmbeddings()
    else:
        emb = emb_cls()

    vector_store = FAISS.from_documents(
        docs,
        emb
    )

    project_dir = base_dir / project / "index"
    project_dir.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(project_dir))

def load_vector_db(project: str, emb_cls=None, base_dir: Path = None):
    base_dir = base_dir or BASE_DIR

    index_dir = base_dir / project / "index"

    # même logique d’injection
    if emb_cls is None:
        emb = NormalizedEmbeddings()
    else:
        emb = emb_cls()

    return FAISS.load_local(
        str(index_dir),
        emb,
        allow_dangerous_deserialization=True
    )
from . import reranker

from ragondin.config.manager import get_value
from ragondin.config.manager import get_config


def build_retriever(vector_store):
    cfg = get_config()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": cfg["retriever_k"]}
    )

    if cfg.get("use_reranker", False):
        model_name = cfg.get("reranker_model")
        # reranker_model = reranker.build_reranker(model_name)
        if model_name:
            reranker_cfg = {
                "use_reranker": True,
                "model": cfg.get("reranker_model"),
                "top_n": cfg.get("reranker_top_n", 5),
                "reranker_device": cfg.get("reranker_device", "cpu"),
            }

            reranker_model = reranker.build_reranker(reranker_cfg)
            return reranker.apply_reranker(retriever, reranker_model)
    # if disabled → just return retriever
    return retriever



def format_docs(docs, max_chars=5000):
    parts, total = [], 0
    for i, d in enumerate(docs, 1):
        block = f"[Chunk {i}]\n{d.page_content}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)
    return "\n".join(parts)

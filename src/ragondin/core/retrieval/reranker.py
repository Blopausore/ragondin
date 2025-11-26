# ragondin/core/retrieval/reranker.py

def build_reranker(config):
    """Load reranker backend only if enabled."""
    if not config.get("reranker_enabled", False):
        return None
    if not config.get("use_reranker", False):
        return None


    try:
        from BCEmbedding.tools.langchain import BCERerank
    except Exception as e:
        raise RuntimeError(
            "Reranker backend BCEmbedding could not be loaded. "
            "Install BCEmbedding==0.1.5 OR disable reranking.\n"
            f"Original error: {e}"
        )

    return BCERerank(
        model=config.get("reranker_model", "maidalun1020/bce-reranker-base_v1"),
        top_n=config.get("reranker_top_n", 5),
        device=config.get("reranker_device", "cpu"),
    )

def apply_reranker(base_retriever, reranker):
    """
    Wraps the base retriever in a new retriever that applies reranking.
    """
    class RerankingRetriever:
        def __init__(self, retriever, reranker):
            self.retriever = retriever
            self.reranker = reranker

        def get_relevant_documents(self, query):
            docs = self.retriever.get_relevant_documents(query)
            reranked = self.reranker.rerank(query, docs)
            return reranked

    return RerankingRetriever(base_retriever, reranker)


def _apply_reranker(reranker, query: str, docs: list):
    """Apply reranker to the retrieved documents."""
    if reranker is None:
        return docs  # no reranking

    passages = [d.page_content for d in docs]
    reranked = reranker.rerank(query, passages)

    # BCERerank.rerank returns sorted passages → map back to docs
    order = []
    for passage in reranked:
        for d in docs:
            if d.page_content == passage:
                order.append(d)
                break

    return order
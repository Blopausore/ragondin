from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank

from ragondin.config.manager import DEFAULT_CONFIG 

def build_reranker(config):
    """Build compressor-based reranker with FlashRank.
    No model_name supported in FlashrankRerank!
    """

    if not config.get("use_reranker", False):
        return None

    try:
        compressor = FlashrankRerank()
        compressor.top_n = config.get("reranker_top_n", DEFAULT_CONFIG.get("reranker_top_n"))
    except Exception as e:
        raise RuntimeError(
            "Could not initialize FlashrankRerank. Install FlashRank:\n"
            "  pipx runpip ragondin install flashrank\n"
            f"Original error: {e}"
        )

    return compressor


def apply_reranker(base_retriever, compressor):
    """
    Use LangChain's ContextualCompressionRetriever.
    """

    if compressor is None:
        return base_retriever

    return ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=base_retriever
    )

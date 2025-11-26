def build_retriever(vector_store, k=5, fetch_k=15, lambda_mult=0.5):
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": fetch_k,
            "lambda_mult": lambda_mult
        }
    )

def format_docs(docs, max_chars=5000):
    parts, total = [], 0
    for i, d in enumerate(docs, 1):
        block = f"[Chunk {i}]\n{d.page_content}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)
    return "\n".join(parts)

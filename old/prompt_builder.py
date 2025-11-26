def build_final_prompt(query: str, context: str) -> str:
    return f"""
Write a complete answer with reasoning, including code if needed.

--------------------
CONTEXT:
{context}
--------------------

USER QUESTION:
{query}

Use the retrieved context to answer. 
If something is not explicitly stated but can be inferred from multiple chunks, include it.
If the question is general ("Parle moi de ce projet"), produce a structured overview based on all chunks.
"""

def build_final_prompt(query: str, context: str) -> str:
    return f"""
You are ChatGPT. Use the following context extracted from my project. 
Write a complete answer with reasoning, including code if needed.

--------------------
CONTEXT:
{context}
--------------------

USER QUESTION:
{query}

Now answer with full detail using the context above.
"""

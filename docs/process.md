
# How Ragondin Works

Ragondin is structured around three core concepts:

## 1. Projects

Each project represents an isolated knowledge space.
A project contains:

* an index directory
* a chunk index file
* a list of document sources
* configuration metadata

A project does not own the document sources; it references external paths.

## 2. Indexing Pipeline

The indexing pipeline performs the following steps:

1. Collect files from all registered source directories
2. Validate and filter supported extensions
3. Split files into well-structured textual chunks
   (Markdown headers, Python code blocks, JSON sections, CSV headers, etc.)
4. Add contextual headers and relative paths
5. Compute stable hashes to detect changed or unchanged chunks
6. Embed new or modified chunks using the configured embedding model
7. Build or update the FAISS vector index
8. Save a chunk index for incremental re-processing

This makes the pipeline both efficient and reproducible.

## 3. Retrieval Pipeline

Ragondin uses a two-stage retrieval system:

### Stage 1: Vector Search

The FAISS index returns the top-k semantically similar chunks using cosine similarity.

### Stage 2 (optional): Reranking

If enabled, a cross-encoder reranker (such as BGE-reranker) re-orders the retrieved chunks based on semantic relevance to the user query.

### Final Output

The `ragondin ask` command produces a complete structured prompt containing:

* the user question
* selected contextual chunks
* final instructions for an LLM

Ragondin does not generate text; it produces high-quality prompts for any LLM.

---




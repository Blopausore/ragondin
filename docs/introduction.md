# Ragondin – Local, Configurable Retrieval-Augmented Generation Toolkit

Ragondin is a lightweight, fully local Retrieval-Augmented Generation (RAG) toolkit designed for developers who want complete control over their indexing, retrieval, and document-processing pipeline.
It provides a structured way to create projects, register document sources, index them, and query the knowledge base through a streamlined command-line interface.

Ragondin focuses on transparency, configurability, and extensibility.
It integrates modern embedding models, optional reranking, and a clean project-oriented architecture.

---

## Features

* Project-based organization with isolated indexing space
* Automatic file discovery, splitting and preprocessing
* Incremental indexing pipeline using FAISS vector store
* Pluggable embedding models (default: BGE base)
* Optional cross-encoder reranking (BGE reranker)
* Extensible configuration system (embedding model, reranker, k-retrieval, chunk sizes)
* Clean CLI for project management and retrieval tasks
* Human-readable chunk metadata with relative paths


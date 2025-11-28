# File Structure (Overview)

```
ragondin/
  core/
    project/
      model.py          Project definition
      manager.py        Project creation and utilities
      active.py         Active project tracking
    config/
      manager.py        Global configuration management
    indexing/
      collector.py      File discovery
      splitter.py       File splitting
      hashing.py        Chunk hashing
      pipeline.py       Indexing engine
      vectordb.py       FAISS interfaces
    retrieval/
      retriever.py      Vector retriever
      reranker.py       Cross-encoder reranking
    embeddings/
      embeddings.py     Embedding model loading
  cli/
    main.py             CLI entrypoint
    process_cmd.py      Indexing commands
    project_cmd.py      Projects managing commands
    sources_cmd.py      Sources managing commands
    ask_cmd.py          Query commands
    config_cmd.py       Configuration commands
    debug_cmd.py        Debug tools commands
    utils.py            Shared CLI utilities
```
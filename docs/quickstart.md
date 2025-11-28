
# Quick Start

## 1. Create a new Ragondin project

```sh
ragondin create myproject
ragondin connect myproject
```

## 2. Manage sources
When you are connected to a specific project you can manage its sources.

### Add
You can add any directory containing files:

```sh
ragondin source add ~/work/documentation.txt
ragondin source add ../some/other/source_dir
```

### List
You can list them.

```sh
ragondin source list
>>> - ~/work/documentation.txt
>>> - ~/work/a/path/to/some/other/source_dir
```


### Del

```sh
ragondin source del ~/work/documentation.txt
```

### Files supported

Ragondin indexes all supported files recursively (`.md`, `.py`, `.tex`, `.json`, `.csv`, etc.).


## 3. Process and index the project

When all your sources are added you can process them.

```sh
ragondin process
```
This commands can take some time.

This runs the incremental indexing pipeline:

* collect all files
* split into chunks
* add metadata
* embed chunks
* build/update FAISS index

## 4. Ask questions

```sh
ragondin ask "Explain the architecture of this project."
```

Ragondin retrieves the most relevant chunks and generates a complete prompt containing:

* your question
* retrieved context
* recommended instructions for your LLM

## 5. Use optional reranking

Enable:

```sh
ragondin config reranker true
```

Disable:

```sh
ragondin config reranker false
```

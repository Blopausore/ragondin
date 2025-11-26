# Ragondin

Ragondin is a RAG create for personal use.

## Usage

Ragondin provides a command-line interface to create, inspect, index and query local RAG projects.
A *project* is a directory containing processed documents, embeddings, and a FAISS index.
Ragondin always works on the currently active project.

### Global Help

```bash
ragondin --help
```

This displays the list of available commands and general information about the CLI.

---

## Project Management

### Create a new project

```bash
ragondin create <project_name>
```

Creates a new project under `~/.ragondin/projects/` and initializes its structure.

### Connect to an existing project

```bash
ragondin connect <project_name>
```

Sets the project as “active”.
All subsequent commands operate on this project.

### Disconnect

```bash
ragondin disconnect
```

Removes the active project context.

### Show project status

```bash
ragondin status
```

Displays the active project and its registered source directories.

---

## Managing Source Directories

Each project maintains a list of root directories from which documents are collected.

### Add a source directory

```bash
ragondin add <path>
```

Registers a new directory whose files will be processed, chunked and embedded.

### Remove a source directory

```bash
ragondin del <path>
```

Unregisters a directory previously added to the project.

### List sources

```bash
ragondin list
```

Shows all directories currently tracked by the active project.

---

## Processing and Indexing

### Process a project

```bash
ragondin process
```

Runs all stages:

1. Collect files
2. Split documents into chunks
3. Embed chunks
4. Build or update the FAISS index

### Rebuild the index

```bash
ragondin rebuild
```

Deletes the existing index and regenerates all embeddings and FAISS structures from scratch.

---

## Querying the Project

### Ask a question

```bash
ragondin ask "<your question>"
```

Retrieves the most relevant chunks and prints a completed prompt containing:

* the retrieved context
* the user’s question
* instructions for ChatGPT

This prompt can be pasted directly into a language model for final answering.

---

## Debugging Tools

Ragondin exposes internal debugging utilities under the `debug` command:

```bash
ragondin debug --help
```

### Inspect generated chunks (before embedding)

```bash
ragondin debug chunks
```

Shows how files are split, including metadata and chunk boundaries.

### Inspect embeddings

```bash
ragondin debug embeddings
```

Displays information such as vector norms, vector previews, and associated metadata.

### Debug retrieval

```bash
ragondin debug retriever "<query>"
```

Shows:

* retrieved chunk list
* scores
* raw text content
* FAISS results and MMR output

Useful for understanding why certain chunks are selected.

### Debug the CLI itself

```bash
ragondin debug debug-cli
```



# Configuration

Ragondin stores global configuration in:

```
~/.ragondin/config.json
```

You can modify settings through the CLI:

### Set embedding model

```
ragondin config embedding BAAI/bge-base-en-v1.5
```

### Set top-k retrieval

```
ragondin config k 8
```

### Enable or disable reranking

```
ragondin config reranker true
```

### Display full configuration

```
ragondin config show
```

Configuration is applied to all subsequent indexing and retrieval operations.

---

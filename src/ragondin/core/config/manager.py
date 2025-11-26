from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".ragondin"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "active_project": None,
    "embedding_model": "BAAI/bge-base-en-v1.5",
    "use_reranker": False,
    "reranker_model": "BAAI/bge-reranker-base",
    "retriever_k": 5,
    "chunk_size": 800,
    "chunk_overlap": 100,
}

def ensure_config():
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))

def get_config():
    ensure_config()
    file_cfg = json.loads(CONFIG_FILE.read_text())
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(file_cfg)
    return cfg


def set_config(updates: dict):
    cfg = get_config()
    cfg.update(updates)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))

def get_value(key, default=None):
    return get_config().get(key, default)

def set_value(key, value):
    set_config({key: value})

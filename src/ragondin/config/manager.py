import json

from .constants import CONFIG_DIR, CONFIG_FILE
from .defaults import DEFAULT_CONFIG

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


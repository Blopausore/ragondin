import json
from pathlib import Path

from .model import Project

CONFIG_DIR = Path.home() / ".ragondin"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config():
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump({"active_project": None}, f)

def set_active_project(name: str):
    ensure_config()
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    data["active_project"] = name
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_active_project():
    ensure_config()
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data.get("active_project")

def disconnect():
    set_active_project(None)
        
def get_status():
    return get_active_project()


def load_active_project() -> Project | None:
    name = get_active_project()
    if name is None:
        return None
    return Project.load(name)
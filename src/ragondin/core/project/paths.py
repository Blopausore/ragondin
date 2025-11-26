# src/ragondin/core/project/paths.py
import os
from pathlib import Path

def get_projects_root() -> Path:
    return Path(os.environ.get("RAGONDIN_HOME", Path.home() / ".ragondin" / "projects"))

def get_project_dir(name: str) -> Path:
    return get_projects_root() / name

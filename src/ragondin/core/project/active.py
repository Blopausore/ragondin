# src/ragondin/core/project/active.py

from ragondin.core.config.manager import get_value, set_value
from .model import Project

def set_active_project(name: str | None):
    set_value("active_project", name)

def get_active_project() -> str | None:
    return get_value("active_project")

def disconnect():
    set_active_project(None)

def get_status():
    return get_active_project()

def load_active_project() -> Project | None:
    name = get_active_project()
    if not name:
        return None
    return Project.load(name)

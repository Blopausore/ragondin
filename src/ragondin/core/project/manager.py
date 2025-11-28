# ragondin/core/project/manager.py
from ragondin.config.constants import BASE_DIR

def get_list_projects():
    """Return a list of all project names in BASE_DIR."""
    if not BASE_DIR.exists():
        return []

    return [
        p.name for p in BASE_DIR.iterdir()
        if p.is_dir()
    ]

import os, shutil
from pathlib import Path

from .project import BASE_DIR, get_project_paths
from .project import list_sources


VALID_EXT = {
    ".md", ".txt", ".py", ".json", ".rst", ".yaml", ".yml",
    ".toml", ".cfg", ".ini", ".sh"
}

SPECIAL_FILES = {"Makefile", "Dockerfile", "README", "LICENSE"}


EXTS = [".md", ".py", ".txt", ".tex", ".xml", ".json", ".csv"]

def collect_files(project: str):
    """Return all valid files from all registered source directories."""
    all_files = []
    for src in list_sources(project):
        root = Path(src)
        if not root.exists():
            continue

        # Si c'est un fichier directement
        if root.is_file():
            if is_valid_file(root):
                all_files.append(root)
            continue

        # Scan récursif
        for f in root.rglob("*"):
            if f.is_file() and is_valid_file(f):
                all_files.append(f)

    return all_files


def is_valid_file(path: Path) -> bool:
    """Check if file should be included in the indexing."""
    if path.name in SPECIAL_FILES:
        return True
    if path.suffix.lower() in VALID_EXT:
        return True
    return False

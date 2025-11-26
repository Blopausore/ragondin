from typing import List, Tuple
from pathlib import Path
from ragondin.core.project.model import Project

VALID_EXT = {
    ".md", ".txt", ".py", ".json", ".rst", ".yaml", ".yml",
    ".toml", ".cfg", ".ini", ".sh", ".tex", ".xml", ".csv"
}

SPECIAL_FILES = {"Makefile", "Dockerfile", "README", "LICENSE"}


def is_valid_file(path: Path) -> bool:
    if path.name in SPECIAL_FILES:
        return True
    return path.suffix.lower() in VALID_EXT


def collect_files(project: Project) -> List[Tuple[Path, Path]]:
    """Return all valid files from all registered sources.
    
    Return:
        (source_file, file_path)
    
    """
    all_files = []

    for src in project.list_sources():
        src_root = Path(src)
        if not src_root.exists():
            continue

        if src_root.is_file():
            if is_valid_file(src_root):
                all_files.append((src_root, src_root))
            continue

        for f in src_root.rglob("*"):
            if f.is_file() and is_valid_file(f):
                all_files.append((src_root, f))

    return all_files

# src/ragondin/core/project/model.py

from dataclasses import dataclass
from pathlib import Path
import json

BASE_DIR = Path.home() / ".ragondin" / "projects"


@dataclass
class Project:
    """Represents a Ragondin project.
    
    Attributes:
        name (str): The name of the project.
        root (Path): The root directory of the project.
        
    Properties:
        paths_file (Path): Path to the file storing source paths.
        index_dir (Path): Path to the index directory.
        raw_docs_dir (Path): Path to the raw documents directory.
        config_file (Path): Path to the configuration file.
    
    """
    
    @classmethod
    def get_base_dir(cls) -> Path:
        return BASE_DIR
    
    name: str
    root: Path
    
    def __init__(self, name: str, root: Path):
        self.name = name
        self.root = Path(root)

    @property
    def paths_file(self) -> Path:
        return self.root / "paths.txt"

    @property
    def index_dir(self) -> Path:
        return self.root / "index"

    @property
    def raw_docs_dir(self) -> Path:
        return self.root / "raw_docs"

    @property
    def config_file(self) -> Path:
        return self.root / "config.json"

    # ---- CREATE -------------------------------------------------------------

    @staticmethod
    def create(name: str, base_dir: Path = None) -> "Project":
        if base_dir is None:
            base_dir = BASE_DIR
        root = base_dir / name
        if root.exists():
            raise ValueError(f"Project '{name}' already exists.")

        (root / "raw_docs").mkdir(parents=True)
        (root / "index").mkdir()
        (root / "paths.txt").touch()
        (root / "chunks.json").write_text("{}")
        (root / "config.json").write_text(json.dumps({"name": name}, indent=2))

        return Project(name=name, root=root)

    # ---- LOAD ---------------------------------------------------------------

    @staticmethod
    def load(name: str, base_dir: Path = None) -> "Project":
        if base_dir is None:
            base_dir = BASE_DIR
        root = base_dir / name
        if not root.exists():
            raise ValueError(f"Project '{name}' does not exist.")
        return Project(name=name, root=root)

    # ---- SOURCES ------------------------------------------------------------

    def list_sources(self) -> list[Path]:
        if not self.paths_file.exists():
            return []
        return [Path(p) for p in self.paths_file.read_text().splitlines() if p.strip()]

    def add_source(self, path: Path):
        path = Path(path)
        path = path.resolve()
        if path in self.list_sources():
            return
        with open(self.paths_file, "a") as f:
            f.write(str(path) + "\n")

    def remove_source(self, path: Path):
        path = Path(path)
        abs_path = str(path.resolve())
        lines = self.list_sources()
        new_lines = [p for p in lines if str(p) != abs_path]
        self.paths_file.write_text("\n".join(str(p) for p in new_lines))

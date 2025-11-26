import json
from pathlib import Path

BASE_DIR = Path.home() / ".ragondin" / "projects"

def create_project(name: str):
    proj_dir = BASE_DIR / name
    if proj_dir.exists():
        raise ValueError(f"Project '{name}' already exists.")
    (proj_dir / "raw_docs").mkdir(parents=True)
    (proj_dir / "index").mkdir()
    (proj_dir / "paths.txt").touch()

    config = {"name": name}
    with open(proj_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)
    return proj_dir


def add_source(project: str, path: str):
    proj_dir = BASE_DIR / project
    if not proj_dir.exists():
        raise ValueError(f"Project '{project}' does not exist.")

    abs_path = str(Path(path).resolve())

    with open(proj_dir / "paths.txt", "a") as f:
        f.write(abs_path + "\n")
        
def remove_source(project: str, path: str):
    proj_dir = BASE_DIR / project

    paths_file = proj_dir / "paths.txt"

    if not paths_file.exists():
        return

    abs_path = str(Path(path).resolve())
    
    lines = [p.strip() for p in paths_file.read_text().splitlines()]
    new_lines = [p for p in lines if p != abs_path]

    with open(paths_file, "w") as f:
        for p in new_lines:
            f.write(p + "\n")


def list_sources(project: str):
    proj_dir = BASE_DIR / project
    paths_file = proj_dir / "paths.txt"
    if not paths_file.exists():
        return []
    return [p.strip() for p in paths_file.read_text().splitlines() if p.strip()]



def get_project_paths(project: str):
    paths_file = BASE_DIR / project / "paths.txt"
    
    if not paths_file.exists():
        return []
    
    with open(paths_file, "r") as f:
        return [x.strip() for x in f.readlines() if x.strip()]
    
# tests/conftest.py
import pytest

from ragondin.core.project.model import Project
from ragondin.config.manager import CONFIG_DIR, CONFIG_FILE, ensure_config


@pytest.fixture(autouse=True)
def clean_config(tmp_path, monkeypatch):
    """
    Each test gets a clean isolated config directory.
    """
    monkeypatch.setattr("ragondin.config.manager.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("ragondin.config.manager.CONFIG_FILE", tmp_path / "config.json")

    ensure_config()
    return tmp_path


@pytest.fixture
def project_dir(tmp_path):
    """Temporary project root."""
    return tmp_path / "proj"


@pytest.fixture
def project(project_dir):
    """A created project instance."""
    p = Project.create("proj", base_dir=project_dir.parent)
    return p


@pytest.fixture
def make_file(tmp_path):
    """
    Utility: write a file easily.
    """
    def _make(rel_path: str, content: str = "hello"):
        path = tmp_path / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path
    return _make

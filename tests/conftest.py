# tests/conftest.py
import pytest
from pathlib import Path
import shutil
import tempfile

@pytest.fixture
def temp_project_dir():
    """Create a temporary project structure with files."""
    root = Path(tempfile.mkdtemp())

    (root / "file1.py").write_text("def test():\n    return 42")
    (root / "file2.md").write_text("# Title\n\nSome content")
    (root / "sub").mkdir()
    (root / "sub" / "nested.txt").write_text("Hello nested")

    yield root

    shutil.rmtree(root)

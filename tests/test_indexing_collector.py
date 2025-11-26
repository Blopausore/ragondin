from ragondin.core.indexing.collector import collect_files, is_valid_file
from ragondin.core.project.manager import add_source
from pathlib import Path
import tempfile
import shutil


def test_collect_files(temp_project_dir):
    # Simulate Ragondin project
    tmp_root = Path(tempfile.mkdtemp())
    proj = "demo"
    (tmp_root / proj).mkdir()

    # Register the temp dir as source
    add_source(proj, str(temp_project_dir))

    files = collect_files(proj)
    names = sorted([f.name for f in files])

    # Only valid extensions
    assert "file1.py" in names
    assert "file2.md" in names
    assert "nested.txt" in names

    shutil.rmtree(tmp_root)

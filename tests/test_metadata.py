# tests/test_metadata.py
from ragondin.core.splitter import load_and_split_file

def test_metadata_added(temp_project_dir):
    file = temp_project_dir / "file1.py"
    docs = load_and_split_file(file, temp_project_dir)

    for d in docs:
        assert "path" in d.metadata
        assert "source" in d.metadata
        assert d.metadata["file"] == "file1.py"

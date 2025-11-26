from ragondin.core.indexing.splitter import load_and_split_file
from pathlib import Path


def test_load_and_split_with_header(temp_project_dir):
    file = temp_project_dir / "file1.py"
    docs = load_and_split_file(file, project_root=temp_project_dir)

    assert len(docs) > 0
    for d in docs:
        assert d.metadata["file"] == "file1.py"
        assert d.metadata["source"].endswith("file1.py")
        assert d.page_content.startswith("# FILE:")

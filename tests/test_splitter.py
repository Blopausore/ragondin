# tests/test_splitter.py
from ragondin.core.splitter import load_and_split_file
from pathlib import Path

def test_split_python(temp_project_dir):
    file = temp_project_dir / "file1.py"

    docs = load_and_split_file(file, temp_project_dir)

    assert len(docs) > 0
    assert any("def test" in d.page_content for d in docs)

def test_split_markdown(temp_project_dir):
    file = temp_project_dir / "file2.md"

    docs = load_and_split_file(file, temp_project_dir)

    assert len(docs) > 0
    assert docs[0].page_content.startswith("# FILE:")

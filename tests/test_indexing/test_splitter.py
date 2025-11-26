# tests/test_indexing/test_splitter.py

from pathlib import Path
from ragondin.core.indexing.splitter import load_and_split_file


def test_split_markdown(tmp_path):
    file = tmp_path / "doc.md"
    file.write_text("# Title\nSome content")
    docs = load_and_split_file(file, source_root=tmp_path)

    assert len(docs) >= 1
    assert "FILE:" in docs[0].page_content
    assert docs[0].metadata["file"] == "doc.md"


def test_split_python(tmp_path):
    file = tmp_path / "code.py"
    file.write_text("def f():\n    pass")
    docs = load_and_split_file(file, source_root=tmp_path)

    assert len(docs) == 1
    assert docs[0].metadata["file"] == "code.py"


def test_split_csv(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("a,b,c\n1,2,3\n4,5,6")
    docs = load_and_split_file(file, source_root=tmp_path)

    # header-only
    assert len(docs) == 1
    assert "a,b,c" in docs[0].page_content


def test_path_relative_to_source_root(tmp_path):
    src = tmp_path / "src"
    sub = src / "folder"
    sub.mkdir(parents=True)
    file = sub / "x.py"
    file.write_text("print('ok')")

    docs = load_and_split_file(file, source_root=src)

    assert docs[0].metadata["path"] == "folder/x.py"

# tests/test_indexing/test_collector.py

from ragondin.core.indexing.collector import collect_files
from ragondin.core.project.model import Project


def test_collect_files(tmp_path, monkeypatch):
    proj = Project.create("p", base_dir=tmp_path)

    # files
    f1 = tmp_path / "src1/a.md"
    f2 = tmp_path / "src1/b.py"
    f3 = tmp_path / "src2/c.json"

    f1.parent.mkdir(parents=True, exist_ok=True)
    f2.parent.mkdir(parents=True, exist_ok=True)
    f3.parent.mkdir(parents=True, exist_ok=True)

    f1.write_text("hello")
    f2.write_text("print('hi')")
    f3.write_text("{}")

    proj.add_source(tmp_path / "src1")
    proj.add_source(tmp_path / "src2")

    files = collect_files(proj)

    # We only validate the second element of each tuple (file path)
    returned_paths = {fp for (_, fp) in files}

    assert f1 in returned_paths
    assert f2 in returned_paths
    assert f3 in returned_paths
    assert len(returned_paths) == 3

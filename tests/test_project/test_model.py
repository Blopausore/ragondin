# tests/test_project/test_model.py

import json
from pathlib import Path
import pytest

from ragondin.core.project.model import Project, BASE_DIR


def test_project_create(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    p = Project.create("myproj")

    assert (tmp_path / "myproj").exists()
    assert (p.root / "raw_docs").exists()
    assert (p.root / "index").exists()
    assert (p.root / "paths.txt").exists()
    assert (p.root / "chunks.json").exists()
    assert (p.root / "config.json").exists()

    data = json.loads((p.root / "config.json").read_text())
    assert data["name"] == "myproj"


def test_project_create_existing(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    Project.create("myproj")
    with pytest.raises(ValueError):
        Project.create("myproj")


def test_project_load(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)
    p1 = Project.create("p")

    p2 = Project.load("p", base_dir=tmp_path)
    assert p1.name == p2.name
    assert p1.root == p2.root


def test_project_load_not_exists(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    with pytest.raises(ValueError):
        Project.load("doesnotexist", base_dir=tmp_path)


def test_list_sources(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    p = Project.create("p")
    p.paths_file.write_text("/a\n/b\n")

    sources = p.list_sources()
    assert Path("/a") in sources
    assert Path("/b") in sources
    assert len(sources) == 2


def test_add_source(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)
    p = Project.create("p")

    p.add_source(Path("/tmp/src"))
    assert "/tmp/src" in p.paths_file.read_text()

    # duplicated append should not break
    p.add_source(Path("/tmp/src"))
    txt = p.paths_file.read_text().strip().splitlines()
    assert len(txt) == 1


def test_remove_source(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    p = Project.create("p")
    p.paths_file.write_text("/a\n/b\n/c\n")

    p.remove_source(Path("/b"))

    txt = p.paths_file.read_text().strip().splitlines()
    assert "/b" not in txt
    assert len(txt) == 2

# tests/test_project/test_active.py

import json
from pathlib import Path
import pytest

from ragondin.core.project.active import (
    set_active_project,
    get_active_project,
    disconnect,
)
from ragondin.config.manager import CONFIG_FILE, ensure_config


def test_active_project_basic(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.config.manager.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("ragondin.config.manager.CONFIG_FILE", tmp_path / "config.json")

    ensure_config()
    set_active_project("p1")

    assert get_active_project() == "p1"

    disconnect()
    assert get_active_project() is None


def test_active_project_overwrite(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.config.manager.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("ragondin.config.manager.CONFIG_FILE", tmp_path / "config.json")

    ensure_config()

    set_active_project("hello")
    assert get_active_project() == "hello"

    set_active_project("world")
    assert get_active_project() == "world"

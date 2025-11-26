# tests/test_cli/test_cli_create.py

from click.testing import CliRunner
from ragondin.cli.main import cli
from ragondin.core.project.model import Project
from ragondin.core.config.manager import CONFIG_DIR, CONFIG_FILE, ensure_config

def test_cli_create_project(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    runner = CliRunner()
    result = runner.invoke(cli, ["create", "p1"])
    assert result.exit_code == 0
    assert (tmp_path / "p1").exists()
    assert "created" in result.output.lower()

# tests/test_cli/test_cli_status.py

from click.testing import CliRunner
from ragondin.cli.main import cli
from ragondin.core.project.model import Project


def test_cli_status_no_project(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    runner = CliRunner()
    result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0
    assert "no active project" in result.output.lower()


def test_cli_status_with_project(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    p = Project.create("proj", base_dir=tmp_path)

    # activate
    from ragondin.core.project.active import set_active_project
    set_active_project("proj")

    runner = CliRunner()
    result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0
    assert "active project: proj" in result.output.lower()

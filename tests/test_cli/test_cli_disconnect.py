# tests/test_cli/test_cli_disconnect.py

from click.testing import CliRunner
from ragondin.cli.main import cli
from ragondin.core.project.active import set_active_project, get_active_project


def test_cli_disconnect(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    set_active_project("x")

    runner = CliRunner()
    result = runner.invoke(cli, ["disconnect"])

    assert result.exit_code == 0
    assert get_active_project() is None

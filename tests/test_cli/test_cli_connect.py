# tests/test_cli/test_cli_connect.py

from click.testing import CliRunner
from ragondin.cli.main import cli
from ragondin.core.project.model import Project
from ragondin.config.manager import CONFIG_DIR, CONFIG_FILE, ensure_config

def test_cli_connect(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    # create project for test
    Project.create("proj", base_dir=tmp_path)

    runner = CliRunner()
    result = runner.invoke(cli, ["connect", "proj"])
    assert result.exit_code == 0
    assert "connected" in result.output.lower()

    # check active project
    from ragondin.config.manager import get_value
    assert get_value("active_project") == "proj"

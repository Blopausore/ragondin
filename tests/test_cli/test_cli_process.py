# tests/test_cli/test_cli_process.py

from click.testing import CliRunner
from ragondin.cli.main import cli
from ragondin.core.project.model import Project
from ragondin.core.project.active import set_active_project


def test_cli_process_project(tmp_path, monkeypatch):
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    proj = Project.create("proj", base_dir=tmp_path)
    set_active_project("proj")

    # mock process_project
    def fake_process(p):
        return {"files": {"x": {"file_hash": "abc", "chunks": []}}}

    monkeypatch.setattr("ragondin.cli.process_cmd.process_project", fake_process)

    runner = CliRunner()
    result = runner.invoke(cli, ["process"])
    assert result.exit_code == 0
    assert "processing project" in result.output.lower()

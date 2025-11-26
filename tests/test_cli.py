# tests/test_cli.py
from click.testing import CliRunner
from pathlib import Path
import json, tempfile, shutil

from ragondin.cli.main import cli

def test_cli_list_empty():
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    assert "No project connected" in result.output or result.exit_code == 0

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output

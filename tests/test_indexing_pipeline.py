from ragondin.core.indexing.pipeline import process_project
from ragondin.core.indexing.hashing import load_chunk_index
from ragondin.core.project.manager import create_project, add_source
from ragondin.core.indexing.collector import collect_files
from pathlib import Path
import tempfile
import shutil


def test_pipeline_full_process(temp_project_dir):
    tmp = Path(tempfile.mkdtemp())
    proj = "demo"

    # Create project
    proj_dir = create_project(proj)
    # Override default location to temp dir
    (tmp / proj).mkdir(exist_ok=True)

    # Add source
    add_source(proj, str(temp_project_dir))

    # Run pipeline
    index = process_project(proj)

    # chunks.json should exist
    chunk_file = proj_dir / "chunks.json"
    assert chunk_file.exists()

    # load saved index
    saved = load_chunk_index(proj_dir)
    assert "files" in saved
    assert len(saved["files"]) > 0

    # All files must have chunks
    for f, entry in saved["files"].items():
        assert "file_hash" in entry
        assert len(entry["chunks"]) > 0

    shutil.rmtree(tmp)

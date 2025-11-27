from click.testing import CliRunner
from ragondin.cli.main import cli
from ragondin.core.project.model import Project


def test_cli_ask(tmp_path, monkeypatch):
    # Patch base directory
    monkeypatch.setattr("ragondin.core.project.model.BASE_DIR", tmp_path)

    # Create project
    Project.create("proj", base_dir=tmp_path)

    # Patch active project resolution
    monkeypatch.setattr(
        "ragondin.core.project.active.load_active_project",
        lambda: Project("proj", base_dir=tmp_path)
    )

    monkeypatch.setattr(
        "ragondin.cli.utils.require_active_project",
        lambda: Project("proj", base_dir=tmp_path)
    )

    # Patch vector DB loader
    monkeypatch.setattr(
        "ragondin.core.indexing.vectordb.load_vector_db",
        lambda *a, **k: "FAKEDB"
    )

    # Fake retriever
    class FakeRetriever:
        def invoke(self, query):
            from langchain_community.docstore.document import Document
            return [Document(page_content="CTX")]

    monkeypatch.setattr(
        "ragondin.core.retrieval.retriever.build_retriever",
        lambda *a, **k: FakeRetriever()
    )

    monkeypatch.setattr(
        "ragondin.core.retrieval.retriever.format_docs",
        lambda docs: "FORMATTED_CTX"
    )

    # Patch prompt builder
    monkeypatch.setattr(
        "ragondin.core.rag_chain.prompt_builder.build_final_prompt",
        lambda q, ctx: f"PROMPT[{q}|{ctx}]"
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["ask", "What is happening?"])

    assert result.exit_code == 0

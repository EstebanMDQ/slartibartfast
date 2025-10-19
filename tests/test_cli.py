from typer.testing import CliRunner
import yaml

from slartibartfast import cli


def test_generate_command_creates_site(tmp_path, monkeypatch):
    src = tmp_path / "site"
    src.mkdir()
    cfg = {"theme": "minimal"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    (src / "page.md").write_text("# Title\n\nContent", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        cli.app, ["generate", str(src), "--output", str(tmp_path / "out")]
    )

    assert result.exit_code == 0
    assert "Site generation complete" in result.stdout


def test_serve_command_checks_path(tmp_path):
    runner = CliRunner()
    # non-existent source path should produce an error and non-zero exit
    result = runner.invoke(cli.app, ["serve", str(tmp_path / "nope")])
    assert result.exit_code != 0
    assert "is not a directory" in result.stdout


def test_serve_command_with_valid_path(tmp_path):
    # Create a valid source directory with config
    src = tmp_path / "site"
    src.mkdir()
    cfg = {"theme": "minimal"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    page_content = "---\npublished: true\n---\n# Title\n\nContent"
    (src / "page.md").write_text(page_content, encoding="utf-8")

    # Mock the server to avoid actually starting it
    import unittest.mock

    runner = CliRunner()
    with unittest.mock.patch("slartibartfast.server.serve") as mock_serve:
        result = runner.invoke(cli.app, ["serve", str(src)])

        # Should not exit with error
        assert result.exit_code == 0

        # Should call the serve function with correct arguments
        mock_serve.assert_called_once_with(str(src), "_build", 8000)

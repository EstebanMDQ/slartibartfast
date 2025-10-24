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


def test_generate_command_reports_static_directories(tmp_path):
    """Test that generate command reports static directories in output."""
    src = tmp_path / "site"
    src.mkdir()

    # Create site config
    cfg = {"theme": "minimal"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    # Create a page
    page_content = "---\npublished: true\n---\n# Test Page\n\nContent"
    (src / "page.md").write_text(page_content, encoding="utf-8")

    # Create static directories
    images_dir = src / "images"
    images_dir.mkdir()
    (images_dir / "logo.png").write_text("fake png content", encoding="utf-8")

    assets_dir = src / "assets"
    assets_dir.mkdir()
    (assets_dir / "style.css").write_text("body { color: red; }", encoding="utf-8")

    out = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(cli.app, ["generate", str(src), "--output", str(out)])

    # Should succeed
    assert result.exit_code == 0

    # Should report static directories in output
    assert "Site generation complete" in result.stdout
    assert "1 pages created" in result.stdout
    assert "2 static directories copied" in result.stdout
    assert "0 errors" in result.stdout

    # Verify static directories were actually copied
    assert (out / "images" / "logo.png").exists()
    assert (out / "assets" / "style.css").exists()


def test_generate_command_without_static_directories(tmp_path):
    """Test that generate command works when no static directories exist."""
    src = tmp_path / "site"
    src.mkdir()

    # Create site config
    cfg = {"theme": "minimal"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    # Create a page
    page_content = "---\npublished: true\n---\n# Test Page\n\nContent"
    (src / "page.md").write_text(page_content, encoding="utf-8")

    out = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(cli.app, ["generate", str(src), "--output", str(out)])

    # Should succeed
    assert result.exit_code == 0

    # Should not mention static directories when none exist
    assert "Site generation complete" in result.stdout
    assert "1 pages created" in result.stdout
    assert "static directories copied" not in result.stdout
    assert "0 errors" in result.stdout


def test_generate_command_reports_theme_assets(tmp_path):
    """Test that generate command reports theme assets in output."""
    src = tmp_path / "site"
    src.mkdir()

    # Create site config with custom theme
    cfg = {"theme": "test_theme"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    # Create a page
    page_content = "---\npublished: true\n---\n# Test Page\n\nContent"
    (src / "page.md").write_text(page_content, encoding="utf-8")

    # Create theme directory with assets
    theme_dir = tmp_path / "themes" / "test_theme"
    theme_dir.mkdir(parents=True)
    (theme_dir / "style.css").write_text("body { color: blue; }", encoding="utf-8")
    (theme_dir / "app.js").write_text("console.log('test');", encoding="utf-8")

    # Create required template
    (theme_dir / "page.html").write_text(
        """
<!DOCTYPE html>
<html>
<head><title>{{ meta.title }}</title></head>
<body>{{ content }}</body>
</html>
    """,
        encoding="utf-8",
    )

    out = tmp_path / "out"

    # Mock the config.THEMES_DIR
    import slartibartfast.config as config

    original_themes_dir = config.THEMES_DIR
    config.THEMES_DIR = str(tmp_path / "themes")

    try:
        runner = CliRunner()
        result = runner.invoke(cli.app, ["generate", str(src), "--output", str(out)])

        # Should succeed
        assert result.exit_code == 0

        # Should report theme assets in output
        assert "Site generation complete" in result.stdout
        assert "1 pages created" in result.stdout
        assert "2 theme assets copied" in result.stdout
        assert "0 errors" in result.stdout

        # Verify theme assets were actually copied
        assert (out / "style.css").exists()
        assert (out / "app.js").exists()

    finally:
        # Restore original config
        config.THEMES_DIR = original_themes_dir


def test_generate_command_with_static_dirs_and_theme_assets(tmp_path):
    """Test that generate command reports both static dirs and theme assets."""
    src = tmp_path / "site"
    src.mkdir()

    # Create site config with custom theme
    cfg = {"theme": "test_theme"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    # Create a page
    page_content = "---\npublished: true\n---\n# Test Page\n\nContent"
    (src / "page.md").write_text(page_content, encoding="utf-8")

    # Create static directory in site
    images_dir = src / "images"
    images_dir.mkdir()
    (images_dir / "logo.png").write_text("fake png", encoding="utf-8")

    # Create theme directory with assets
    theme_dir = tmp_path / "themes" / "test_theme"
    theme_dir.mkdir(parents=True)
    (theme_dir / "theme.css").write_text("/* theme styles */", encoding="utf-8")

    # Create required template
    (theme_dir / "page.html").write_text(
        """
<!DOCTYPE html>
<html>
<head><title>{{ meta.title }}</title></head>
<body>{{ content }}</body>
</html>
    """,
        encoding="utf-8",
    )

    out = tmp_path / "out"

    # Mock the config.THEMES_DIR
    import slartibartfast.config as config

    original_themes_dir = config.THEMES_DIR
    config.THEMES_DIR = str(tmp_path / "themes")

    try:
        runner = CliRunner()
        result = runner.invoke(cli.app, ["generate", str(src), "--output", str(out)])

        # Should succeed
        assert result.exit_code == 0

        # Should report both static directories and theme assets
        assert "Site generation complete" in result.stdout
        assert "1 pages created" in result.stdout
        assert "1 static directories copied" in result.stdout
        assert "1 theme assets copied" in result.stdout
        assert "0 errors" in result.stdout

        # Verify both were copied
        assert (out / "images" / "logo.png").exists()
        assert (out / "theme.css").exists()

    finally:
        # Restore original config
        config.THEMES_DIR = original_themes_dir

import yaml

from slartibartfast import generator


def test_generate_site_creates_html(tmp_path):
    src = tmp_path / "site"
    src.mkdir()

    # minimal theme is provided in the repository themes/minimal
    cfg = {"theme": "minimal"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    md = """---
title: Hello
author: Tester
published: true
---
# Hello

This is content.
"""
    (src / "hello.md").write_text(md, encoding="utf-8")

    out = tmp_path / "out"

    stats = generator.generate_site(str(src), str(out))

    assert isinstance(stats, dict)
    assert stats["pages"] == 1
    assert stats["errors"] == 0

    html = (out / "hello.html").read_text(encoding="utf-8")
    assert "<html" in html.lower() or "<!doctype html" in html.lower()
    assert "Hello" in html


def test_should_process():
    assert generator.should_process({"published": True}) is True
    assert generator.should_process({"published": False}) is False
    assert generator.should_process({}) is False
    assert (
        generator.should_process({"published": True, "publish_date": "2000-01-01"})
        is True
    )
    assert (
        generator.should_process({"published": True, "publish_date": "3000-01-01"})
        is False
    )


def test_copy_static_directories_copies_directories_without_config(tmp_path):
    """Test that directories without _config.yaml are copied to output."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "out"
    out.mkdir()

    # Create a static directory with files
    images_dir = src / "images"
    images_dir.mkdir()
    (images_dir / "logo.png").write_text("fake png content", encoding="utf-8")
    (images_dir / "banner.jpg").write_text("fake jpg content", encoding="utf-8")

    # Create another static directory
    assets_dir = src / "assets"
    assets_dir.mkdir()
    (assets_dir / "style.css").write_text("body { color: red; }", encoding="utf-8")
    (assets_dir / "app.js").write_text("console.log('hello');", encoding="utf-8")

    # Copy static directories
    copied_count = generator.copy_static_directories(str(src), str(out))

    # Verify the function returns correct count
    assert copied_count == 2

    # Verify directories were copied
    assert (out / "images").exists()
    assert (out / "assets").exists()

    # Verify files were copied
    assert (out / "images" / "logo.png").read_text(
        encoding="utf-8"
    ) == "fake png content"
    assert (out / "images" / "banner.jpg").read_text(
        encoding="utf-8"
    ) == "fake jpg content"
    assert (out / "assets" / "style.css").read_text(
        encoding="utf-8"
    ) == "body { color: red; }"
    assert (out / "assets" / "app.js").read_text(
        encoding="utf-8"
    ) == "console.log('hello');"


def test_copy_static_directories_skips_directories_with_config(tmp_path):
    """Test that directories with _config.yaml are not copied."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "out"
    out.mkdir()

    # Create a directory with _config.yaml (should be skipped)
    blog_dir = src / "blog"
    blog_dir.mkdir()
    (blog_dir / "_config.yaml").write_text("title: Blog", encoding="utf-8")
    (blog_dir / "post.md").write_text("# Post", encoding="utf-8")

    # Create a static directory (should be copied)
    images_dir = src / "images"
    images_dir.mkdir()
    (images_dir / "logo.png").write_text("fake png content", encoding="utf-8")

    # Copy static directories
    copied_count = generator.copy_static_directories(str(src), str(out))

    # Verify only the static directory was copied
    assert copied_count == 1
    assert (out / "images").exists()
    assert not (out / "blog").exists()


def test_copy_static_directories_skips_hidden_and_build_directories(tmp_path):
    """Test that hidden directories and _build are skipped."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "out"
    out.mkdir()

    # Create hidden directory (should be skipped)
    hidden_dir = src / ".hidden"
    hidden_dir.mkdir()
    (hidden_dir / "secret.txt").write_text("secret content", encoding="utf-8")

    # Create _build directory (should be skipped)
    build_dir = src / "_build"
    build_dir.mkdir()
    (build_dir / "index.html").write_text("<html></html>", encoding="utf-8")

    # Create normal static directory (should be copied)
    assets_dir = src / "assets"
    assets_dir.mkdir()
    (assets_dir / "style.css").write_text("body { color: blue; }", encoding="utf-8")

    # Copy static directories
    copied_count = generator.copy_static_directories(str(src), str(out))

    # Verify only the assets directory was copied
    assert copied_count == 1
    assert (out / "assets").exists()
    assert not (out / ".hidden").exists()
    assert not (out / "_build").exists()


def test_copy_static_directories_overwrites_existing_directories(tmp_path):
    """Test that existing directories in output are overwritten."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "out"
    out.mkdir()

    # Create static directory in source
    images_dir = src / "images"
    images_dir.mkdir()
    (images_dir / "new_logo.png").write_text("new content", encoding="utf-8")

    # Create existing directory in output with different content
    existing_images = out / "images"
    existing_images.mkdir()
    (existing_images / "old_logo.png").write_text("old content", encoding="utf-8")

    # Copy static directories
    copied_count = generator.copy_static_directories(str(src), str(out))

    # Verify directory was overwritten
    assert copied_count == 1
    assert (out / "images").exists()
    assert (out / "images" / "new_logo.png").read_text(
        encoding="utf-8"
    ) == "new content"
    assert not (out / "images" / "old_logo.png").exists()


def test_generate_site_includes_static_directories_in_stats(tmp_path):
    """Test that generate_site includes static directories count in stats."""
    src = tmp_path / "site"
    src.mkdir()

    # Create minimal site config
    cfg = {"theme": "minimal"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    # Create a page
    md = """---
title: Test Page
published: true
---
# Test Page

Content here.
"""
    (src / "test.md").write_text(md, encoding="utf-8")

    # Create static directories
    images_dir = src / "images"
    images_dir.mkdir()
    (images_dir / "logo.png").write_text("fake png", encoding="utf-8")

    assets_dir = src / "assets"
    assets_dir.mkdir()
    (assets_dir / "style.css").write_text("body {}", encoding="utf-8")

    out = tmp_path / "out"

    # Generate site
    stats = generator.generate_site(str(src), str(out))

    # Verify stats include static directories
    assert "static_dirs" in stats
    assert stats["static_dirs"] == 2
    assert stats["pages"] == 1
    assert stats["errors"] == 0

    # Verify static directories were copied
    assert (out / "images" / "logo.png").exists()
    assert (out / "assets" / "style.css").exists()


def test_copy_static_directories_handles_empty_source_directory(tmp_path):
    """Test that copy_static_directories handles empty source directory gracefully."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "out"
    out.mkdir()

    # Copy from empty directory
    copied_count = generator.copy_static_directories(str(src), str(out))

    # Should return 0 without errors
    assert copied_count == 0


def test_copy_theme_assets_copies_css_and_js_files(tmp_path):
    """Test that copy_theme_assets copies CSS, JS and other non-template files."""
    # Create theme directory
    theme_dir = tmp_path / "themes" / "test_theme"
    theme_dir.mkdir(parents=True)

    # Create theme files
    (theme_dir / "style.css").write_text("body { color: red; }", encoding="utf-8")
    (theme_dir / "script.js").write_text("console.log('hello');", encoding="utf-8")
    (theme_dir / "logo.png").write_text("fake png", encoding="utf-8")

    # Create template files (should be skipped)
    (theme_dir / "base.html").write_text("<html></html>", encoding="utf-8")
    (theme_dir / "page.html").write_text("<div></div>", encoding="utf-8")
    (theme_dir / "README.md").write_text("# Theme", encoding="utf-8")

    out = tmp_path / "out"
    out.mkdir()

    # Mock the config.THEMES_DIR to point to our test directory
    import slartibartfast.config as config

    original_themes_dir = config.THEMES_DIR
    config.THEMES_DIR = str(tmp_path / "themes")

    try:
        # Copy theme assets
        copied_count = generator.copy_theme_assets("", "test_theme", str(out))

        # Should copy 3 non-template files
        assert copied_count == 3

        # Verify non-template files were copied
        assert (out / "style.css").exists()
        assert (out / "script.js").exists()
        assert (out / "logo.png").exists()

        # Verify template files were not copied
        assert not (out / "base.html").exists()
        assert not (out / "page.html").exists()
        assert not (out / "README.md").exists()

        # Verify content
        assert (out / "style.css").read_text(encoding="utf-8") == "body { color: red; }"
        assert (out / "script.js").read_text(
            encoding="utf-8"
        ) == "console.log('hello');"

    finally:
        # Restore original config
        config.THEMES_DIR = original_themes_dir


def test_copy_theme_assets_copies_subdirectories(tmp_path):
    """Test that copy_theme_assets copies subdirectories from theme."""
    # Create theme directory with subdirectories
    theme_dir = tmp_path / "themes" / "test_theme"
    theme_dir.mkdir(parents=True)

    # Create subdirectories with files
    assets_dir = theme_dir / "assets"
    assets_dir.mkdir()
    (assets_dir / "extra.css").write_text("/* extra styles */", encoding="utf-8")
    (assets_dir / "app.js").write_text("// app code", encoding="utf-8")

    js_dir = theme_dir / "js"
    js_dir.mkdir()
    (js_dir / "utils.js").write_text("// utilities", encoding="utf-8")

    out = tmp_path / "out"
    out.mkdir()

    # Mock the config.THEMES_DIR
    import slartibartfast.config as config

    original_themes_dir = config.THEMES_DIR
    config.THEMES_DIR = str(tmp_path / "themes")

    try:
        # Copy theme assets
        copied_count = generator.copy_theme_assets("", "test_theme", str(out))

        # Should copy 2 directories
        assert copied_count == 2

        # Verify directories were copied
        assert (out / "assets").exists()
        assert (out / "js").exists()

        # Verify files in subdirectories
        assert (out / "assets" / "extra.css").exists()
        assert (out / "assets" / "app.js").exists()
        assert (out / "js" / "utils.js").exists()

        # Verify content
        assert (out / "assets" / "extra.css").read_text(
            encoding="utf-8"
        ) == "/* extra styles */"

    finally:
        # Restore original config
        config.THEMES_DIR = original_themes_dir


def test_copy_theme_assets_handles_nonexistent_theme(tmp_path):
    """Test that copy_theme_assets handles nonexistent theme gracefully."""
    out = tmp_path / "out"
    out.mkdir()

    # Try to copy from nonexistent theme
    copied_count = generator.copy_theme_assets("", "nonexistent_theme", str(out))

    # Should return 0 without errors
    assert copied_count == 0


def test_generate_site_includes_theme_assets_in_stats(tmp_path):
    """Test that generate_site includes theme assets count in stats."""
    src = tmp_path / "site"
    src.mkdir()

    # Create site config
    cfg = {"theme": "test_theme"}
    (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

    # Create a page
    md = """---
title: Test Page
published: true
---
# Test Page

Content here.
"""
    (src / "test.md").write_text(md, encoding="utf-8")

    # Create theme directory with assets
    theme_dir = tmp_path / "themes" / "test_theme"
    theme_dir.mkdir(parents=True)
    (theme_dir / "style.css").write_text("body {}", encoding="utf-8")
    (theme_dir / "script.js").write_text("// code", encoding="utf-8")

    # Create template files (required for theme to work)
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
        # Generate site
        stats = generator.generate_site(str(src), str(out))

        # Verify stats include theme assets
        assert "theme_assets" in stats
        assert stats["theme_assets"] == 2
        assert stats["pages"] == 1
        assert stats["errors"] == 0

        # Verify theme assets were copied
        assert (out / "style.css").exists()
        assert (out / "script.js").exists()

    finally:
        # Restore original config
        config.THEMES_DIR = original_themes_dir

from datetime import date

import pytest
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


# ---------------------------------------------------------------------------
# Task 1.2: _extract_config_header() tests
# ---------------------------------------------------------------------------


class TestExtractConfigHeader:
    """Tests for _extract_config_header()."""

    def test_valid_front_matter(self):
        """Valid YAML front matter is extracted correctly."""
        content = "---\ntitle: Hello\ndescription: A page\n---\n# Body"
        meta, body = generator._extract_config_header(content)
        assert meta == {"title": "Hello", "description": "A page"}
        assert body == "# Body"

    def test_multiple_fields(self):
        """Front matter with several fields all round-trip."""
        content = (
            "---\n"
            "title: My Page\n"
            "nav_order: 2\n"
            "in_nav: true\n"
            "published: true\n"
            "---\nContent here"
        )
        meta, body = generator._extract_config_header(content)
        assert meta["title"] == "My Page"
        assert meta["nav_order"] == 2
        assert meta["in_nav"] is True
        assert meta["published"] is True
        assert body == "Content here"

    def test_missing_end_delimiter(self):
        """No closing --- returns empty dict and full content."""
        content = "---\ntitle: Unclosed\nSome body text"
        meta, body = generator._extract_config_header(content)
        assert meta == {}
        assert body == content

    def test_empty_content(self):
        """Empty string returns empty dict and empty string."""
        meta, body = generator._extract_config_header("")
        assert meta == {}
        assert body == ""

    def test_no_front_matter(self):
        """Content without front matter delimiter returns unchanged."""
        content = "# Just a heading\n\nSome text."
        meta, body = generator._extract_config_header(content)
        assert meta == {}
        assert body == content

    def test_malformed_yaml_raises(self):
        """Malformed YAML in front matter raises a YAML error."""
        content = "---\n: :\n  bad:\n    - [invalid\n---\nBody"
        with pytest.raises(yaml.YAMLError):
            generator._extract_config_header(content)

    def test_empty_front_matter(self):
        """Empty front matter block (just delimiters) returns None meta."""
        content = "---\n---\nBody text"
        meta, body = generator._extract_config_header(content)
        # yaml.safe_load("") returns None
        assert meta is None
        assert body == "Body text"

    def test_body_whitespace_is_stripped(self):
        """Leading whitespace after front matter is stripped."""
        content = "---\ntitle: Test\n---\n\n\n  Body"
        _, body = generator._extract_config_header(content)
        # lstrip() removes leading newlines/spaces
        assert body.startswith("Body")


# ---------------------------------------------------------------------------
# Task 1.3: load_config() tests
# ---------------------------------------------------------------------------


class TestLoadConfig:
    """Tests for load_config()."""

    def test_missing_config_file_raises(self, tmp_path):
        """Missing _config.yaml raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            generator.load_config(str(tmp_path))

    def test_invalid_yaml_raises(self, tmp_path):
        """Malformed YAML in config file raises an error."""
        (tmp_path / "_config.yaml").write_text(
            ": :\n  bad:\n    - [invalid", encoding="utf-8"
        )
        with pytest.raises(yaml.YAMLError):
            generator.load_config(str(tmp_path))

    def test_valid_config_returns_dict_with_source_path(self, tmp_path):
        """Valid config file returns dict with source_path set."""
        cfg = {"theme": "minimal", "title": "My Site"}
        (tmp_path / "_config.yaml").write_text(
            yaml.safe_dump(cfg), encoding="utf-8"
        )
        result = generator.load_config(str(tmp_path))
        assert isinstance(result, dict)
        assert result["theme"] == "minimal"
        assert result["title"] == "My Site"
        assert result["source_path"] == str(tmp_path)

    def test_empty_yaml_raises(self, tmp_path):
        """Empty YAML file (safe_load returns None) causes TypeError."""
        (tmp_path / "_config.yaml").write_text("", encoding="utf-8")
        # yaml.safe_load("") returns None, then config["source_path"] fails
        with pytest.raises(TypeError):
            generator.load_config(str(tmp_path))

    def test_config_preserves_all_keys(self, tmp_path):
        """All keys from the YAML are preserved in the returned dict."""
        cfg = {
            "theme": "default",
            "base_url": "https://example.com",
            "title": "Test",
            "description": "A site",
        }
        (tmp_path / "_config.yaml").write_text(
            yaml.safe_dump(cfg), encoding="utf-8"
        )
        result = generator.load_config(str(tmp_path))
        for key, value in cfg.items():
            assert result[key] == value


# ---------------------------------------------------------------------------
# Task 1.4: generate_navigation() tests
# ---------------------------------------------------------------------------


class TestGenerateNavigation:
    """Tests for generate_navigation()."""

    def test_empty_input(self):
        """Empty list returns empty navigation."""
        assert generator.generate_navigation([]) == []

    def test_pages_with_in_nav_false_excluded(self):
        """Pages with in_nav=False are excluded from navigation."""
        pages = [
            {
                "url": "/about.html",
                "title": "About",
                "description": "",
                "nav_order": 1,
                "in_nav": True,
            },
            {
                "url": "/hidden.html",
                "title": "Hidden",
                "description": "",
                "nav_order": 2,
                "in_nav": False,
            },
        ]
        nav = generator.generate_navigation(pages)
        assert len(nav) == 1
        assert nav[0]["title"] == "About"

    def test_sorting_by_nav_order(self):
        """Navigation items are sorted by nav_order."""
        pages = [
            {
                "url": "/c.html",
                "title": "C",
                "description": "",
                "nav_order": 3,
                "in_nav": True,
            },
            {
                "url": "/a.html",
                "title": "A",
                "description": "",
                "nav_order": 1,
                "in_nav": True,
            },
            {
                "url": "/b.html",
                "title": "B",
                "description": "",
                "nav_order": 2,
                "in_nav": True,
            },
        ]
        nav = generator.generate_navigation(pages)
        assert [item["title"] for item in nav] == ["A", "B", "C"]

    def test_same_nav_order_preserves_input_order(self):
        """Pages with same nav_order keep their relative input order."""
        pages = [
            {
                "url": "/x.html",
                "title": "X",
                "description": "",
                "nav_order": 1,
                "in_nav": True,
            },
            {
                "url": "/y.html",
                "title": "Y",
                "description": "",
                "nav_order": 1,
                "in_nav": True,
            },
        ]
        nav = generator.generate_navigation(pages)
        assert len(nav) == 2
        # Python's sort is stable, so original order is preserved
        assert nav[0]["title"] == "X"
        assert nav[1]["title"] == "Y"

    def test_all_pages_excluded(self):
        """If all pages have in_nav=False, result is empty."""
        pages = [
            {
                "url": "/a.html",
                "title": "A",
                "description": "",
                "nav_order": 1,
                "in_nav": False,
            },
        ]
        assert generator.generate_navigation(pages) == []

    def test_nav_items_have_active_false(self):
        """All generated nav items start with active=False."""
        pages = [
            {
                "url": "/home.html",
                "title": "Home",
                "description": "Main",
                "nav_order": 0,
                "in_nav": True,
            },
        ]
        nav = generator.generate_navigation(pages)
        assert nav[0]["active"] is False

    def test_nav_item_structure(self):
        """Nav items contain the expected keys."""
        pages = [
            {
                "url": "/about.html",
                "title": "About",
                "description": "About us",
                "nav_order": 5,
                "in_nav": True,
            },
        ]
        nav = generator.generate_navigation(pages)
        item = nav[0]
        assert item == {
            "url": "/about.html",
            "title": "About",
            "description": "About us",
            "active": False,
            "nav_order": 5,
        }


# ---------------------------------------------------------------------------
# Task 1.5: generate_sitemap() tests
# ---------------------------------------------------------------------------


class TestGenerateSitemap:
    """Tests for generate_sitemap()."""

    def test_empty_pages_produces_valid_xml(self):
        """Empty pages list produces a valid but empty sitemap."""
        sitemap = generator.generate_sitemap(
            [], {"base_url": "https://example.com"}
        )
        assert '<?xml version="1.0"' in sitemap
        assert "<urlset" in sitemap
        assert "</urlset>" in sitemap
        assert "<url>" not in sitemap

    def test_missing_base_url_uses_empty_string(self):
        """Missing base_url in config defaults to empty string."""
        pages = [
            {
                "url": "/page.html",
                "publish_date": None,
                "date": "2024-01-01",
            },
        ]
        sitemap = generator.generate_sitemap(pages, {})
        assert "<loc>/page.html</loc>" in sitemap

    def test_invalid_date_falls_back_to_today(self):
        """Invalid date string falls back to today's date."""
        pages = [
            {
                "url": "/page.html",
                "publish_date": "not-a-date",
                "date": None,
            },
        ]
        sitemap = generator.generate_sitemap(pages, {"base_url": ""})
        today_str = date.today().isoformat()
        assert f"<lastmod>{today_str}</lastmod>" in sitemap

    def test_valid_sitemap_structure(self):
        """Sitemap with pages has correct XML structure."""
        pages = [
            {
                "url": "/index.html",
                "publish_date": "2024-06-15",
                "date": "2024-06-01",
            },
            {
                "url": "/about.html",
                "publish_date": None,
                "date": "2024-05-01",
            },
        ]
        sitemap = generator.generate_sitemap(
            pages, {"base_url": "https://example.com"}
        )
        assert sitemap.count("<url>") == 2
        assert sitemap.count("</url>") == 2
        assert "<loc>https://example.com/index.html</loc>" in sitemap
        assert "<loc>https://example.com/about.html</loc>" in sitemap
        assert "<lastmod>2024-06-15</lastmod>" in sitemap
        assert "<lastmod>2024-05-01</lastmod>" in sitemap
        assert "<changefreq>weekly</changefreq>" in sitemap
        assert "<priority>0.8</priority>" in sitemap

    def test_base_url_trailing_slash_stripped(self):
        """Trailing slash on base_url is stripped to avoid double slashes."""
        pages = [
            {
                "url": "/page.html",
                "publish_date": None,
                "date": "2024-01-01",
            },
        ]
        sitemap = generator.generate_sitemap(
            pages, {"base_url": "https://example.com/"}
        )
        assert "<loc>https://example.com/page.html</loc>" in sitemap

    def test_publish_date_takes_precedence_over_date(self):
        """publish_date is used over date when both are present."""
        pages = [
            {
                "url": "/page.html",
                "publish_date": "2024-12-25",
                "date": "2024-01-01",
            },
        ]
        sitemap = generator.generate_sitemap(pages, {"base_url": ""})
        assert "<lastmod>2024-12-25</lastmod>" in sitemap
        assert "2024-01-01" not in sitemap

    def test_date_object_handled(self):
        """date objects (not just strings) are handled correctly."""
        pages = [
            {
                "url": "/page.html",
                "publish_date": date(2024, 3, 15),
                "date": "2024-01-01",
            },
        ]
        sitemap = generator.generate_sitemap(pages, {"base_url": ""})
        assert "<lastmod>2024-03-15</lastmod>" in sitemap


# ---------------------------------------------------------------------------
# Task 1.6: generate_site() error path tests
# ---------------------------------------------------------------------------


class TestGenerateSiteErrors:
    """Tests for generate_site() error paths."""

    def test_missing_config_raises(self, tmp_path):
        """generate_site raises FileNotFoundError when no _config.yaml."""
        src = tmp_path / "site"
        src.mkdir()
        out = tmp_path / "out"
        with pytest.raises(FileNotFoundError):
            generator.generate_site(str(src), str(out))

    def test_template_not_found_increments_errors(self, tmp_path):
        """A page referencing a missing template increments the error count."""
        src = tmp_path / "site"
        src.mkdir()

        cfg = {"theme": "minimal"}
        (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

        # Page that references a template that doesn't exist
        md = (
            "---\ntitle: Test\npublished: true\n"
            "template: nonexistent.html\n---\nBody"
        )
        (src / "page.md").write_text(md, encoding="utf-8")

        out = tmp_path / "out"
        stats = generator.generate_site(str(src), str(out))
        assert stats["errors"] >= 1
        assert not (out / "page.html").exists()

    def test_missing_theme_increments_errors(self, tmp_path):
        """Pages with a theme that doesn't exist result in errors."""
        src = tmp_path / "site"
        src.mkdir()

        cfg = {"theme": "totally_fake_theme_xyz"}
        (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

        md = "---\ntitle: Test\npublished: true\n---\nBody"
        (src / "page.md").write_text(md, encoding="utf-8")

        out = tmp_path / "out"
        stats = generator.generate_site(str(src), str(out))
        assert stats["errors"] >= 1

    def test_output_directory_created(self, tmp_path):
        """generate_site creates the output directory if it doesn't exist."""
        src = tmp_path / "site"
        src.mkdir()

        cfg = {"theme": "minimal"}
        (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

        out = tmp_path / "nested" / "output"
        assert not out.exists()
        generator.generate_site(str(src), str(out))
        assert out.exists()

    def test_sitemap_always_generated(self, tmp_path):
        """Sitemap XML is generated even when there are no pages."""
        src = tmp_path / "site"
        src.mkdir()

        cfg = {"theme": "minimal"}
        (src / "_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")

        out = tmp_path / "out"
        stats = generator.generate_site(str(src), str(out))
        assert stats["pages"] == 0
        assert stats["errors"] == 0
        assert (out / "sitemap.xml").exists()

        sitemap = (out / "sitemap.xml").read_text(encoding="utf-8")
        assert '<?xml version="1.0"' in sitemap

"""Tests for the generator correctness fixes: metadata, publish/nav semantics,
front-matter parsing, and output escaping."""

from xml.dom.minidom import parseString

from slartibartfast import generator


def _write(path, text):
    path.write_text(text, encoding="utf-8")


# --- Metadata correctness -------------------------------------------------


def test_filepath_is_source_path_once(tmp_path):
    src = tmp_path / "site"
    src.mkdir()
    _write(src / "root.md", "---\npublished: true\ntitle: Root\n---\n# Root\n")
    blog = src / "blog"
    blog.mkdir()
    _write(blog / "_config.yaml", "title: Blog\npublished: true\n")
    _write(blog / "post.md", "---\npublished: true\ntitle: Post\n---\n# Post\n")

    pages = generator.collect_pages_metadata(str(src))
    by_name = {p["filename"]: p for p in pages}

    assert by_name["root.md"]["filepath"] == str(src / "root.md")
    assert by_name["blog/post.md"]["filepath"] == str(blog / "post.md")


def test_directory_named_like_md_is_section_only(tmp_path):
    src = tmp_path / "site"
    src.mkdir()
    weird = src / "notes.md"  # a directory whose name ends in .md
    weird.mkdir()
    _write(weird / "_config.yaml", "title: Notes\npublished: true\n")
    _write(weird / "inner.md", "---\npublished: true\ntitle: Inner\n---\n# Inner\n")

    pages = generator.collect_pages_metadata(str(src))
    filenames = {p["filename"] for p in pages}

    assert "notes.md/index.html" in filenames  # treated as a section
    assert "notes.md" not in filenames  # not also treated as a markdown page


def test_pages_sorted_by_nav_order_then_title(tmp_path):
    src = tmp_path / "site"
    src.mkdir()
    _write(src / "b.md", "---\npublished: true\ntitle: Bravo\nnav_order: 2\n---\nx")
    _write(src / "a.md", "---\npublished: true\ntitle: Alpha\nnav_order: 2\n---\nx")
    _write(src / "c.md", "---\npublished: true\ntitle: Charlie\nnav_order: 1\n---\nx")

    pages = generator.collect_pages_metadata(str(src))
    titles = [p["title"] for p in pages]

    # nav_order 1 first, then nav_order 2 broken by title (Alpha before Bravo)
    assert titles == ["Charlie", "Alpha", "Bravo"]


# --- Publish and navigation semantics -------------------------------------


def test_section_respects_published_false(tmp_path):
    src = tmp_path / "site"
    src.mkdir()
    sec = src / "hidden"
    sec.mkdir()
    _write(sec / "_config.yaml", "title: Hidden\npublished: false\n")
    _write(sec / "p.md", "---\npublished: true\ntitle: P\n---\nx")

    pages = generator.collect_pages_metadata(str(src))
    filenames = {p["filename"] for p in pages}

    assert "hidden/index.html" not in filenames
    assert "hidden/p.md" not in filenames  # children excluded with the section


def test_section_respects_future_publish_date(tmp_path):
    src = tmp_path / "site"
    src.mkdir()
    sec = src / "future"
    sec.mkdir()
    _write(
        sec / "_config.yaml",
        "title: Future\npublished: true\npublish_date: '3000-01-01'\n",
    )
    _write(sec / "p.md", "---\npublished: true\ntitle: P\n---\nx")

    pages = generator.collect_pages_metadata(str(src))
    filenames = {p["filename"] for p in pages}

    assert "future/index.html" not in filenames


def test_in_nav_defaults_true_for_pages_and_sections(tmp_path):
    src = tmp_path / "site"
    src.mkdir()
    _write(src / "page.md", "---\npublished: true\ntitle: P\n---\nx")  # no in_nav
    sec = src / "sec"
    sec.mkdir()
    _write(sec / "_config.yaml", "title: Sec\npublished: true\n")  # no in_nav
    _write(sec / "c.md", "---\npublished: true\ntitle: C\n---\nx")

    pages = generator.collect_pages_metadata(str(src))
    by_name = {p["filename"]: p for p in pages}

    assert by_name["page.md"]["in_nav"] is True
    assert by_name["sec/index.html"]["in_nav"] is True


# --- Front-matter parsing -------------------------------------------------


def test_front_matter_body_horizontal_rule():
    content = "---\ntitle: X\n---\n# Head\n\nbefore\n\n---\n\nafter\n"
    cfg, body = generator._extract_config_header(content)
    assert cfg == {"title": "X"}
    assert "---" in body  # body thematic break preserved
    assert "after" in body


def test_front_matter_empty():
    cfg, body = generator._extract_config_header("---\n---\nbody\n")
    assert cfg == {}
    assert body.strip() == "body"


def test_front_matter_absent():
    content = "# Just a heading\n\ntext"
    cfg, body = generator._extract_config_header(content)
    assert cfg == {}
    assert body == content


def test_front_matter_dashes_inside_yaml_value():
    content = '---\ntitle: "a --- b"\n---\nbody\n'
    cfg, body = generator._extract_config_header(content)
    assert cfg == {"title": "a --- b"}
    assert body.strip() == "body"


# --- Output escaping ------------------------------------------------------


def test_sitemap_escapes_ampersand():
    pages = [{"url": "/a?x=1&y=2.html", "publish_date": None, "date": "2025-01-01"}]
    sitemap = generator.generate_sitemap(pages, {"base_url": "https://e.com"})

    assert "&amp;" in sitemap
    parseString(sitemap)  # raises if not well-formed XML


def test_metadata_escaped_and_content_not_double_escaped(tmp_path, monkeypatch):
    src = tmp_path / "site"
    src.mkdir()
    _write(src / "_config.yaml", "theme: t\n")
    _write(
        src / "p.md",
        '---\npublished: true\ntitle: "<b>hi</b>"\ntemplate: page.html\n---\n'
        "# Heading\n\n**bold**\n",
    )
    theme = tmp_path / "themes" / "t"
    theme.mkdir(parents=True)
    # content deliberately has no |safe filter to prove Markup marks it safe
    _write(
        theme / "page.html", "<title>{{ meta.title }}</title><main>{{ content }}</main>"
    )
    monkeypatch.setattr(generator.config, "THEMES_DIR", str(tmp_path / "themes"))

    out = tmp_path / "out"
    stats = generator.generate_site(str(src), str(out))
    assert stats["errors"] == 0

    html = (out / "p.html").read_text(encoding="utf-8")
    # untrusted metadata is escaped
    assert "&lt;b&gt;hi&lt;/b&gt;" in html
    assert "<title><b>hi</b></title>" not in html
    # rendered markdown content passes through as real HTML
    assert "<strong>bold</strong>" in html
    assert "<h1>Heading</h1>" in html

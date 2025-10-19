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

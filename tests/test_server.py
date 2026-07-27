"""Tests for the dev-server watcher event filtering."""

import os

from slartibartfast.server import ReloadEventHandler


def _handler(tmp_path):
    content = tmp_path / "site"
    content.mkdir()
    output = content / "_build"
    output.mkdir()
    return ReloadEventHandler(str(content), str(output)), content, output


def test_watcher_ignores_output_directory_events(tmp_path):
    handler, content, output = _handler(tmp_path)
    # A file written inside the output directory must not trigger a rebuild.
    assert handler.should_handle(str(output / "index.html")) is False
    assert handler.should_handle(str(output / "blog" / "post.html")) is False


def test_watcher_handles_content_file_change(tmp_path):
    handler, content, _ = _handler(tmp_path)
    assert handler.should_handle(str(content / "index.md")) is True
    assert handler.should_handle(str(content / "blog" / "post.md")) is True


def test_watcher_ignores_irrelevant_extensions(tmp_path):
    handler, content, _ = _handler(tmp_path)
    assert handler.should_handle(str(content / "module.pyc")) is False
    assert handler.should_handle(str(content / "notes.swp")) is False
    assert handler.should_handle(str(content / ".DS_Store")) is False


def test_watcher_ignores_hidden_directories(tmp_path):
    handler, content, _ = _handler(tmp_path)
    assert handler.should_handle(str(content / ".git" / "index.md")) is False
    assert handler.should_handle(str(content / ".cache" / "style.css")) is False


def test_watcher_handles_relevant_asset_types(tmp_path):
    handler, content, _ = _handler(tmp_path)
    for name in ("style.css", "app.js", "logo.svg", "photo.png", "_config.yaml"):
        assert handler.should_handle(str(content / name)) is True, name


def test_output_path_resolved_to_absolute(tmp_path):
    content = tmp_path / "site"
    content.mkdir()
    handler = ReloadEventHandler(str(content), "_build")
    assert os.path.isabs(handler.output)

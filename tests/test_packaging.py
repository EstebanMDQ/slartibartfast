"""Tests for package data: themes are bundled with the package."""

import os

from slartibartfast import config


def test_themes_dir_is_bundled_in_package():
    # THEMES_DIR resolves inside the package directory, not the repo root, so
    # bundled themes are found after a pip install.
    assert config.THEMES_DIR.startswith(config.PACKAGE_DIR)
    assert os.path.isdir(config.THEMES_DIR)

    entries = set(os.listdir(config.THEMES_DIR))
    assert {"default", "minimal"} <= entries


def test_default_theme_has_templates():
    default = os.path.join(config.THEMES_DIR, "default")
    files = set(os.listdir(default))
    assert "base.html" in files
    assert "page.html" in files

"""Slartibartfast: a tiny, fast static site generator."""

from importlib.metadata import PackageNotFoundError, version

try:
    # Single source of truth is [project].version in pyproject.toml.
    __version__ = version("slartibartfast")
except PackageNotFoundError:  # running from a source tree without an install
    __version__ = "0.0.0+unknown"

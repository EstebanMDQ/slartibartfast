"""Test bootstrap: make the repository root importable so tests can import
the package as `slartibartfast` when pytest is run from the project root.

This is a small, non-invasive helper useful for local/test environments where
the package hasn't been installed into the current Python environment.
Prefer installing the package into the virtualenv (see README) for CI/normal use.
"""

from pathlib import Path
import sys


def _add_repo_root_to_path() -> None:
    # tests/ is at repo_root/tests; add repo_root to sys.path so
    # `import slartibartfast` works during pytest collection.
    repo_root = Path(__file__).resolve().parent.parent
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


_add_repo_root_to_path()

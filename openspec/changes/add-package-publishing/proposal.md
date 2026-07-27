# Change: Prepare project for package publishing

## Why
The project is currently set up for local development only. To publish to PyPI so users can `pip install slartibartfast`, the package needs proper PEP 621 metadata (or Poetry metadata enrichment), a distribution-safe theme bundling strategy, classifiers, and a publishing workflow.

## What Changes
- Add complete package metadata (classifiers, keywords, project URLs, requires-python)
- Bundle the `themes/` directory as package data so themes ship with the install
- Ensure the `slarti` CLI entry point works when installed from PyPI (not just from the repo root)
- Fix `config.py` `BASE_DIR`/`THEMES_DIR` to resolve correctly when installed as a package (currently uses `__file__` relative paths that assume repo layout)
- Add a `__version__` to the package `__init__.py`
- Add a `py.typed` marker if type hints should be exposed
- Update `.gitignore` for distribution artifacts (`dist/`, `*.egg-info`)

## Impact
- Affected specs: `package-publishing` (new)
- Affected code: `pyproject.toml`, `slartibartfast/__init__.py`, `slartibartfast/config.py`, `.gitignore`
- **BREAKING**: `config.THEMES_DIR` resolution will change - themes must be bundled inside the package rather than resolved relative to the repo root

## 1. Package metadata
- [x] 1.1 Add classifiers (Development Status, License, Programming Language, Topic)
- [x] 1.2 Add keywords and project URLs (homepage, repository, issues)
- [x] 1.3 Add `requires-python` constraint
- [x] 1.4 Add `__version__` to `slartibartfast/__init__.py`

## 2. Bundle themes as package data
- [x] 2.1 Move `themes/` inside `slartibartfast/` (e.g., `slartibartfast/themes/`) so it ships with the package
- [x] 2.2 Update `pyproject.toml` to include theme files as package data
- [x] 2.3 Update `config.py` to resolve `THEMES_DIR` using `importlib.resources` or `__file__` relative to the package directory (not the repo root)
- [x] 2.4 Verify template loading still works with the new theme path

## 3. Fix installed entry point
- [x] 3.1 Verify `slarti` CLI works when installed via `pip install .` (not just `poetry run`)
- [x] 3.2 Verify `python -m slartibartfast.cli` still works

## 4. Distribution hygiene
- [x] 4.1 Update `.gitignore` to exclude `dist/`, `*.egg-info`
- [x] 4.2 Add a `MANIFEST.in` or verify build backend includes all needed files
- [x] 4.3 Test building with `python -m build` (or `uv build` if migration is done first)

## 5. Tests
- [x] 5.1 Add test that `THEMES_DIR` resolves to a real directory containing the bundled themes
- [x] 5.2 Verify existing generator tests still pass with the new theme path resolution

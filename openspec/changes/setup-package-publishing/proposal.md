# Change: Set up package publishing for PyPI distribution

## Why

The package cannot be installed via pip because themes are not bundled with the package. `config.py` uses `os.path.dirname`-relative paths that resolve to the source tree, not the installed package location. Additionally, the project lacks PyPI metadata, CI workflows, and release infrastructure.

## What Changes

- **BREAKING**: Move `themes/` directory inside the `slartibartfast/` package directory so themes are included in the distribution
- Update `config.py` to resolve theme paths relative to the package using `__file__`-based paths or `importlib.resources`
- Update `generator.py` theme loading to work with the new theme location
- Add PyPI classifiers, keywords, and project URLs to `pyproject.toml`
- Add `dist/`, `build/`, `*.egg-info` to `.gitignore`
- Create GitHub Actions workflow for CI (lint + test on multiple Python versions)
- Create GitHub Actions workflow for PyPI publishing on tagged releases
- Add `CHANGELOG.md` for release tracking
- Resolve version duplication between `pyproject.toml` and `__init__.py`

## Impact

- Affected specs: distribution (new)
- Affected code: `themes/` (moved), `slartibartfast/config.py`, `slartibartfast/generator.py`, `pyproject.toml`, `.gitignore`
- New files: `CHANGELOG.md`, `.github/workflows/ci.yml`, `.github/workflows/publish.yml`
- **BREAKING**: `themes/` directory moves from project root to `slartibartfast/themes/`

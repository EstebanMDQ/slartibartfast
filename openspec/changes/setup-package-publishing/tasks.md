## 1. Bundle themes with package

- [x] 1.1 Move `themes/` directory to `slartibartfast/themes/`
- [x] 1.2 Update `config.py` `THEMES_DIR` to use `os.path.join(os.path.dirname(__file__), "themes")` instead of parent directory traversal
- [x] 1.3 Update `generator.py` if any direct theme path references exist (no changes needed - uses config.THEMES_DIR)
- [x] 1.4 Add `[tool.hatch.build.targets.wheel]` config to include `slartibartfast/themes/` as package data (not needed - hatchling includes all files by default)

## 2. Add PyPI metadata

- [x] 2.1 Add classifiers (Development Status, License, Programming Language, Topic) to `pyproject.toml`
- [x] 2.2 Add keywords to `pyproject.toml`
- [x] 2.3 Add project URLs (Homepage, Repository, Issues) to `pyproject.toml`

## 3. Resolve version management

- [x] 3.1 Check for version in `slartibartfast/__init__.py` and `pyproject.toml`
- [x] 3.2 Choose single source of truth for version (prefer `pyproject.toml` with dynamic reading, or `__init__.py` with hatch-vcs)
- [x] 3.3 Remove duplicate version definition

## 4. Build artifacts and release infrastructure

- [ ] 4.1 Add `dist/`, `build/`, `*.egg-info` to `.gitignore`
- [ ] 4.2 Create `CHANGELOG.md` with initial 0.1.0 entry
- [ ] 4.3 Create `.github/workflows/ci.yml` - lint with ruff, test with pytest on Python 3.10-3.13
- [ ] 4.4 Create `.github/workflows/publish.yml` - build and publish to PyPI on tagged releases

## 5. Verify

- [ ] 5.1 Run `uv build` (or `python -m build`) and confirm wheel/sdist are created
- [ ] 5.2 Install the built wheel in a clean venv and run `slarti --help`
- [ ] 5.3 Confirm themes are accessible from the installed package
- [ ] 5.4 Run test suite to confirm nothing broke

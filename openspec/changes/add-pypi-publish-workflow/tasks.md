## 1. Prerequisites

- [x] 1.1 Confirm `add-package-publishing` is applied (PEP 621 metadata, bundled themes, `THEMES_DIR` fix, working `slarti` entry point)
- [x] 1.2 Confirm the PyPI distribution name `slartibartfast` is available; if not, decide on an alternate `[project].name`
- [x] 1.3 Decide the version source of truth (single manual bump point, or hatchling dynamic version) and document it

## 2. Build

- [x] 2.1 Build distributions with `uv build` (or `python -m build`) and confirm a `.whl` and `.tar.gz` appear in `dist/`
- [x] 2.2 Inspect the wheel contents to confirm bundled themes and the `slarti` entry point are included
- [x] 2.3 Smoke-test: create a clean venv, `pip install dist/slartibartfast-*.whl`, and run `slarti generate site --output /tmp/_smoke` successfully

## 3. Publish workflow

- [x] 3.1 Write `RELEASING.md`: bump version -> build -> inspect -> smoke-test -> tag -> publish
- [x] 3.2 Document PyPI token configuration (`UV_PUBLISH_TOKEN` or `~/.pypirc`) with an explicit "do not commit" note
- [x] 3.3 Document the publish command (`uv publish`, with `twine upload dist/*` as the fallback)
- [x] 3.4 Verify no credentials are present in tracked files

## 4. README rewrite

- [x] 4.1 Rewrite the Install section to lead with `pip install slartibartfast` (plus `uv tool install` / `uv add` notes)
- [x] 4.2 Update Quick usage to use the installed `slarti generate` / `slarti serve` commands
- [x] 4.3 Replace Poetry references in Testing with `uv sync` / `uv run pytest`
- [x] 4.4 Update Contributing to reference the current toolchain (uv, Ruff, pre-commit)
- [x] 4.5 Preserve the README's existing tone and structure while updating commands

## 5. Verification

- [x] 5.1 Follow `RELEASING.md` end-to-end in a dry run (everything up to, but not including, the actual `publish`)
- [x] 5.2 Confirm the README no longer instructs end users to `poetry install`
- [ ] 5.3 (Deferred) Publish to PyPI - not done: the `slartibartfast` name is taken; set an available distribution name (e.g. `slartibartfast-ssg`) and publish per RELEASING.md when ready

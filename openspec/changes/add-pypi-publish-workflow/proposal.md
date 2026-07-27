## Why

Once the package has proper metadata and bundled themes (`add-package-publishing`), it still cannot actually be shipped: there is no defined way to build distributions, publish them to PyPI, or install them, and the README still tells users to `poetry install` from source. This change adds the release workflow and rewrites the README so users can `pip install slartibartfast` and get started.

## What Changes

- Define a repeatable **build** step that produces both a wheel and an sdist (`uv build`, falling back to `python -m build`)
- Define a **publish** workflow to upload distributions to PyPI (via `uv publish`/`twine`), including a version-bump and tagging convention
- Document the **release procedure** (build -> verify -> publish) in the repo so it is reproducible
- Rewrite **README.md** installation and usage instructions:
  - Lead with `pip install slartibartfast` (and `uv add` / `uv tool install slarti`)
  - Replace `poetry install` / `poetry run` guidance with the installed `slarti` CLI and `uv run` for development
  - Update Testing and Contributing sections to match the current toolchain
- **No changes** to Python runtime behavior

## Capabilities

### New Capabilities
- `package-publishing`: Building distributable artifacts and publishing the package to PyPI, plus the user-facing installation and usage documentation. Extends the metadata/bundling groundwork from the `add-package-publishing` change with the actual build/publish/document workflow.

### Modified Capabilities
<!-- No archived specs exist yet; the package-publishing capability is still an unmerged delta, so this change ADDs to it rather than MODIFYing archived requirements. -->

## Impact

- Depends on `add-package-publishing` (PEP 621 metadata, bundled themes, fixed `THEMES_DIR`, working entry point) landing first
- Benefits from `migrate-to-uv-ruff-bandit` (enables `uv build` / `uv publish`); the workflow documents a non-uv fallback so it does not hard-block on that change
- Affected files: `README.md`, `pyproject.toml` (version/URLs as needed), and a release/publishing doc (e.g., `RELEASING.md`)
- Requires a PyPI account and API token for the actual upload (out of band; documented, not committed)
- No Python source code changes

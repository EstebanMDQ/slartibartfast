# Change: Migrate from Poetry to uv

> **Superseded and withdrawn.** This change was absorbed by
> `migrate-to-uv-ruff-bandit`, which performs the same Poetry-to-uv migration
> plus Bandit security scanning and pre-commit formalization. Archived
> unimplemented to avoid two changes editing `pyproject.toml`.

## Why
Poetry is slow for dependency resolution and installs compared to modern alternatives. uv (by Astral, the same team behind Ruff) is significantly faster, has native `pyproject.toml` support with PEP 621 metadata, and aligns with the project's existing use of Astral tooling (Ruff).

## What Changes
- Replace `[tool.poetry]` sections in `pyproject.toml` with PEP 621 `[project]` metadata
- Replace `[build-system]` from `poetry-core` to `hatchling` (uv-compatible, PEP 517)
- Delete `poetry.lock` and generate `uv.lock` instead
- Update all `poetry run ...` commands to `uv run ...` in README and docs
- Update `openspec/project.md` to reference uv instead of Poetry
- Add `.python-version` file for uv's Python management (optional)

## Impact
- Affected specs: `build-tooling` (new capability spec)
- Affected code: `pyproject.toml`, `poetry.lock`, `README.md`, `openspec/project.md`
- **No changes** to any Python source code - this is purely a tooling/packaging migration
- Pre-commit config is unaffected (Ruff hooks are independent of the package manager)

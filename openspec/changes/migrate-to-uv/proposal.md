# Change: Migrate from Poetry to uv

## Why

Poetry is slow for dependency resolution and installs, and its `pyproject.toml` format uses non-standard `[tool.poetry]` sections instead of PEP 621 `[project]`. Migrating to uv provides faster installs, standard-compliant metadata, and a simpler toolchain.

## What Changes

- Rewrite `pyproject.toml` from `[tool.poetry]` to PEP 621 `[project]` format
- Switch build backend from `poetry-core` to `hatchling`
- Delete `poetry.lock`, replace with `uv.lock`
- Add `.python-version` file (set to `3.10`)
- Update `README.md` to replace `poetry` commands with `uv` equivalents
- Update `openspec/project.md` to reference uv instead of Poetry

## Impact

- Affected specs: build-system (new)
- Affected code: `pyproject.toml`, `poetry.lock`, `README.md`, `openspec/project.md`
- **BREAKING**: Developers using `poetry install` / `poetry run` must switch to `uv sync` / `uv run`
- No runtime behavior changes - only developer tooling

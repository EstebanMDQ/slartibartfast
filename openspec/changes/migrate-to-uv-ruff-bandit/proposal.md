## Why

The project uses Poetry for dependency management, which is slower than modern alternatives and diverges from the Astral tooling (Ruff) already in use. It also has no automated security scanning. Consolidating on uv, Ruff, pre-commit, and Bandit gives a faster, single-vendor toolchain with linting, formatting, and security checks enforced consistently on every commit.

## What Changes

- Replace Poetry with **uv** for dependency management and packaging:
  - Convert `[tool.poetry]` to PEP 621 `[project]` metadata in `pyproject.toml`
  - Switch build backend from `poetry-core` to `hatchling`
  - Move dev dependencies to `[dependency-groups]`
  - Add `bandit` as a dev dependency
  - Remove `poetry.lock`; generate and commit `uv.lock`
  - Add a `.python-version` file for uv-managed Python
- Keep and formalize **Ruff** as the linter and formatter (existing `[tool.ruff]` config is preserved and documented as the single source of truth)
- Add **Bandit** security static analysis with project configuration in `pyproject.toml`
- Update the **pre-commit** config to run Ruff (lint + format) and Bandit, and to install/run under uv
- Update `README.md` and `openspec/project.md` to reference `uv run ...` and the new quality/security tooling
- **No changes** to any Python source code - this is purely a tooling migration

## Capabilities

### New Capabilities
- `build-tooling`: uv-based dependency management and packaging using PEP 621 metadata and the hatchling build backend, replacing Poetry.
- `code-quality`: Automated linting, formatting, and security scanning via Ruff and Bandit, enforced locally through pre-commit hooks.

### Modified Capabilities
<!-- No existing archived specs; nothing to modify. -->

## Impact

- Affected code: none (Python source is unchanged)
- Affected config/docs: `pyproject.toml`, `poetry.lock` (removed), `uv.lock` (added), `.pre-commit-config.yaml`, `.python-version` (added), `README.md`, `openspec/project.md`
- Affected dependencies: adds `bandit` (dev); removes Poetry as the required package manager
- Supersedes the in-flight `migrate-poetry-to-uv` change, which covered only the uv portion
- Developer workflow changes: `poetry install` -> `uv sync`, `poetry run <cmd>` -> `uv run <cmd>`

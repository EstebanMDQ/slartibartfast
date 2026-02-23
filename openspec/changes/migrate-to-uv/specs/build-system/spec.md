## ADDED Requirements

### Requirement: PEP 621 Project Metadata

The project SHALL use PEP 621 `[project]` format in `pyproject.toml` for all package metadata including name, version, description, authors, license, readme, and Python version constraints.

#### Scenario: Standard metadata fields present
- **WHEN** `pyproject.toml` is read by any PEP 621-compliant tool
- **THEN** it SHALL contain `[project]` with name, version, description, authors, license, readme, and `requires-python`

### Requirement: Hatchling Build Backend

The project SHALL use `hatchling` as its build backend in `[build-system]`.

#### Scenario: Build backend configuration
- **WHEN** the package is built with `uv build` or `python -m build`
- **THEN** hatchling SHALL be used as the build backend

### Requirement: uv Lock File

The project SHALL use `uv.lock` for deterministic dependency locking, replacing `poetry.lock`.

#### Scenario: Dependency installation from lock file
- **WHEN** a developer runs `uv sync`
- **THEN** dependencies SHALL be installed from `uv.lock` with exact pinned versions

### Requirement: Python Version Pin

The project SHALL include a `.python-version` file set to `3.10` as the minimum supported Python version.

#### Scenario: Python version detected by tooling
- **WHEN** uv or pyenv reads `.python-version`
- **THEN** it SHALL use Python 3.10 as the target version

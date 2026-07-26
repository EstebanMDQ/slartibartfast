## ADDED Requirements

### Requirement: uv Project Management
The project SHALL use uv as its package manager and project management tool, with metadata defined via PEP 621.

#### Scenario: Project metadata uses PEP 621
- **WHEN** a developer reads `pyproject.toml`
- **THEN** project metadata is defined under `[project]` following PEP 621
- **AND** the `[build-system]` uses `hatchling`

#### Scenario: Dependencies are installed with uv
- **WHEN** a developer runs `uv sync`
- **THEN** all runtime and dev dependencies are installed in a virtual environment
- **AND** a `uv.lock` file is present for reproducible installs

#### Scenario: CLI entry point works via uv
- **WHEN** a developer runs `uv run slarti generate <path>`
- **THEN** the CLI executes the same as the previous `poetry run slarti` command

#### Scenario: Dev dependencies are in a dependency group
- **WHEN** a developer inspects `pyproject.toml`
- **THEN** dev dependencies (pytest, ruff, pre-commit, bandit) are listed under `[dependency-groups]`

### Requirement: Python Version Pinning
The project SHALL declare a target Python version that uv uses to provision the environment.

#### Scenario: Python version file present
- **WHEN** a developer lists project files
- **THEN** a `.python-version` file exists
- **AND** its version satisfies the `requires-python` constraint in `pyproject.toml`

### Requirement: No Poetry Artifacts
The project SHALL NOT contain Poetry-specific configuration or lock files.

#### Scenario: Poetry lock file removed
- **WHEN** a developer lists project files
- **THEN** `poetry.lock` does not exist
- **AND** `uv.lock` exists instead

#### Scenario: No Poetry sections in pyproject.toml
- **WHEN** a developer reads `pyproject.toml`
- **THEN** there are no `[tool.poetry]` sections
- **AND** the build backend is not `poetry-core`

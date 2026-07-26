## ADDED Requirements

### Requirement: Ruff Linting and Formatting
The project SHALL use Ruff as the single source of truth for linting and formatting, configured in `pyproject.toml`.

#### Scenario: Ruff configuration is present
- **WHEN** a developer reads `pyproject.toml`
- **THEN** `[tool.ruff]` defines line length and target version
- **AND** `[tool.ruff.lint]` enables the `E`, `F`, and `I` rule sets

#### Scenario: Linting passes on existing source
- **WHEN** a developer runs `uv run ruff check .`
- **THEN** the command completes with no lint errors

#### Scenario: Formatting is stable
- **WHEN** a developer runs `uv run ruff format --check .`
- **THEN** the command reports that all files are already formatted

### Requirement: Bandit Security Scanning
The project SHALL run Bandit static security analysis over the package source, configured in `pyproject.toml`.

#### Scenario: Bandit configuration is present
- **WHEN** a developer reads `pyproject.toml`
- **THEN** a `[tool.bandit]` section scopes the scan to the `slartibartfast` package
- **AND** the `tests` directory is excluded

#### Scenario: Security scan passes
- **WHEN** a developer runs `uv run bandit -c pyproject.toml -r slartibartfast`
- **THEN** the command completes with no unignored high-severity findings

### Requirement: Pre-commit Enforcement
The project SHALL enforce Ruff and Bandit checks via pre-commit hooks so violations are caught before commit.

#### Scenario: Hooks are configured
- **WHEN** a developer reads `.pre-commit-config.yaml`
- **THEN** it includes Ruff lint, Ruff format, and Bandit hooks

#### Scenario: Hooks run against staged files
- **WHEN** a developer runs `uv run pre-commit run --all-files`
- **THEN** the Ruff and Bandit hooks execute and pass on the current source

#### Scenario: Non-code hygiene hooks retained
- **WHEN** a developer reads `.pre-commit-config.yaml`
- **THEN** existing hygiene hooks (end-of-file fixer, trailing whitespace, YAML/TOML checks) remain configured

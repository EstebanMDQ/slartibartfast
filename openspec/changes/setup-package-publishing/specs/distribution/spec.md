## ADDED Requirements

### Requirement: Bundled Themes

The package distribution SHALL include all built-in themes inside the `slartibartfast/themes/` directory so they are available when the package is installed via pip.

#### Scenario: Themes accessible after pip install
- **WHEN** the package is installed via `pip install slartibartfast`
- **THEN** the default theme SHALL be accessible at the package's `themes/` subdirectory
- **AND** `slarti build` SHALL work without a local `themes/` directory in the project root

### Requirement: Package Path Resolution

The `config.py` module SHALL resolve the `THEMES_DIR` path relative to the package's own `__file__` location, not relative to the project source tree root.

#### Scenario: Theme path resolves correctly in installed package
- **WHEN** `config.THEMES_DIR` is accessed from an installed package
- **THEN** it SHALL point to `<site-packages>/slartibartfast/themes/`

#### Scenario: Theme path resolves correctly in development
- **WHEN** `config.THEMES_DIR` is accessed during development (editable install or direct execution)
- **THEN** it SHALL point to `<project>/slartibartfast/themes/`

### Requirement: PyPI Metadata

The `pyproject.toml` SHALL include PyPI classifiers, keywords, and project URLs sufficient for discoverability on PyPI.

#### Scenario: Package metadata visible on PyPI
- **WHEN** the package is published to PyPI
- **THEN** the listing SHALL display license, supported Python versions, project description, and links to the repository and issue tracker

### Requirement: CI Workflow

The project SHALL have a GitHub Actions CI workflow that runs linting and tests on every push and pull request.

#### Scenario: CI runs on pull request
- **WHEN** a pull request is opened or updated
- **THEN** the CI workflow SHALL run ruff lint and pytest across Python 3.10 through 3.13

### Requirement: Automated PyPI Publishing

The project SHALL have a GitHub Actions workflow that builds and publishes the package to PyPI when a version tag is pushed.

#### Scenario: Tag triggers publish
- **WHEN** a tag matching `v*` is pushed to the repository
- **THEN** the publish workflow SHALL build the sdist and wheel and upload them to PyPI

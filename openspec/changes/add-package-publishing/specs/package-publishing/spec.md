## ADDED Requirements

### Requirement: PyPI-Ready Package Metadata
The project SHALL have complete package metadata suitable for publishing to PyPI.

#### Scenario: Package has required metadata fields
- **WHEN** a user inspects the built package metadata
- **THEN** it SHALL include name, version, description, author, license, classifiers, keywords, project URLs, and requires-python

#### Scenario: Version is accessible at runtime
- **WHEN** a user runs `import slartibartfast; print(slartibartfast.__version__)`
- **THEN** the version string SHALL be returned

### Requirement: Bundled Themes
The default themes SHALL be bundled inside the package so they are available when installed from PyPI.

#### Scenario: Themes available after pip install
- **WHEN** a user installs the package via `pip install slartibartfast`
- **AND** runs `slarti generate` with the default theme
- **THEN** the default theme templates SHALL be found and used for rendering

#### Scenario: Theme directory resolves inside package
- **WHEN** the generator resolves the `THEMES_DIR` path
- **THEN** it SHALL point to the themes directory inside the installed package
- **AND** the directory SHALL exist and contain the default and minimal themes

### Requirement: Working CLI Entry Point
The `slarti` CLI entry point SHALL work correctly when the package is installed from a distribution (not just from the source repo).

#### Scenario: Entry point after pip install
- **WHEN** a user installs the package via `pip install slartibartfast`
- **AND** runs `slarti generate <path>`
- **THEN** the CLI SHALL execute correctly

#### Scenario: Module execution
- **WHEN** a user runs `python -m slartibartfast.cli generate <path>`
- **THEN** the CLI SHALL execute correctly

### Requirement: Clean Build Artifacts
The repository SHALL exclude build and distribution artifacts from version control.

#### Scenario: Gitignore covers distribution files
- **WHEN** a developer builds the package
- **THEN** `dist/`, `*.egg-info`, and build artifacts SHALL be ignored by git

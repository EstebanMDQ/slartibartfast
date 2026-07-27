## ADDED Requirements

### Requirement: Buildable Distributions
The project SHALL produce both a wheel and a source distribution from a single build command.

#### Scenario: Build produces wheel and sdist
- **WHEN** a maintainer runs `uv build` (or `python -m build`) at the repo root
- **THEN** a `.whl` and a `.tar.gz` are written to `dist/`
- **AND** both artifacts include the bundled themes and the `slarti` entry point

#### Scenario: Built wheel installs and runs
- **WHEN** a user runs `pip install dist/slartibartfast-*.whl` in a clean environment
- **THEN** the `slarti` command is available on the PATH
- **AND** `slarti generate <path>` renders a site using the bundled default theme

### Requirement: PyPI Publish Workflow
The project SHALL define a documented, repeatable workflow for publishing distributions to PyPI.

#### Scenario: Publish uploads distributions
- **WHEN** a maintainer runs the documented publish command (`uv publish` or `twine upload dist/*`) with a valid PyPI token
- **THEN** the wheel and sdist for the current version are uploaded to PyPI
- **AND** the package becomes installable via `pip install slartibartfast`

#### Scenario: Release procedure is documented
- **WHEN** a maintainer reads the release documentation (`RELEASING.md`)
- **THEN** it describes bumping the version, building, verifying the artifacts, tagging the release, and publishing
- **AND** it explains how to configure the PyPI token without committing it

#### Scenario: Credentials are not committed
- **WHEN** a developer inspects the repository
- **THEN** no PyPI tokens or credentials are present in tracked files

### Requirement: Installation and Usage Documentation
The README SHALL document installing the published package and using the `slarti` CLI, without instructing users to install from source via Poetry.

#### Scenario: README leads with pip install
- **WHEN** a user reads the README installation section
- **THEN** it shows `pip install slartibartfast` as the primary install method
- **AND** it does not instruct end users to run `poetry install`

#### Scenario: Usage uses the installed CLI
- **WHEN** a user reads the README usage section
- **THEN** commands are shown as `slarti generate <path>` and `slarti serve <path>`
- **AND** development-only commands use `uv run`

#### Scenario: Testing and contributing instructions match the toolchain
- **WHEN** a contributor reads the Testing and Contributing sections
- **THEN** they reference `uv sync` / `uv run pytest` rather than Poetry commands

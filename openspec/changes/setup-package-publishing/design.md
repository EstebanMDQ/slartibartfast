## Context

The package currently cannot be installed via pip because `config.py` resolves theme paths by navigating to the parent of the package directory (`os.path.dirname(os.path.dirname(__file__))`), which only works in the source tree. Themes live at the project root in `themes/` and are not included in the built distribution.

## Goals / Non-Goals

- Goals:
  - Make `pip install slartibartfast` (or `uv pip install`) produce a working installation
  - Themes bundled inside the package wheel
  - Automated CI and PyPI publishing via GitHub Actions
  - Single source of truth for version number
- Non-Goals:
  - Publishing to conda-forge or other registries
  - Signing releases or SBOM generation
  - Auto-generating changelog from commits

## Decisions

- **Theme location: `slartibartfast/themes/`** - Move themes inside the package so they are automatically included in wheel builds. Alternative considered: using `package-data` to include a root-level `themes/` dir (rejected - non-standard, fragile across build backends).

- **Theme path resolution: `__file__`-based** - Use `os.path.join(os.path.dirname(__file__), "themes")` in `config.py`. This works in both development (editable install) and production (pip install). Alternative considered: `importlib.resources` (rejected - adds complexity for directory trees, requires Python 3.9+ `files()` API and `Traversable` handling).

- **Version source of truth: `pyproject.toml`** - Keep version in `pyproject.toml` `[project]` section. If `__init__.py` also has `__version__`, read it dynamically or remove the duplication. Alternative considered: hatch-vcs for git-tag-based versioning (rejected - adds dependency, overkill for this project size).

- **CI matrix: Python 3.10-3.13** - Test on all supported Python versions. Use `ubuntu-latest` runner. Run ruff lint + pytest in CI.

- **Publish workflow: Trusted publishing** - Use PyPI trusted publishing (OIDC) via GitHub Actions instead of API tokens. Triggered on `v*` tag push.

## Risks / Trade-offs

- Moving `themes/` is a breaking change for anyone with a custom path setup - Mitigation: document in CHANGELOG, update all path references in one commit
- GitHub Actions workflows need repository secrets or trusted publisher setup on PyPI - Mitigation: document the one-time PyPI configuration in the publish workflow comments
- `__file__`-based path resolution does not work inside zip archives - Mitigation: pip installs are unzipped by default, and zip imports are rare

## Migration Plan

1. Move `themes/` to `slartibartfast/themes/`
2. Update `config.py` path resolution
3. Verify `uv build` produces a wheel containing `slartibartfast/themes/`
4. Add CI and publish workflows
5. Tag first release as `v0.1.0`

Rollback: revert the move and path changes; themes return to project root.

## Open Questions

- Should the PyPI package name be `slartibartfast` or something shorter? (Current: `slartibartfast`)

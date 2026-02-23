## Context

The project currently uses Poetry for dependency management. Poetry uses a non-standard `[tool.poetry]` section in `pyproject.toml` instead of the PEP 621 `[project]` format that most modern Python tools understand. uv is a fast, standards-compliant alternative that supports PEP 621 natively.

## Goals / Non-Goals

- Goals:
  - Standard PEP 621 metadata in `pyproject.toml`
  - Faster dependency resolution and installs
  - Simpler developer onboarding (one tool instead of pipx + poetry)
- Non-Goals:
  - Changing runtime dependencies or behavior
  - Adding workspace/monorepo support
  - Changing the CI pipeline (handled in setup-package-publishing)

## Decisions

- **Build backend: hatchling** - Lightweight, PEP 621-native, widely adopted. Alternatives considered: setuptools (more config boilerplate), flit-core (limited build customization), pdm-backend (less mainstream).
- **Lock file: uv.lock** - uv's native lock format. Cross-platform, deterministic. Replaces `poetry.lock` directly.
- **Python version pin: .python-version** - Standard file recognized by uv, pyenv, and most tooling. Set to `3.10` as the minimum supported version.

## Risks / Trade-offs

- Developers with Poetry muscle memory need to learn uv commands - Mitigation: update README with a command mapping
- uv is newer than Poetry - Mitigation: uv has reached stable releases and is backed by Astral (ruff maintainers)
- `uv.lock` format differs from `poetry.lock` - Mitigation: one-time migration, no ongoing impact

## Migration Plan

1. Rewrite `pyproject.toml` in-place (PEP 621 + hatchling)
2. Delete `poetry.lock`
3. Run `uv lock` to generate `uv.lock`
4. Update docs
5. Verify with `uv sync && uv run pytest -q`

Rollback: revert the commit and restore `poetry.lock` from git history.

## Open Questions

- None

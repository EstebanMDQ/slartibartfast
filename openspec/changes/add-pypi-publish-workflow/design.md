## Context

The `add-package-publishing` change makes the package structurally installable (PEP 621 metadata, themes bundled inside `slartibartfast/`, `THEMES_DIR` resolved relative to the installed package, working `slarti` entry point, `dist/` ignored). What remains is the release mechanics - actually building artifacts, publishing them to PyPI - and fixing the README, which currently instructs users to `poetry install` from source. This change is the "extend" layer on top of that groundwork, targeting local installation plus public PyPI distribution.

## Goals / Non-Goals

**Goals:**
- One-command build producing wheel + sdist
- A documented, repeatable PyPI publish workflow with version bump and tagging
- A README that leads with `pip install slartibartfast` and installed-CLI usage
- Keep credentials out of the repo

**Non-Goals:**
- No CI/CD automation of publishing (manual, documented workflow only; GitHub Actions can come later)
- No Test PyPI dry-run stage (chosen target is local + PyPI; a fallback note is fine but not required)
- No changes to package metadata semantics already owned by `add-package-publishing`
- No Python source or runtime behavior changes

## Decisions

**uv as the primary build/publish tool, with a documented fallback.**
`uv build` and `uv publish` align with the `migrate-to-uv-ruff-bandit` direction and need no extra dev deps. To avoid hard-blocking on that migration, the release doc also lists the standard-tool path (`python -m build` + `twine upload`). Chosen because it keeps the happy path on uv while remaining usable today.

**Manual, documented release in `RELEASING.md`.**
A prose runbook (bump version -> build -> inspect `dist/` -> smoke-test the wheel in a clean venv -> tag -> publish) is the right altitude for a solo/small project. Alternative: a GitHub Actions release workflow - deferred as a non-goal to keep this change small and because it needs repo secrets configured out of band.

**Version is bumped in one place.**
`add-package-publishing` adds `__version__` to `__init__.py` and `version` to `[project]`. To avoid drift, the release doc specifies a single source of truth; if both must exist, document updating them together (or have `[project]` read the version dynamically via hatchling). Prefer a single manual edit point to keep the runbook simple.

**Token via environment/keyring, never committed.**
Publishing uses `UV_PUBLISH_TOKEN` (or `~/.pypirc`/keyring for twine). The doc explains configuration; nothing secret enters version control. A `.gitignore`/inspection check backs the "credentials not committed" requirement.

**README rewrite is scoped to install/usage/testing/contributing.**
Only the sections that give commands change. The prose/personality of the README is preserved; the Poetry commands become `pip install` (users) and `uv` (developers), matching the current toolchain direction.

## Risks / Trade-offs

- **Depends on `add-package-publishing` not yet applied** → Sequence apply after it; the build smoke-test (wheel installs and finds themes) will fail otherwise, which is the intended guard.
- **PyPI name `slartibartfast` may be taken** → Check availability before first publish; document the fallback of adjusting the distribution name in `[project].name` if needed.
- **Version drift between `__init__.py` and `[project]`** → Single documented bump point, or dynamic version via hatchling; called out in the runbook.
- **uv not installed for a given maintainer** → Documented `python -m build` + `twine` fallback keeps release possible.
- **First publish is irreversible (a version cannot be re-uploaded to PyPI)** → Runbook mandates a clean-venv smoke test of the built wheel before `publish`.

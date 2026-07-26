## Context

The project currently uses Poetry (`[tool.poetry]` in `pyproject.toml`, `poetry-core` build backend) for dependency management and packaging. Ruff is already configured for linting/formatting and wired into `.pre-commit-config.yaml`, but there is no automated security scanning. The local `poetry` binary is currently broken (missing interpreter), and there is a separate in-flight `migrate-poetry-to-uv` change that covers only the uv portion of this work.

This change consolidates the toolchain on Astral's uv (matching the existing Ruff usage) and adds Bandit for security static analysis, with everything enforced through pre-commit. No Python source code changes are involved.

## Goals / Non-Goals

**Goals:**
- Manage dependencies and packaging with uv using PEP 621 metadata and the hatchling build backend
- Preserve the existing Ruff lint/format configuration as the single source of truth
- Add Bandit security scanning scoped to the package source
- Run Ruff and Bandit (plus existing hygiene hooks) via pre-commit
- Keep the `slarti` CLI entry point and all developer commands working under `uv run`
- Update README and `openspec/project.md` to reflect the new workflow

**Non-Goals:**
- No changes to Python source code or runtime behavior
- No package publishing to PyPI (covered by the separate `add-package-publishing` change)
- No changes to the theme resolution / `THEMES_DIR` layout
- No CI pipeline setup (pre-commit is local; CI is out of scope here)

## Decisions

**Build backend: hatchling over poetry-core.**
uv works with any PEP 517 backend, but hatchling is the de facto default in the uv ecosystem, needs minimal configuration, and cleanly bundles the `slartibartfast` package. Alternatives: `setuptools` (more boilerplate, legacy feel) and keeping `poetry-core` (would require Poetry to build, defeating the migration). Chosen: hatchling.

**Dev dependencies in `[dependency-groups]`.**
uv supports PEP 735 dependency groups. Dev tools (pytest, ruff, pre-commit, bandit) go under `[dependency-groups].dev` rather than optional-dependencies, since they are not installable extras for end users. `uv sync` installs them by default for local development.

**Bandit configured in `pyproject.toml`, not a separate `.bandit` file.**
Keeps all tool config in one place, consistent with Ruff. `[tool.bandit]` scopes the recursive scan to `slartibartfast` and excludes `tests`. Test code commonly trips low-value rules (asserts, tmp paths), so excluding it avoids noise without hiding real issues in shipped code.

**Bandit invoked with `-c pyproject.toml` in pre-commit.**
The Bandit pre-commit hook does not read `pyproject.toml` automatically; it must be passed `-c pyproject.toml` and needs the `bandit[toml]` extra (installs `tomli` on older Pythons). The hook `args` will include `["-c", "pyproject.toml"]`.

**Ruff config is preserved verbatim.**
The existing `[tool.ruff]` / `[tool.ruff.lint]` / `[tool.ruff.format]` blocks already encode the project's conventions (line length 88, `E`/`F`/`I`, isort settings, double quotes). They are carried over unchanged; this change only ensures they remain the authority and are exercised by pre-commit.

**Supersede `migrate-poetry-to-uv`.**
Rather than layering on top of the narrower change, this change owns the full pyproject rewrite. The older change should be archived/withdrawn to avoid two proposals editing the same `[project]`/`[build-system]` sections.

## Risks / Trade-offs

- **Broken local Poetry environment blocks verification** → After the rewrite, verify with `uv sync` + `uv run pytest` (which no longer depends on Poetry). Do not rely on the existing broken `poetry` binary.
- **Bandit pre-commit hook ignores pyproject config if `-c` is omitted** → Explicitly pass `["-c", "pyproject.toml"]` in the hook args and pin `bandit[toml]`.
- **Version constraint drift when converting `^` specifiers** → Poetry `^x.y.z` maps to PEP 621 `>=x.y.z,<(next major)`. Translate each dependency explicitly rather than dropping bounds, and regenerate `uv.lock` to confirm resolution.
- **Two overlapping changes touching pyproject** → Withdraw/archive `migrate-poetry-to-uv` before applying this one so the deltas don't conflict.
- **Bandit may surface findings in existing code** → The generator uses `yaml.safe_load` (good) and `http.server` (local only). If Bandit flags anything, triage: fix, or add a scoped `# nosec` with justification, or a `skips` entry in `[tool.bandit]`. Since source is unchanged, prefer config-level skips with documented reasons over silent suppression.

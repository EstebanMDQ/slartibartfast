## 1. Preparation

- [x] 1.1 Confirm uv is installed (`uv --version`); install per Astral docs if missing
- [x] 1.2 Archive/withdraw the overlapping `migrate-poetry-to-uv` change so only this change edits `pyproject.toml`
- [x] 1.3 Record current dependency versions from `[tool.poetry.dependencies]` for accurate translation

## 2. pyproject.toml migration to uv

- [x] 2.1 Replace `[tool.poetry]` with a PEP 621 `[project]` table (name, version, description, authors, license, readme, requires-python)
- [x] 2.2 Move runtime dependencies to `[project.dependencies]`, translating `^x.y.z` to `>=x.y.z,<next-major` (typer, jinja2, watchdog, pyyaml, markdown-it-py extras)
- [x] 2.3 Move dev dependencies to `[dependency-groups].dev` and add `bandit[toml]`
- [x] 2.4 Define the `slarti` entry point under `[project.scripts]`
- [x] 2.5 Replace `[build-system]` with `hatchling` and configure it to include the `slartibartfast` package
- [x] 2.6 Preserve the existing `[tool.ruff]`, `[tool.ruff.lint]`, and `[tool.ruff.format]` blocks unchanged

## 3. Bandit configuration

- [x] 3.1 Add a `[tool.bandit]` section scoping the recursive scan to `slartibartfast` and excluding `tests`
- [x] 3.2 Run `uv run bandit -c pyproject.toml -r slartibartfast`, triage findings, and document any `skips`/`# nosec` with reasons

## 4. Lock and environment

- [x] 4.1 Delete `poetry.lock`
- [x] 4.2 Run `uv sync` to create the environment and generate `uv.lock`
- [x] 4.3 Add a `.python-version` file consistent with `requires-python`
- [x] 4.4 Update `.gitignore` if needed (do not ignore `uv.lock`; keep it committed)

## 5. Pre-commit hooks

- [x] 5.1 Update `.pre-commit-config.yaml` to run Ruff lint and Ruff format hooks
- [x] 5.2 Add a Bandit hook with `args: ["-c", "pyproject.toml"]`
- [x] 5.3 Retain existing hygiene hooks (end-of-file-fixer, trailing-whitespace, YAML/TOML checks)
- [x] 5.4 Run `uv run pre-commit run --all-files` and confirm all hooks pass

## 6. Documentation

- [x] 6.1 Update `README.md`: replace `poetry install`/`poetry run` with `uv sync`/`uv run`, add quality/security tooling notes
- [x] 6.2 Update `openspec/project.md` tech-stack and workflow sections to reference uv and Bandit

## 7. Verification

- [x] 7.1 Run `uv run pytest -q` and confirm the suite passes
- [x] 7.2 Run `uv run slarti generate site --output _build` and confirm the site builds unchanged
- [x] 7.3 Confirm no `[tool.poetry]` sections and no `poetry.lock` remain

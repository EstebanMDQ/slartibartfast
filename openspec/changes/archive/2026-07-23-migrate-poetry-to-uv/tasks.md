## 1. Migrate pyproject.toml
- [ ] 1.1 Replace `[tool.poetry]` with PEP 621 `[project]` metadata
- [ ] 1.2 Convert `[tool.poetry.dependencies]` to `[project.dependencies]` with PEP 508 version specifiers
- [ ] 1.3 Convert `[tool.poetry.group.dev.dependencies]` to `[dependency-groups]`
- [ ] 1.4 Convert `[tool.poetry.scripts]` to `[project.scripts]`
- [ ] 1.5 Replace `[build-system]` from `poetry-core` to `hatchling`
- [ ] 1.6 Keep all `[tool.ruff]` sections unchanged

## 2. Replace lock file
- [ ] 2.1 Delete `poetry.lock`
- [ ] 2.2 Run `uv lock` to generate `uv.lock`
- [ ] 2.3 Run `uv sync` to install dependencies and verify everything resolves

## 3. Verify functionality
- [ ] 3.1 Run `uv run pytest -q` and confirm all tests pass
- [ ] 3.2 Run `uv run slarti generate site --output _build` and confirm site builds
- [ ] 3.3 Run `uv run ruff check` and confirm linting works
- [ ] 3.4 Verify pre-commit hooks still work (`pre-commit run --all-files`)

## 4. Update documentation
- [ ] 4.1 Update `README.md` - replace all `poetry` references with `uv` equivalents
- [ ] 4.2 Update `openspec/project.md` - replace Poetry references with uv

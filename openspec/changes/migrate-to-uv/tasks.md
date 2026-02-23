## 1. Migrate pyproject.toml

- [x] 1.1 Rewrite `[tool.poetry]` section to PEP 621 `[project]` format
- [x] 1.2 Convert `[tool.poetry.dependencies]` to `[project.dependencies]` with PEP 508 version specifiers
- [x] 1.3 Convert `[tool.poetry.group.dev.dependencies]` to `[dependency-groups]` dev group
- [x] 1.4 Convert `[tool.poetry.scripts]` to `[project.scripts]`
- [x] 1.5 Replace `[build-system]` from `poetry-core` to `hatchling`

## 2. Lock file and Python version

- [x] 2.1 Delete `poetry.lock`
- [x] 2.2 Run `uv lock` to generate `uv.lock`
- [x] 2.3 Create `.python-version` file with `3.10`

## 3. Update documentation

- [x] 3.1 Update `README.md` to replace all `poetry` commands with `uv` equivalents
- [x] 3.2 Update `openspec/project.md` to reference uv as the package manager

## 4. Verify

- [ ] 4.1 Run `uv sync` and confirm all dependencies install correctly
- [ ] 4.2 Run `uv run pytest -q` and confirm all tests pass
- [ ] 4.3 Run `uv run slarti --help` to confirm CLI entry point works

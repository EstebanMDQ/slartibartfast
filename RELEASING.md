# Releasing

How to cut a release of Slartibartfast and publish it to PyPI.

## Before the first publish: distribution name

The PyPI name `slartibartfast` is already taken by an unrelated placeholder
package, and `slarti` is taken too. The import package name stays
`slartibartfast`, but the **distribution name** published to PyPI must be one
that is available. `slartibartfast-ssg` was available at the time of writing and
is the recommended choice.

Before the first publish, set the distribution name in `pyproject.toml`:

```toml
[project]
name = "slartibartfast-ssg"   # confirm availability first
```

The import name (`import slartibartfast`, `slarti` CLI) is unaffected by the
distribution name. Once chosen, update the `pip install` command in `README.md`
to match.

## Version source of truth

`[project].version` in `pyproject.toml` is the single source of truth. The
runtime `slartibartfast.__version__` is derived from the installed package
metadata via `importlib.metadata`, so there is nothing else to bump.

## Release steps

1. **Bump the version** in `pyproject.toml` (`[project].version`).
2. **Build** the distributions:
   ```bash
   uv build
   ```
   Confirm a `.whl` and a `.tar.gz` appear in `dist/`.
3. **Inspect** the wheel to confirm the bundled themes and entry point are
   present:
   ```bash
   python -c "import zipfile; print([n for n in zipfile.ZipFile('dist/slartibartfast-<version>-py3-none-any.whl').namelist() if '/themes/' in n])"
   ```
4. **Smoke-test** in a clean environment:
   ```bash
   uv venv /tmp/slarti-smoke
   uv pip install --python /tmp/slarti-smoke/bin/python dist/slartibartfast-*.whl
   /tmp/slarti-smoke/bin/slarti generate path/to/site --output /tmp/_smoke
   ```
5. **Tag** the release:
   ```bash
   git tag v<version>
   git push origin v<version>
   ```
6. **Publish** (see below).

## Publishing

Preferred (uv):

```bash
uv publish
```

Fallback (twine):

```bash
uv pip install twine
twine upload dist/*
```

### PyPI credentials

Use an API token from https://pypi.org/manage/account/token/.

- With uv, set the token via the environment (do **not** commit it):
  ```bash
  export UV_PUBLISH_TOKEN="pypi-..."
  ```
- With twine, either set `TWINE_USERNAME=__token__` and
  `TWINE_PASSWORD=pypi-...`, or configure `~/.pypirc`.

**Never commit tokens.** `~/.pypirc` lives in your home directory, not the repo.
Environment variables and `~/.pypirc` are the only supported credential
locations; there are no credentials in tracked files.

## Dry run

Everything above through step 4 (build, inspect, smoke-test) is a safe dry run.
The publish step is irreversible: a released version cannot be re-uploaded or
overwritten on PyPI, so only run it when the release is final.

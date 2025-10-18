# Slartibartfast

A tiny, fast static site generator — designed for people who prefer tea, good fonts,
and a minimal toolchain. If you're carrying a towel, you're already halfway there.

## What it is

Slartibartfast builds static HTML from a directory of Markdown files and a
simple theme. It supports front matter for per-page metadata, uses Jinja2 for
templating, and Markdown-It for rendering Markdown (with front-matter and
footnote plugins).

The project name is a gentle nod to cosmic coastline designers; the generator
tries to be tidy and practical rather than overwhelmingly clever.

## Install

Recommended: use Poetry (project already includes a `pyproject.toml`). From the
project root:

```bash
poetry install
```

This will create a virtual environment and install runtime + dev dependencies.

Alternative: create a virtualenv and install dependencies manually:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install "typer" "jinja2" "pyyaml" "markdown-it-py[plugins]" pytest
```


## Quick usage

The package exposes a CLI via the `slarti` script (installed by Poetry)
or you can run the Typer app directly.

Generate a site from a content directory:

```bash
# using Poetry-managed script
poetry run slarti generate path/to/content --output _build

# or run the module directly
python -m slartibartfast.cli generate path/to/content --output _build
```

Serve a generated site locally (serves files from the given directory on port
8000):

```bash
poetry run slarti serve --path _build
# or
python -m slartibartfast.cli serve --path _build
```

Note: the server command uses Python's builtin `http.server` — it's fine for
local previews but not intended as a production webserver (nor does it have a
Babel fish to translate HTTP headers).

## Themes and templates

Themes live in the `themes/` directory. A minimal theme is provided at
`themes/minimal`. Templates are standard Jinja2 templates; pages may specify a
`template` in their front matter to pick a different template file.

## Testing

Run the test suite with Poetry:

```bash
poetry run pytest -q
```

Or with pytest directly if you set `PYTHONPATH` to the project root:

```bash
PYTHONPATH=. pytest -q
```

## Contributing

Contributions are welcome. If you're making changes, prefer small, focused
PRs. Add tests for new behavior and run `poetry run pytest` before opening the
PR.

## License

MIT — see `LICENSE` for details.

----

A small, helpful reminder: don't panic. If the universe seems a bit absurd,
sometimes an opinionated static site generator and a hot cup of tea are a good
start.

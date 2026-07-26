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

Recommended: use [uv](https://docs.astral.sh/uv/) (project already includes a
`pyproject.toml`). From the project root:

```bash
uv sync
```

This will create a virtual environment and install runtime + dev dependencies,
and generate `uv.lock`.

Alternative: create a virtualenv and install the package manually:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install .
```


## Quick usage

The package exposes a CLI via the `slarti` script (installed into the
environment) or you can run the Typer app directly.

Generate a site from a content directory:

```bash
# using the uv-managed environment
uv run slarti generate path/to/content --output _build

# or run the module directly
python -m slartibartfast.cli generate path/to/content --output _build
```

Serve a generated site locally (watches the content directory and serves the
built site on port 8000):

```bash
uv run slarti serve path/to/content --output _build
# or
python -m slartibartfast.cli serve path/to/content --output _build
```

Note: the server command uses Python's builtin `http.server` - it's fine for
local previews but not intended as a production webserver (nor does it have a
Babel fish to translate HTTP headers).

## Themes and templates

Themes live in the `themes/` directory. A minimal theme is provided at
`themes/minimal`. Templates are standard Jinja2 templates; pages may specify a
`template` in their front matter to pick a different template file.

## Navigation and Sitemap

Slartibartfast automatically generates:

- **Navigation menu**: Available in templates as `site.navigation`
- **XML Sitemap**: Generated at `/sitemap.xml`

### Page metadata for navigation

You can control navigation behavior with front matter:

```yaml
---
title: "Page Title"
description: "Page description for navigation and SEO"
published: true       # Required to publish (default: false, opt-in)
nav_order: 1          # Lower numbers appear first (default: 999)
in_nav: true          # Include in navigation menu (default: true)
---
```

### Publishing and navigation defaults

- **`published`** defaults to `false`. Publishing is opt-in: a page or section
  is only generated when its front matter (or a section's `_config.yaml`) sets
  `published: true`. A `publish_date` in the future also excludes content until
  that date. These rules apply the same way to both pages and sections.
- **`in_nav`** defaults to `true` for both pages and sections. Set
  `in_nav: false` to keep an item out of the navigation menu (for example,
  individual blog posts that are listed by their section index).

### Template context

Templates have access to:

- `meta`: Current page metadata
- `content`: Rendered markdown content
- `site.config`: Site configuration from `_config.yaml`
- `site.navigation`: Array of navigation items
- `site.pages`: Array of all page metadata
- `site.sitemap_url`: URL to the sitemap (`/sitemap.xml`)

Example template usage:

```html
<!-- Navigation menu -->
<nav>
  <ul>
    {% for nav_item in site.navigation %}
    <li><a href="{{ nav_item.url }}">{{ nav_item.title }}</a></li>
    {% endfor %}
  </ul>
</nav>

<!-- List recent pages -->
{% for page in site.pages[:5] %}
  <a href="{{ page.url }}">{{ page.title }}</a>
{% endfor %}
```

## Testing

Run the test suite with uv:

```bash
uv run pytest -q
```

Or with pytest directly if you set `PYTHONPATH` to the project root:

```bash
PYTHONPATH=. pytest -q
```

## Contributing

Contributions are welcome. If you're making changes, prefer small, focused
PRs. The project uses uv for environment management, Ruff for linting and
formatting, Bandit for security scanning, and pre-commit to run them all.
Install the hooks with `uv run pre-commit install`, add tests for new
behavior, and run `uv run pytest` before opening the PR.

## License

MIT — see `LICENSE` for details.

----

A small, helpful reminder: don't panic. If the universe seems a bit absurd,
sometimes an opinionated static site generator and a hot cup of tea are a good
start.

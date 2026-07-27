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

> Not yet on PyPI under an available name (the `slartibartfast` name is taken by
> an unrelated package). Until it is published, install from source or Git. See
> [RELEASING.md](RELEASING.md) for the publishing plan.

Install the `slarti` CLI as a tool with [uv](https://docs.astral.sh/uv/):

```bash
# from a local checkout
uv tool install .

# or straight from Git
uv tool install git+https://github.com/informalthinkers/slartibartfast
```

Or with pip:

```bash
pip install .
# or
pip install git+https://github.com/informalthinkers/slartibartfast
```

Once published to PyPI, installation will be:

```bash
pip install slartibartfast-ssg   # distribution name; the CLI stays `slarti`
```

## Quick usage

After installing, the `slarti` command is available directly.

Generate a site from a content directory:

```bash
slarti generate path/to/content --output _build
```

Serve a generated site locally (watches the content directory and serves the
built site on port 8000):

```bash
slarti serve path/to/content --output _build
```

Working from a source checkout with `uv sync` instead? Prefix commands with
`uv run` (e.g. `uv run slarti generate ...`), or run the module directly with
`python -m slartibartfast.cli generate ...`.

Note: the server command uses Python's builtin `http.server` - it's fine for
local previews but not intended as a production webserver (nor does it have a
Babel fish to translate HTTP headers).

## Themes and templates

Themes are bundled with the package under `slartibartfast/themes/`; `default`
and `minimal` themes are provided. A site directory can also override a theme by
placing a directory of the same name alongside its content. Templates are
standard Jinja2 templates; pages may specify a `template` in their front matter
to pick a different template file.

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

Contributions are welcome. Set up a development environment with
[uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

If you're making changes, prefer small, focused PRs. The project uses uv for
environment management, Ruff for linting and formatting, Bandit for security
scanning, and pre-commit to run them all. Install the hooks with
`uv run pre-commit install`, add tests for new behavior, and run
`uv run pytest` before opening the PR.

See [RELEASING.md](RELEASING.md) for how releases are built and published.

## License

MIT — see `LICENSE` for details.

----

A small, helpful reminder: don't panic. If the universe seems a bit absurd,
sometimes an opinionated static site generator and a hot cup of tea are a good
start.

# Project Context

## Purpose
Slartibartfast is a tiny, fast static site generator for building HTML from Markdown files. It targets users who want a minimal toolchain - no complex build pipelines, just Markdown content, Jinja2 templates, and a theme system.

Key goals:
- Generate static HTML from a directory of Markdown files with YAML front matter
- Support theming via Jinja2 templates
- Auto-generate navigation menus and XML sitemaps
- Provide a local dev server with file-watching and auto-regeneration
- Support sections (subdirectories with their own `_config.yaml`)
- Copy static assets (images, CSS, JS) from both content and theme directories

## Tech Stack
- Python 3.10+ (primary language)
- Typer (CLI framework)
- Jinja2 (templating engine)
- markdown-it-py with plugins (Markdown rendering, front matter, footnotes, tables)
- PyYAML (configuration parsing)
- Watchdog (file system monitoring for dev server)
- uv (dependency management, virtual environment, and packaging via hatchling)
- Ruff (linting and formatting)
- Bandit (security static analysis)
- pytest (testing)
- pre-commit (Git hooks for linting/formatting/security)

## Project Conventions

### Code Style
- PEP 8 formatting enforced via Ruff (line length 88)
- Double quotes for strings
- Space indentation
- Import sorting via Ruff isort rules (`known-first-party = ["slartibartfast"]`)
- Type hints required
- Straight quotes only - no curly quotes
- No em dashes or en dashes - use regular hyphens

### Architecture Patterns
- Single-package layout: `slartibartfast/` contains all source modules
- `cli.py` - Typer CLI entry point with `generate` and `serve` commands
- `generator.py` - Core site generation logic (page collection, rendering, sitemap, asset copying)
- `config.py` - Global constants (theme dir, output dir, base dir)
- `server.py` - Local dev server with watchdog-based auto-regeneration
- Themes live in `themes/` at project root; each theme is a directory of Jinja2 templates
- Content directories use `_config.yaml` for section configuration
- Pages use YAML front matter for per-page metadata (`title`, `description`, `nav_order`, `in_nav`, `published`, `publish_date`, `template`)

### Testing Strategy
- Tests in `tests/` directory using pytest
- `conftest.py` for shared fixtures
- `test_generator.py` for core generation logic
- `test_cli.py` for CLI integration tests
- Run with `uv run pytest -q`

### Git Workflow
- Main branch: `main`
- Pre-commit hooks: Ruff linting with auto-fix, Ruff formatting, Bandit security scan, end-of-file fixer, trailing whitespace, YAML/TOML checks
- Concise commit messages

## Domain Context
- The `site/` directory is an example content directory (not part of the package itself)
- A "section" is a subdirectory with its own `_config.yaml` (e.g., `site/blog/`)
- Pages with `published: false` or a future `publish_date` are skipped during generation
- Navigation is built from pages with `in_nav: true` and sorted by `nav_order`
- Templates receive `content` (rendered HTML), `meta` (page front matter), `site` (global context with config, pages, sitemap_url), `navigation` (nav items with active state), and `section_pages`
- The CLI entry point is `slarti` (defined under `[project.scripts]`)

## Important Constraints
- Python >=3.10, <3.14
- No production web server - the `serve` command uses Python's built-in `http.server` for local preview only
- Themes are resolved by checking source directory first, then global `themes/` directory
- Template files (.html, .htm) in themes are not copied as assets; only non-template files (CSS, JS, images) are

## External Dependencies
- No external services or APIs
- All processing is local and file-based
- markdown-it-py plugins: front_matter, footnote, linkify, table support

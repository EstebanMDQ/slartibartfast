# Project Context

## Purpose

Slartibartfast is a tiny, fast static site generator for people who prefer simplicity and a minimal toolchain. It builds static HTML from a directory of Markdown files and Jinja2 templates, with YAML front matter for per-page metadata.

Goals:
- Stay small and practical - avoid framework bloat
- Support hierarchical content (pages and sections like blog/)
- Provide automatic navigation, sitemaps, and publishing control
- Include a development server with hot reload for local previews
- Ship usable themes out of the box

Non-goals:
- Being a CMS or content management platform
- Supporting databases or dynamic server-side logic
- Competing with large generators like Hugo or Jekyll on feature count

## Tech Stack

- **Language**: Python 3.10+ (target: >=3.10, <3.14)
- **Package manager**: uv
- **CLI framework**: Typer
- **Templating**: Jinja2 with template inheritance
- **Markdown rendering**: markdown-it-py with linkify and footnote plugins
- **Front matter**: PyYAML
- **File watching**: watchdog (for hot reload dev server)
- **Linting/formatting**: Ruff (PEP 8, pyflakes, isort)
- **Testing**: pytest
- **Pre-commit hooks**: ruff + basic file checks

## Project Conventions

### Code Style

- PEP 8 via Ruff with line length 88
- Double quotes for strings
- Space-based indentation
- Import sorting with isort rules (first-party: slartibartfast)
- Lint rules: E (pycodestyle), F (pyflakes), I (isort)
- Type hints for function signatures
- Simple solutions over clever ones - avoid unnecessary abstractions

### Architecture Patterns

- **Single-package layout**: all source code lives in `slartibartfast/`
- **Separation of concerns**: `cli.py` (commands), `generator.py` (core logic), `server.py` (dev server), `config.py` (constants)
- **Convention over configuration**: sensible defaults with YAML overrides
- **Theme system**: themes/ directory with Jinja2 templates and static assets; themes can be overridden per-site or per-page
- **Hierarchical content**: sections (subdirectories with their own `_config.yaml`) are processed recursively
- **Static asset pipeline**: non-markdown directories are copied as-is to output

### Testing Strategy

- pytest with fixtures and tmp_path for file I/O tests
- Integration tests that exercise the full generation pipeline
- Unit tests for individual functions (publishing logic, navigation, sitemap)
- CLI tests using Typer's test runner
- Tests live in `tests/` and mirror the source structure
- Run with: `uv run pytest -q`

### Git Workflow

- Single `main` branch for trunk-based development
- Concise commit messages
- Pre-commit hooks enforce formatting and linting before each commit
- Small, focused PRs with tests for new behavior

## Domain Context

Key concepts:
- **Page**: a Markdown file with YAML front matter that gets rendered to HTML
- **Section**: a subdirectory containing pages and its own `_config.yaml` (e.g., blog/)
- **Theme**: a directory of Jinja2 templates and static assets (CSS, JS, images)
- **Front matter**: YAML metadata at the top of each Markdown file (title, description, date, tags, nav_order, template, published, publish_date)
- **Navigation**: auto-generated from page metadata, sorted by nav_order, with active state tracking
- **Sitemap**: auto-generated XML sitemap at /sitemap.xml
- **Publishing control**: pages can be excluded via `published: false` or future `publish_date`

Template context available to themes:
- `meta` - current page metadata
- `content` - rendered HTML from markdown
- `site.config` - site-level configuration from `_config.yaml`
- `site.navigation` - sorted navigation items
- `site.pages` - all page metadata
- `site.sitemap_url` - sitemap URL

## Important Constraints

- Must run on Python 3.10 through 3.13 (no 3.14+ yet)
- No runtime dependencies beyond the five core libraries (typer, jinja2, pyyaml, markdown-it-py, watchdog)
- The dev server uses Python's built-in http.server - not for production use
- Themes must work with standard Jinja2 (no custom extensions)
- Output is purely static HTML/CSS/JS - no server-side processing

## External Dependencies

No external services or APIs. The generator operates entirely on local files:
- Input: Markdown files + YAML config + Jinja2 templates
- Output: static HTML, CSS, JS, and assets in an output directory

The only network activity is the local dev server (localhost:8000).

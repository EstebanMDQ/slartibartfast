## 1. Metadata correctness

- [x] 1.1 Fix the `filepath` value in `collect_pages_metadata` so it is the source path once (no doubled subfolder/root)
- [x] 1.2 Change the directory vs `.md` handling to `if`/`elif` so an entry is treated as one or the other
- [x] 1.3 Re-enable deterministic ordering of `pages_metadata` by `(nav_order, title)`

## 2. Publish and navigation semantics

- [x] 2.1 Route sections through `should_process` so `published`/`publish_date` apply consistently to pages and sections
- [x] 2.2 Use a single documented `in_nav` default for both pages and sections
- [x] 2.3 Confirm publishing stays opt-in (`published: true` required) and keep the behavior centralized in `should_process`
- [x] 2.4 Document publish and `in_nav` defaults in `README.md`

## 3. Front-matter parsing

- [x] 3.1 Rewrite `_extract_config_header` to only close on a line-anchored `---`, preserving body `---` and YAML `---`
- [x] 3.2 Remove the redundant markdown-it front-matter handling (front matter is parsed once by manual extraction)
- [x] 3.3 Confirm footnote, table, and linkify plugins remain enabled and working

## 4. Output escaping

- [x] 4.1 XML-escape URLs and dates in `generate_sitemap` (e.g., `xml.sax.saxutils.escape`)
- [x] 4.2 Enable Jinja `autoescape` in `template_loader`'s `Environment`
- [x] 4.3 Wrap rendered Markdown `content` in `Markup` (or render with `|safe`) so it is not double-escaped
- [x] 4.4 Audit `themes/default` and `themes/minimal` templates for assumptions about unescaped output and adjust

## 5. Tests

- [x] 5.1 Test `filepath` is correct for root and nested pages
- [x] 5.2 Test a directory named `*.md` is treated only as a section, not a page
- [x] 5.3 Test `site.pages` ordering is deterministic and by `(nav_order, title)`
- [x] 5.4 Test section respects `published: false` and future `publish_date`
- [x] 5.5 Test the documented `in_nav` default for pages and sections
- [x] 5.6 Test front-matter edge cases: body `---`, empty front matter, no front matter, `---` inside YAML
- [x] 5.7 Test sitemap output is valid XML when a URL contains `&`
- [x] 5.8 Test metadata with HTML characters is escaped and rendered `content` is not double-escaped

## 6. Verification

- [x] 6.1 Run the full test suite and confirm it passes
- [x] 6.2 Regenerate the example `site/` and confirm output is correct (nav, ordering, sitemap valid)

## Why

Code review of `generator.py` surfaced several correctness, robustness, and security defects that are unrelated to the dev-server loop already covered by `fix-serve-watcher-loop`. They range from silent bugs (a mangled `filepath`, a missing `elif`, unsorted pages) to a user-hostile publishing default and unescaped output that can produce invalid or unsafe HTML/XML.

## What Changes

- Fix the double-prefixed `filepath` metadata value (currently `blog/site/blog/post.md` for a nested page)
- Change the page-collection loop so a directory and a `.md` file are mutually exclusive branches (`if`/`elif`), so a directory named `foo.md` is not processed as both
- Restore deterministic page ordering (currently the sort is commented out, so `site.pages` follows filesystem order)
- Make publish/visibility defaults consistent and documented:
  - Apply the same publish check (`should_process`) to sections as to pages, so `published`/`publish_date` behave consistently
  - Align the `in_nav` default with the documented behavior and keep it consistent between pages and sections
  - Keep pages opt-in for publishing (`published: true` still required) but document this clearly in the README so it is not a silent footgun
- Harden front-matter extraction so a `---` in the body or inside the YAML does not corrupt parsing, and remove the now-redundant markdown-it front-matter handling
- Fix output-escaping defects:
  - XML-escape URLs and dates in the generated sitemap
  - Enable Jinja autoescape for HTML templates while explicitly marking the trusted rendered-Markdown `content` as safe, so page metadata cannot inject markup
- **BREAKING (behavioral)**: `in_nav` default and page-ordering may change which items appear in navigation and in what order; `site.pages` ordering becomes deterministic

## Capabilities

### New Capabilities
<!-- None; this extends the existing site-generation capability. -->

### Modified Capabilities
- `site-generation`: correctness and robustness of page collection, publish/visibility semantics, front-matter parsing, and output escaping. Added as new requirements on the same capability the `fix-serve-watcher-loop` change also extends (no overlapping requirements).

## Impact

- Affected code: `slartibartfast/generator.py` (primary), theme templates if they rely on `content` being pre-escaped, `README.md` (document publish/nav defaults)
- Affected tests: `tests/test_generator.py` (add cases for filepath, ordering, publish/nav defaults, front-matter edge cases, sitemap/template escaping)
- Coordinates with `fix-serve-watcher-loop` (same capability, disjoint requirements) - either order is fine
- No new dependencies

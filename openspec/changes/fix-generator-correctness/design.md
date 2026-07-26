## Context

`generator.py` is the core of the SSG. A review found defects across four areas: metadata correctness (`filepath`, `if` vs `elif`, commented-out sort), publish/visibility semantics that differ between pages and sections and contradict the README, fragile front-matter parsing, and unescaped output (sitemap XML, template rendering). The dev-server loop and hardcoded `_build` are out of scope here - they belong to `fix-serve-watcher-loop`. These fixes touch behavior, so a couple of decisions were confirmed with the maintainer: publishing stays opt-in (but documented and made consistent), and the security cleanup covers both the sitemap and template rendering.

## Goals / Non-Goals

**Goals:**
- Correct the silent metadata bugs (`filepath`, branch exclusivity, deterministic ordering)
- Make publish and `in_nav` semantics consistent between pages and sections and document them
- Parse front matter robustly and remove redundant handling
- Escape output: valid sitemap XML and safe template rendering

**Non-Goals:**
- The serve/watcher loop and dynamic output-dir exclusion (owned by `fix-serve-watcher-loop`)
- Changing the opt-in publishing model (kept, just documented and made consistent)
- Reworking the theme or metadata schema beyond what the fixes require
- New features

## Decisions

**Publishing stays opt-in, applied consistently.**
`should_process` currently runs on pages only; sections default `published: True` and skip the check. The fix routes sections through the same check so `published`/`publish_date` mean the same thing everywhere. The default stays `False` (opt-in) per the maintainer, with a clear README note so an unpublished new page is not a mystery. Alternative (default-published) was rejected to avoid changing existing sites' output.

**`in_nav` default aligned to the README.**
README documents `in_nav: true` as the default, but pages default to `False` in code while sections default `True`. The fix uses one documented default for both. This can change which items appear in nav (flagged BREAKING/behavioral in the proposal); a test pins the chosen default.

**Deterministic ordering via the existing (commented-out) sort key.**
Re-enable sorting by `(nav_order, title)` for `pages_metadata` so `site.pages` is stable. Navigation already sorts independently; this makes the page list match.

**Front-matter parsing: anchor the closing delimiter.**
Replace `content.find("---", 3)` with a parse that only treats a `---` on its own line as the closing fence (e.g., split on a line-anchored delimiter), so a body thematic break or `---` inside YAML does not truncate. Since front matter is stripped manually before `md.render`, the markdown-it `front_matter_plugin` never sees it - remove that redundancy (either drop the plugin, or stop stripping manually and let the plugin own it). Chosen: keep manual extraction (we need the parsed dict for metadata) and drop the redundant plugin use, documenting that front matter is handled once.

**Escaping: `xml.sax.saxutils.escape` for the sitemap; Jinja autoescape + `Markup` for templates.**
Sitemap URLs/dates are f-string-interpolated today; wrap them with `escape(...)`. For templates, enable `autoescape=True` on the Jinja `Environment` so metadata (title, description) is escaped, and wrap the already-rendered Markdown `content` in `markupsafe.Markup` (or `|safe`) so it is not double-escaped. This treats content as trusted (it is authored Markdown) while treating metadata interpolation as escaped by default. `markupsafe` ships with Jinja2, so no new dependency.

**Markdown `html: True` retained.**
Disabling raw HTML in Markdown would break legitimate authoring in an SSG. The trust boundary is the template layer (autoescape for metadata), not the Markdown renderer. Documented as an explicit decision.

## Risks / Trade-offs

- **Behavioral changes to nav and ordering** → Flagged BREAKING in the proposal; add tests pinning the new defaults and update the example `site/` output if needed.
- **Enabling Jinja autoescape can double-escape or break existing themes** → Audit `themes/default` and `themes/minimal` for places that assume raw output; mark `content` safe and adjust any template that relied on unescaped metadata. Covered by tests rendering metadata with HTML characters.
- **Front-matter parser rewrite could regress edge cases** → Add tests for: normal front matter, body `---`, no front matter, empty front matter, and `---` inside YAML values.
- **Removing markdown-it front-matter plugin** → Confirm nothing else depends on it; footnote/table/linkify plugins are unaffected.
- **Coordinating with `fix-serve-watcher-loop`** → Both extend `site-generation` with disjoint requirements; if both are applied, verify combined tests pass.

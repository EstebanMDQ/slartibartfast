## ADDED Requirements

### Requirement: Correct Page Filepath Metadata
The page metadata `filepath` value SHALL be a single, correct path to the source file, not a doubly-prefixed path.

#### Scenario: Nested page filepath
- **WHEN** a page exists in a section subfolder (e.g., `blog/post.md`)
- **THEN** its `filepath` metadata resolves to the actual source path once
- **AND** it does not contain a duplicated subfolder or root segment

### Requirement: Mutually Exclusive Collection Branches
Page collection SHALL treat a filesystem entry as either a section directory or a Markdown file, never both.

#### Scenario: Directory named like a Markdown file
- **WHEN** the content directory contains a directory whose name ends in `.md`
- **THEN** it is processed only as a directory (section) if it has a `_config.yaml`
- **AND** it is not also processed as a Markdown page

### Requirement: Deterministic Page Ordering
Collected pages SHALL be ordered deterministically rather than by filesystem enumeration order.

#### Scenario: Stable ordering across runs
- **WHEN** a site is generated more than once from unchanged content
- **THEN** `site.pages` appears in the same order each run
- **AND** the order is by `nav_order` then `title`

### Requirement: Consistent Publish Semantics
Publish and publish-date checks SHALL apply consistently to both pages and sections.

#### Scenario: Section respects published flag
- **WHEN** a section's `_config.yaml` sets `published: false`
- **THEN** the section is excluded from generation the same way an unpublished page is

#### Scenario: Future publish date excludes content
- **WHEN** a page or section has a `publish_date` in the future
- **THEN** it is excluded from the generated site until that date

#### Scenario: Unpublished pages remain opt-in and documented
- **WHEN** a page has no `published` value in its front matter
- **THEN** it is not published (publishing remains opt-in via `published: true`)
- **AND** this requirement is documented in the README

### Requirement: Consistent Navigation Inclusion Default
The `in_nav` default SHALL match the documented behavior and be consistent between pages and sections.

#### Scenario: Default matches documentation
- **WHEN** a page or section does not specify `in_nav`
- **THEN** the applied default equals the value documented in the README
- **AND** the same default is used for both pages and sections

### Requirement: Robust Front-Matter Extraction
Front-matter parsing SHALL correctly separate YAML front matter from body content even when the body or YAML contains `---`.

#### Scenario: Body contains a horizontal rule
- **WHEN** a Markdown file has valid front matter followed by a body containing a `---` thematic break
- **THEN** only the leading front-matter block is parsed as YAML
- **AND** the full body (including the `---`) is preserved as content

#### Scenario: No redundant front-matter handling
- **WHEN** the Markdown renderer is configured
- **THEN** front matter is stripped exactly once before rendering
- **AND** there is no duplicate front-matter processing between manual extraction and the renderer

### Requirement: Escaped Sitemap Output
The generated sitemap SHALL be well-formed XML with special characters escaped.

#### Scenario: URL contains an ampersand
- **WHEN** a page URL or base URL contains characters that are special in XML (e.g., `&`)
- **THEN** the sitemap escapes them so the output is valid XML

### Requirement: Safe Template Rendering
HTML template rendering SHALL escape untrusted page metadata by default while treating the rendered Markdown body as trusted.

#### Scenario: Metadata cannot inject markup
- **WHEN** a page's front-matter field (e.g., `title`) contains HTML characters
- **THEN** the value is escaped when rendered into a template

#### Scenario: Rendered content passes through
- **WHEN** the rendered Markdown `content` is inserted into a template
- **THEN** it is rendered as intended HTML (marked safe) and not double-escaped

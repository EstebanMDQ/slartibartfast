## ADDED Requirements

### Requirement: Jinja2 Environment Caching

The site generator SHALL create a single Jinja2 `Environment` per site build and reuse it across all page renders, rather than creating a new environment per page.

#### Scenario: Environment reused across pages
- **WHEN** `generate_site()` renders multiple pages
- **THEN** the same Jinja2 `Environment` instance SHALL be used for all template lookups within that build

### Requirement: Efficient Navigation Active State

The site generator SHALL mark navigation active state without deep-copying the navigation list for each page.

#### Scenario: Active navigation item set and reset
- **WHEN** a page is rendered
- **THEN** the matching navigation item SHALL be marked active before rendering
- **AND** the active flag SHALL be reset after rendering

### Requirement: Efficient Directory Traversal

Directory listing operations SHALL use `os.scandir()` instead of `os.listdir()` combined with separate `os.path.isdir()` or `os.path.exists()` calls.

#### Scenario: Directory entries checked without extra stat calls
- **WHEN** `collect_pages_metadata()` or `copy_static_directories()` iterates over a directory
- **THEN** it SHALL use `os.scandir()` to avoid redundant filesystem stat calls

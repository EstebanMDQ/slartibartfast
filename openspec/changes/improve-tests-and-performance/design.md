## Context

The site generator has performance bottlenecks that become noticeable with larger sites (50+ pages). The Jinja2 `Environment` is created fresh for every page via `template_loader()`, navigation is deep-copied per page, and directory traversal uses multiple stat calls per entry.

## Goals / Non-Goals

- Goals:
  - Reduce per-page overhead in `generate_site()` loop
  - Achieve test coverage for all public functions
  - Zero behavior changes in generated output
- Non-Goals:
  - Async/parallel page generation
  - Caching across builds (only within a single build)
  - Restructuring the module layout

## Decisions

- **Jinja2 Environment caching**: Create the `Environment` once at the start of `generate_site()` and pass it to `template_loader()` (or load templates directly). This avoids repeated filesystem scanning for the template search path. Alternative considered: global module-level cache (rejected - complicates testing and theme switching).

- **Navigation active marking**: Instead of `deepcopy(navigation)` per page, set `active=True` on the matching nav item before rendering, then reset it to `False` after. This eliminates O(n) list copies. Alternative considered: generating a separate nav context dict per page (rejected - more complex, same result).

- **os.scandir() for directory traversal**: Replace `os.listdir()` + `os.path.isdir()` with `os.scandir()` which returns `DirEntry` objects with cached `is_dir()` results, avoiding redundant stat calls. This is a drop-in improvement with no API changes.

## Risks / Trade-offs

- In-place navigation mutation is slightly more fragile than deepcopy - Mitigation: reset active flag in a finally block to ensure cleanup
- Jinja2 env caching changes the `template_loader()` signature - Mitigation: keep backward compatibility or update all call sites in one commit

## Open Questions

- None

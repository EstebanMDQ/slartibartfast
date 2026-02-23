# Change: Improve test coverage and site generation performance

## Why

Several core modules have zero or minimal test coverage (`server.py`, `_extract_config_header()`, `load_config()`), leaving bugs undetected. The site generator also has performance bottlenecks: Jinja2 environments are recreated per page, navigation is deep-copied per page, and directory listing uses double-stat patterns.

## What Changes

- Add unit tests for `server.py` (`ReloadEventHandler`, `serve` function)
- Add direct unit tests for `_extract_config_header()` edge cases (malformed YAML, missing delimiters)
- Add direct unit tests for `load_config()` (missing file, invalid YAML)
- Add tests for `generate_navigation()` and `generate_sitemap()` edge cases
- Add tests for error paths in `generate_site()`
- Cache the Jinja2 `Environment` per site build instead of creating one per page
- Replace deep-copy of navigation per page with in-place active item marking and reset
- Replace `os.listdir()` + `os.path.exists()` with `os.scandir()` in directory traversal

## Impact

- Affected specs: site-generation (new)
- Affected code: `slartibartfast/generator.py`, `tests/test_generator.py`, `tests/test_server.py`
- No breaking changes - internal optimizations and new tests only

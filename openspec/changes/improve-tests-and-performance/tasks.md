## 1. Add missing unit tests

- [x] 1.1 Create `tests/test_server.py` with tests for `ReloadEventHandler` (on_modified, on_created) and `serve()` function setup
- [ ] 1.2 Add direct tests for `_extract_config_header()`: valid front matter, missing end delimiter, empty content, malformed YAML
- [ ] 1.3 Add direct tests for `load_config()`: missing config file raises `FileNotFoundError`, invalid YAML handling
- [ ] 1.4 Add tests for `generate_navigation()`: empty input, pages with `in_nav=False`, sorting by `nav_order`
- [ ] 1.5 Add edge case tests for `generate_sitemap()`: empty pages list, missing `base_url`, invalid date formats
- [ ] 1.6 Add tests for `generate_site()` error paths: template not found, write permission errors

## 2. Performance optimizations

- [ ] 2.1 Cache the Jinja2 `Environment` per site build in `generate_site()` instead of creating a new one in `template_loader()` for each page
- [ ] 2.2 Replace `deepcopy(navigation)` per page with setting/resetting active flags in-place
- [ ] 2.3 Replace `os.listdir()` + `os.path.isdir()` / `os.path.exists()` with `os.scandir()` in `collect_pages_metadata()` and `copy_static_directories()`

## 3. Verify

- [ ] 3.1 Run full test suite and confirm all tests pass
- [ ] 3.2 Generate the example site and compare output to verify no regressions

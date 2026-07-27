## 1. Fix watcher output directory exclusion
- [x] 1.1 Resolve output path to absolute in `ReloadEventHandler.__init__`
- [x] 1.2 Skip events whose `src_path` is inside the output directory in `on_modified` and `on_created`

## 2. Add debouncing
- [x] 2.1 Add a debounce mechanism (e.g., timer-based) so multiple rapid events coalesce into a single regeneration
- [x] 2.2 Choose a reasonable debounce interval (e.g., 300-500ms)

## 3. Add file-type filtering
- [x] 3.1 Only trigger regeneration for content-relevant file extensions (`.md`, `.yaml`, `.yml`, `.html`, `.css`, `.js`, image formats)
- [x] 3.2 Ignore hidden files/directories (paths containing `/.`)

## 4. Fix hardcoded `_build` in generator
- [x] 4.1 Change `copy_static_directories` to accept the output directory name and skip it dynamically instead of hardcoding `_build`
- [x] 4.2 Update `generate_site` to pass the output path to `copy_static_directories`

## 5. Clean up observer lifecycle
- [x] 5.1 Call `observer.stop()` and `observer.join()` in the shutdown path

## 6. Tests
- [x] 6.1 Add test for watcher ignoring output directory events
- [x] 6.2 Add test for `copy_static_directories` skipping a custom output directory name
- [x] 6.3 Update existing tests if signatures change

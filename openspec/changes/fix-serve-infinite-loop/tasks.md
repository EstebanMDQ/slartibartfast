## 1. Fix event handler in server.py

- [x] 1.1 Add output directory path filtering to `ReloadEventHandler.on_modified()` and `on_created()` - skip events where `event.src_path` starts with the resolved output directory
- [x] 1.2 Add debouncing (e.g., 0.5s cooldown) to prevent rapid successive rebuilds from multiple filesystem events

## 2. Fix hardcoded output path in generator.py

- [x] 2.1 Change `copy_static_directories()` to accept the output directory name as a parameter instead of hardcoding `_build`
- [x] 2.2 Update `generate_site()` to pass the actual output path to `copy_static_directories()`

## 3. Add tests

- [x] 3.1 Create `tests/test_server.py` with tests for `ReloadEventHandler` path filtering
- [x] 3.2 Add test for debounce behavior
- [x] 3.3 Add test for `copy_static_directories()` skipping the actual output directory

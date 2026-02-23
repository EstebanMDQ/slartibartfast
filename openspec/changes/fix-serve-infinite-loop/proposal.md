# Change: Fix serve command infinite regeneration loop

## Why

The `serve` command's file watcher triggers infinite regeneration when the output directory is inside the watched project directory. Watchdog detects generated files as changes, which triggers another build, creating an endless loop.

## What Changes

- Add path filtering in `ReloadEventHandler` to ignore filesystem events originating from the output directory
- Add debouncing to coalesce rapid filesystem events into a single rebuild
- Fix hardcoded `_build` skip in `copy_static_directories()` to use the actual configured output path instead

## Impact

- Affected specs: dev-server (new)
- Affected code: `slartibartfast/server.py`, `slartibartfast/generator.py`
- New test file: `tests/test_server.py`
- No breaking changes - fixes incorrect behavior

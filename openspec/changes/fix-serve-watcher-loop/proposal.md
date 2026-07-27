# Change: Fix serve command watcher regeneration loop

## Why
The `serve` command's file watcher triggers infinite regeneration loops. When the output directory (default `_build`) is inside the watched content directory (e.g., `slarti serve .`), every file written by `generate_site` triggers another `on_modified`/`on_created` event, which regenerates the site, which writes more files, and so on. Secondary issues: no debouncing (editors fire multiple events per save), no file-type filtering (`.pyc`/`.DS_Store` changes trigger rebuilds), and `copy_static_directories` hardcodes `_build` instead of using the actual output path.

## What Changes
- Filter watcher events to ignore the output directory (resolves the infinite loop)
- Add debouncing so rapid filesystem events are coalesced into a single regeneration
- Filter events to only trigger on content-relevant file types (`.md`, `.yaml`, `.html`, `.css`, `.js`, images)
- Replace the hardcoded `_build` skip in `copy_static_directories` with the actual output directory name
- Properly stop the watchdog observer on shutdown

## Impact
- Affected specs: `dev-server` (new), `site-generation` (new)
- Affected code: `slartibartfast/server.py`, `slartibartfast/generator.py`
- No breaking changes to CLI interface - same commands, same flags

## ADDED Requirements

### Requirement: Output Directory Filtering

The file watcher SHALL ignore filesystem events originating from the output directory to prevent infinite regeneration loops.

#### Scenario: Generated file does not trigger rebuild
- **WHEN** the site generator writes a file to the output directory
- **THEN** the file watcher SHALL NOT trigger a site regeneration

#### Scenario: Source file change triggers rebuild
- **WHEN** a source file (markdown, template, config) is modified outside the output directory
- **THEN** the file watcher SHALL trigger a site regeneration

### Requirement: Event Debouncing

The file watcher SHALL debounce rapid filesystem events to coalesce multiple near-simultaneous changes into a single rebuild.

#### Scenario: Multiple rapid file changes
- **WHEN** multiple source files are modified within a short time window (e.g., 0.5 seconds)
- **THEN** the file watcher SHALL trigger only one site regeneration after the debounce period

### Requirement: Dynamic Output Directory Exclusion

The static directory copier SHALL exclude the actual configured output directory, not a hardcoded `_build` string.

#### Scenario: Non-default output directory
- **WHEN** `copy_static_directories()` runs with output directory set to `dist`
- **THEN** the `dist` directory SHALL be skipped during static directory copying
- **AND** directories other than `dist` that lack `_config.yaml` SHALL still be copied

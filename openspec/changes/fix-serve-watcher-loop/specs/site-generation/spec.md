## ADDED Requirements

### Requirement: Dynamic Output Directory Exclusion
The `copy_static_directories` function SHALL skip the actual output directory by name rather than hardcoding `_build`.

#### Scenario: Default output directory
- **WHEN** the output directory is the default `_build`
- **AND** `_build` exists inside the content directory
- **THEN** it SHALL be skipped during static directory copying

#### Scenario: Custom output directory
- **WHEN** the user specifies a custom output directory (e.g., `--output dist`)
- **AND** that directory exists inside the content directory
- **THEN** it SHALL be skipped during static directory copying

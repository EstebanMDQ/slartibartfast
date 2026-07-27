## ADDED Requirements

### Requirement: Watcher Output Directory Exclusion
The dev server's file watcher SHALL ignore filesystem events originating from inside the output directory.

#### Scenario: Output directory inside watched path
- **WHEN** the output directory is inside the content directory (e.g., `slarti serve .`)
- **AND** the generator writes files to the output directory
- **THEN** those writes SHALL NOT trigger a new regeneration

#### Scenario: Content file change still triggers regeneration
- **WHEN** a Markdown file inside the content directory is modified
- **AND** the file is not inside the output directory
- **THEN** the site SHALL be regenerated once

### Requirement: Watcher Debouncing
The dev server SHALL debounce rapid filesystem events so that multiple events within a short window result in a single site regeneration.

#### Scenario: Multiple rapid file changes
- **WHEN** multiple files are saved within a short interval (e.g., editor save producing multiple events)
- **THEN** only one regeneration SHALL occur after the events settle

### Requirement: Watcher File-Type Filtering
The dev server SHALL only trigger regeneration for changes to content-relevant files.

#### Scenario: Relevant file change
- **WHEN** a file with a content-relevant extension (`.md`, `.yaml`, `.yml`, `.html`, `.css`, `.js`, or image format) is modified
- **THEN** the site SHALL be regenerated

#### Scenario: Irrelevant file change
- **WHEN** a file with an irrelevant extension (e.g., `.pyc`, `.DS_Store`, `.swp`) is modified
- **THEN** no regeneration SHALL occur

#### Scenario: Hidden file change
- **WHEN** a file inside a hidden directory (path containing `/.`) is modified
- **THEN** no regeneration SHALL occur

### Requirement: Observer Graceful Shutdown
The dev server SHALL properly stop the watchdog observer when the server shuts down.

#### Scenario: Server interrupted with Ctrl-C
- **WHEN** the user presses Ctrl-C to stop the server
- **THEN** the observer SHALL be stopped and joined before the process exits

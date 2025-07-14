# CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2025-07-14

### Added

- **Configuration-Driven Menus**:
  - New `config_models.py` module with Pydantic models (`MenuConfig`, `MenuItemConfig`) to define a strict schema for menu configurations.
  - New `executors.py` module to handle the parsing and asynchronous execution of string-based actions (e.g., `"command::ls -l"`). This module safely runs subprocesses without blocking the UI's event loop.
  - The `loaders.py` module was updated with `create_menu_from_config` to dynamically build menu classes from these validated configuration models.
- **New Dependency**: Added `PyYAML` to support future loading from `.yml` files.
- **New Test Module**: Added `tests/test_config_actions.py` to verify the new external action execution system.

## [0.5.0] - 2025-07-14

### Added

- **Dynamic Menu Loading**:
  - New `loaders.py` module with `create_menu_from_dict` function to dynamically build `TyperdanticMenu` classes from Python dictionaries.

### Fixed

- **Menu Title Display**: Cleaned up menu title rendering to be a single, clean line.

## [0.4.0] - 2025-07-13

### Changed

- **Major Architectural Refactor**: Implemented a single, long-running application instance for seamless, flash-free menu navigation.

### Fixed

- **Application Hang**: Replaced blocking `input()` with an asynchronous `PromptSession`.
- **Pydantic and Import Errors**: Resolved circular dependency issues.

## [0.2.0] - 2025-07-13

### Added

- **Custom Styling System**: Added `styles.py` module and support for loading themes from TOML files.

## [0.1.0] - 2025-07-12

### Added

- Initial project structure, core models, and base classes.

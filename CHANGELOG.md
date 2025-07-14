# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2025-07-13

### Changed

- **Major Architectural Refactor for Seamless Navigation**:
  - The `TyperdanticApp` now manages a single, long-running `prompt-toolkit` application instance. This provides a smooth, flash-free experience when navigating between menus.
  - The `TyperdanticMenu` class has been simplified into a pure data and state container, with all rendering and key-handling logic now managed by the `TyperdanticApp`.
  - The complex and buggy `KeyBindingProxy` was removed in favor of a centralized key-handling system in `TyperdanticApp`.

### Fixed

- **Fixed Application Hang**: Replaced the blocking `input()` call with an asynchronous `PromptSession().prompt_async()` after an action is executed. This resolves the critical bug where the application would freeze.
- **Fixed Pydantic Validation Errors**: The new architecture resolves the circular dependency between `TyperdanticApp` and `TyperdanticMenu`, eliminating the `ValidationError` and `PydanticUserError` on startup.
- **Fixed `ImportError`**: Corrected the import for async prompting to use `PromptSession`, which is more robust across different `prompt-toolkit` versions.

## [0.2.0] - 2025-07-13

### Added

- **Custom Styling System**:
  - New `styles.py` module with `DEFAULT_STYLE` and `load_style_from_file` function.
  - `TyperdanticApp` and `TyperdanticMenu` now accept a `style` argument to theme the UI.
- **New Test Module**: Added `tests/test_styles.py`.

### Changed

- **Decoupled Actions**: `TyperdanticMenu.run()` now returns the `MenuItem` instead of executing the action internally.

## [0.1.0] - 2025-07-12

### Added

- Initial project structure, core models (`MenuItem`), base classes (`TyperdanticMenu`, `TyperdanticApp`), and documentation.


# All notable changes to this project will be documented in this file

## [0.1.1] - 2025-07-13

### Added

- **Custom Styling System**:
  - New `styles.py` module with `DEFAULT_STYLE` and `load_style_from_file` function.
  - `TyperdanticApp` and `TyperdanticMenu` now accept a `style` argument to theme the UI.
  - Style definitions can be loaded from a TOML file.
- **New Test Module**: Added `tests/test_styles.py` to verify style loading and fallback functionality.

### Changed

- **Decoupled Actions**: `TyperdanticMenu.run()` now returns the selected `MenuItem` instead of executing the action internally. This resolves context manager errors in certain terminals.
- The `TyperdanticApp` is now responsible for handling the returned `MenuItem` to execute actions or navigate.
- Refactored `tests/test_app.py` to align with the new action handling logic.

## [0.1.0] - 2025-07-12

### Added

- **Initial Project Structure**: Created the basic library file structure with `pyproject.toml`.
- **Core Models (`models.py`)**:
  - `MenuItem`: A Pydantic model to represent a single, selectable option in a menu.
- **Base Menu Logic (`base.py`)**:
  - `TyperdanticMenu`: The core base class for creating interactive menus.
- **App Controller (`app.py`)**:
  - `TyperdanticApp`: A top-level class to manage navigation between multiple menus.
- **Initial `README.md` and `CHANGELOG.md`**.

# **Changelog**

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

## **[1.1.0] - 2025-07-20**

### **Added**

* **Runtime Argument Prompting**: Actions defined in config files can now prompt the user for arguments when selected.
* **Structured Action Configuration**: Introduced ActionConfig and ArgumentSpec Pydantic models for more robust and readable action definitions in TOML files.
* **Action Context**: Registered internal:: actions now receive a context dictionary containing the TyperdanticApp instance and the active menu.
* **Expanded Script Support**: The script:: action executor now explicitly handles .sh, .bash, .bat, .cmd, and .js files.

### **Changed**

* The execute\_action\_string function now accepts context and args parameters.
* MenuItem model now includes args and prompt\_args fields to support advanced action configurations.
* TyperdanticApp.handle\_selection was refactored to support suspending the application to prompt for user input.

## **[1.0.2] - 2025-07-19**

### **Fixed**

* Corrected uv build command in the release.ps1 script.
* Addressed dependency resolution warnings when installing in a global environment by recommending virtual environments.

---

## **[1.0.0] - 2025-07-19**

### **Added**

* Initial release of typerdantic.
* Core functionality for creating declarative menus with TyperdanticMenu.
* TyperdanticApp for running and managing menus.
* Support for synchronous and asynchronous actions.
* Dynamic menu generation by overriding get\_items.
* Configuration-driven menus using create\_menu\_from\_config.
* Action registry for internal:: actions.
* Customizable styling via TOML files.
* Comprehensive documentation and examples.
* Test suite for core features.
* CI/CD pipeline for publishing to PyPI.

### **Changed**

* Refactored codebase for clarity and maintainability.
* Improved error handling and user feedback.

### **Fixed**

* Resolved ImportError issues in the test suite.
* Fixed PydanticUserError related to forward references in dynamically created models.

---

## [0.6.0] - 2025-07-14

### Added

* **Configuration-Driven Menus**:
  * New `config_models.py` module with Pydantic models (`MenuConfig`, `MenuItemConfig`) to define a strict schema for menu configurations.
  * New `executors.py` module to handle the parsing and asynchronous execution of string-based actions (e.g., `"command::ls -l"`). This module safely runs subprocesses without blocking the UI's event loop.
  * The `loaders.py` module was updated with `create_menu_from_config` to dynamically build menu classes from these validated configuration models.
* **New Dependency**: Added `PyYAML` to support future loading from `.yml` files.
* **New Test Module**: Added `tests/test_config_actions.py` to verify the new external action execution system.

---

## [0.5.0] - 2025-07-14

### Added

* **Dynamic Menu Loading**:
  * New `loaders.py` module with `create_menu_from_dict` function to dynamically build `TyperdanticMenu` classes from Python dictionaries.

### Fixed

* **Menu Title Display**: Cleaned up menu title rendering to be a single, clean line.

---

## [0.4.0] - 2025-07-13

### Changed

* **Major Architectural Refactor**: Implemented a single, long-running application instance for seamless, flash-free menu navigation.

### Fixed

* **Application Hang**: Replaced blocking `input()` with an asynchronous `PromptSession`.
* **Pydantic and Import Errors**: Resolved circular dependency issues.

---

## [0.2.0] - 2025-07-13

### Added

* **Custom Styling System**: Added `styles.py` module and support for loading themes from TOML files.

---

## [0.1.0] - 2025-07-12

### Added

* Initial project structure, core models, and base classes.

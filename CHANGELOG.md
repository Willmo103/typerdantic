# **Changelog**

All notable changes to this project will be documented in this file.

## **\[0.1.0\] \- 2025-07-12**

### **Added**

* **Initial Project Structure**: Created the basic library file structure with pyproject.toml.
* **Core Models (models.py)**:
  * MenuItem: A Pydantic model to represent a single, selectable option in a menu. Includes fields for description, action, and is\_quit.
* **Base Menu Logic (base.py)**:
  * TyperdanticMenu: The core base class for creating interactive menus.
  * Implemented async rendering loop.
  * Implemented keyboard navigation (Up/Down arrows, Enter).
  * Handles dynamic menu item discovery from Pydantic model fields.
* **Initial README.md and CHANGELOG.md**:
  * Added project description, core philosophy, and example usage.

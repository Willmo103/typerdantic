# 🗿 Typerdantic

**Typerdantic** is a Python library for building powerful, interactive, and self-documenting command-line interface (CLI) menus. It combines the command-line elegance of [**Typer**](https://typer.tiangolo.com/), the robust data modeling of [**Pydantic**](https://docs.pydantic.dev/), and the rich terminal UI capabilities of [**prompt-toolkit**](https://python-prompt-toolkit.readthedocs.io/).

The goal is to abstract away the boilerplate of creating interactive menus, allowing developers to define complex, multi-screen applications using simple Pydantic models.

---

## Core Features

- **Declarative Menus**: Define your CLI menus, options, and actions using Pydantic models. The structure of your data model *is* the structure of your menu.
- **Seamless Navigation**: A top-level `TyperdanticApp` controller manages a single, persistent UI, eliminating screen flashes when navigating between menus.
- **Custom Styling**: Theme your entire application by loading a simple TOML style file.
- **Self-Documenting**: Pydantic `Field` descriptions are automatically used as help text within the interactive UI.
- **Asynchronous by Design**: Built with `asyncio` to handle user input and actions without blocking.

---

## Example Usage

Define your menus as classes inheriting from `TyperdanticMenu`.

```python
# menus.py
from typerdantic import TyperdanticMenu, MenuItem
from pydantic import Field

class SettingsMenu(TyperdanticMenu):
    """Configure application settings."""
    change_item: MenuItem = Field(default=MenuItem(description="Change a setting"))
    back: MenuItem = Field(default=MenuItem(description="Back to Main Menu", is_quit=True))

class MainMenu(TyperdanticMenu):
    """This is the main menu."""
    settings: MenuItem = Field(
        default=MenuItem(description="Go to Settings", target_menu="settings")
    )
    exit_app: MenuItem = Field(default=MenuItem(description="Exit", is_quit=True))
```

Then, create and run an application instance.

```python
# main.py
import asyncio
from pathlib import Path
from typerdantic.app import TyperdanticApp
from typerdantic.styles import load_style_from_file
from menus import MainMenu, SettingsMenu

async def main():
    # Load an optional custom style file
    style = load_style_from_file(Path("styles.toml"))

    # Create the app with a main menu and custom style
    app = TyperdanticApp(main_menu=MainMenu, style=style)

    # Register other menus
    app.register_menu("settings", SettingsMenu)

    # Run the application
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Future Goals

- **CLI Menu Builder**: An interactive command to help scaffold new `Typerdantic` menus and actions.
- **More Widgets**: Support for more complex inputs like forms, confirmation dialogs, and progress bars.
- **Plugin System**: Allow for custom actions and menu item types to be added easily.

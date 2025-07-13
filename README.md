# **🗿 Typerdantic**

**Typerdantic** is a Python library for building powerful, interactive, and self-documenting command-line interface (CLI) menus. It combines the command-line elegance of [**Typer**](https://typer.tiangolo.com/), the robust data modeling of [**Pydantic**](https://www.google.com/search?q=https://docs.pydantic.dev/), and the rich terminal UI capabilities of [**prompt-toolkit**](https://python-prompt-toolkit.readthedocs.io/).

The goal is to abstract away the boilerplate of creating interactive menus, allowing developers to define menu structures using simple Pydantic models and then run them with a single command.

## **Core Philosophy**

* **Declarative Menus**: Define your CLI menus, options, and actions using Pydantic models. The structure of your data model *is* the structure of your menu.
* **Self-Documenting**: Pydantic Field descriptions are automatically used as help text within the interactive UI.
* **Reusable & Extensible**: A base class provides the core logic for handling keyboard navigation (arrow keys, Enter, quit), while allowing for easy extension with custom actions and logic.
* **Asynchronous by Design**: Built with asyncio to handle user input and actions without blocking.

## **Example Usage (Planned)**

The goal is to enable a developer to write something as simple as this:

```python
from typerdantic import TyperdanticMenu, MenuItem
from pydantic import Field
import asyncio

class MainMenu(TyperdanticMenu):
    """The main menu for our awesome application."""

    explore\_files: MenuItem \= Field(
        description="Dive into the file explorer.",
        action="explore\_app.run"  \# Points to a function to call
    )
    manage\_settings: MenuItem \= Field(
        description="Configure application settings.",
        action="settings\_app.show\_menu"
    )
    quit\_app: MenuItem \= Field(
        description="Exit the application.",
        is\_quit=True
    )

async def main():
    menu \= MainMenu()
    await menu.run()

if __name__ == "__main__":
    asyncio.run(main())

```

## **Project Status**

**Alpha**. This project is currently in the initial design and development phase. The core API is subject to change.

## **Contribution**

Contributions are welcome\! Feel free to open an issue or submit a pull request.

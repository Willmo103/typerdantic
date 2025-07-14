# 🗿 Typerdantic

**Typerdantic** is a Python library for building powerful, interactive, and self-documenting command-line interface (CLI) menus. It combines the command-line elegance of [**Typer**](https://typer.tiangolo.com/), the robust data modeling of [**Pydantic**](https://docs.pydantic.dev/), and the rich terminal UI capabilities of [**prompt-toolkit**](https://python-prompt-toolkit.readthedocs.io/).

The goal is to abstract away the boilerplate of creating interactive menus, allowing developers to define complex, multi-screen applications using simple Pydantic models or configuration files.

---

## Core Features

- **Declarative & Dynamic Menus**: Define menus by subclassing `TyperdanticMenu` or generate them on the fly from configuration files (e.g., YAML, JSON) using a Pydantic-validated schema.
- **External Action Execution**: Run shell commands and scripts directly from your menu configuration using action strings like `"command::echo Hello"` or `"script::./deploy.sh"`.
- **Seamless Navigation**: A top-level `TyperdanticApp` controller manages a single, persistent UI, eliminating screen flashes when navigating between menus.
- **Custom Styling**: Theme your entire application by loading a simple TOML style file.
- **Asynchronous by Design**: Built with `asyncio` to handle user input and execute subprocesses without blocking or freezing the UI.

---

## Example Usage

Define your menu in a configuration file, like `menu.yml`:

```yaml
# file: menu.yml
doc: My Awesome CLI
items:
  list_files:
    description: List files in the current directory
    action: "command::ls -l"

  run_backup:
    description: Run the backup script
    action: "script::./scripts/backup.sh"

  quit:
    description: Exit the application
    is_quit: true
```

Then, load and run your application:

```python
# main.py
import asyncio
import yaml
from pathlib import Path
from typerdantic import TyperdanticApp, create_menu_from_config
from typerdantic.config_models import MenuConfig

async def main():
    # Load and parse the YAML configuration
    config_path = Path("menu.yml")
    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)

    menu_config = MenuConfig(**config_dict)

    # Create a menu class from the validated config
    MyMenu = create_menu_from_config("MyMenu", menu_config)

    # Create and run the app
    app = TyperdanticApp(main_menu=MyMenu)
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Future Goals

- **YAML/JSON Loaders**: Add convenience functions like `load_menu_from_yaml()` to simplify the loading process.
- **Internal Action Registry**: Create a system for registering and calling internal Python functions via action strings (e.g., `"internal::backup_database"`).
- **CLI Menu Builder**: An interactive command to help scaffold new `Typerdantic` apps, menus, and actions.
- **More Widgets**: Support for forms, confirmation dialogs, and progress bars.

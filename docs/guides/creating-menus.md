# Creating Menus: From Static to Dynamic

In the "Getting Started" guide, you learned how to create a basic, static menu. Now, let's explore how to build more complex interfaces by nesting menus and creating dynamic menus whose contents change based on your application's state.

---

## 1. Nested Menus for Navigation

Most real-world applications require more than one menu. Typerdantic makes it easy to navigate between different menus. The key is the `target_menu` property on a `MenuItem` and the `app.register_menu()` method.

Let's expand our first application with a separate "Settings" menu.

### Example: Main Menu with a Settings Sub-Menu

```python
# file: nested_app.py

import asyncio
from pydantic import Field
from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem

# --- Action for the settings menu ---
def change_setting():
    print("\nA setting was changed!")

# --- Menu Definitions ---

class SettingsMenu(TyperdanticMenu):
    """Application Settings"""
    change_item: MenuItem = Field(
        default=MenuItem(description="Change a setting", action=change_setting)
    )
    # is_quit=True in a sub-menu acts as a "back" button.
    back: MenuItem = Field(
        default=MenuItem(description="Back to Main Menu", is_quit=True)
    )

class MainMenu(TyperdanticMenu):
    """Main Application Menu"""
    # This item doesn't have an action. Instead, it has a target_menu.
    # The string 'settings' must match the name we register below.
    settings_item: MenuItem = Field(
        default=MenuItem(
            description="Go to Settings",
            target_menu="settings"
        )
    )
    quit_item: MenuItem = Field(
        default=MenuItem(description="Exit", is_quit=True)
    )

# --- Application Setup ---

if __name__ == "__main__":
    # 1. Create the app with the main menu.
    app = TyperdanticApp(main_menu=MainMenu)

    # 2. Register the other menus with a unique string name.
    app.register_menu("settings", SettingsMenu)

    # 3. Run the application.
    try:
        asyncio.run(app.run())
    except (KeyboardInterrupt, EOFError):
        print("\nApplication interrupted by user.")
````

When you run this (`python nested_app.py`), selecting "Go to Settings" will close the `MainMenu` and open the `SettingsMenu`. Selecting "Back to Main Menu" (or pressing `q`) in the `SettingsMenu` will take you back to the `MainMenu`.

---

## 2\. Dynamic Menus

Static menus defined by class fields are great, but what if your menu's content depends on the file system, a database, or a web API? For this, you need a **dynamic menu**.

To create a dynamic menu, you override the `get_items()` method in your `TyperdanticMenu` subclass.

### How it Works

- You create a class that inherits from `TyperdanticMenu`.
- Instead of defining `MenuItem`s as class fields, you implement the `get_items()` method.
- This method must return a `List` of `Tuples`, where each tuple contains a unique name (`str`) and a `MenuItem` instance.
- The menu class can hold its own state (e.g., the current directory), and the `get_items()` method can use this state to generate the items.

### Example: A Simple File Explorer

Here’s a practical example of a dynamic menu that lists the contents of the current directory. This example comes directly from the `examples/` folder.

```python
# file: examples/file_explorer.py
import os
from pathlib import Path
from typing import List, Tuple
import asyncio

from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem

class FileExplorerMenu(TyperdanticMenu):
    """File Explorer"""

    # This menu holds its own state!
    current_path: Path = Path(".").resolve()

    def go_up(self):
        """Action to navigate to the parent directory."""
        self.current_path = self.current_path.parent
        # No return value needed; the app will refresh the menu
        # after an action is run.

    # This is the core of a dynamic menu.
    def get_items(self) -> List[Tuple[str, MenuItem]]:
        """Dynamically generate menu items based on the file system."""
        items: List[Tuple[str, MenuItem]] = []

        # Manually add a navigation action.
        # The action is a method on this class instance itself.
        if self.current_path.parent != self.current_path:
            items.append(
                ("go_up", MenuItem(description="[.. Go Up]", action=self.go_up))
            )

        # Scan the directory and create an item for each entry.
        try:
            # Sort entries to show directories first.
            entries = sorted(
                os.scandir(self.current_path),
                key=lambda e: (not e.is_dir(), e.name.lower())
            )
            for entry in entries:
                prefix = "[D]" if entry.is_dir() else "[F]"
                item_desc = f"{prefix} {entry.name}"
                # Here, the action is to change the directory if it's a dir,
                # or just print its name if it's a file.
                action = (
                    lambda p=entry.path: self.set_path(p)
                    if os.path.isdir(p) else
                    lambda: print(f"Selected file: {entry.name}")
                )

                items.append(
                    (entry.name, MenuItem(description=item_desc, action=action))
                )
        except OSError as e:
            items.append(
                ("error", MenuItem(description=f"Error reading directory: {e}"))
            )

        # Always add a quit option.
        items.append(("quit", MenuItem(description="[Exit Explorer]", is_quit=True)))

        return items

    def set_path(self, new_path: str):
        """Action to change the current directory."""
        self.current_path = Path(new_path).resolve()


if __name__ == "__main__":
    app = TyperdanticApp(main_menu=FileExplorerMenu)
    try:
        asyncio.run(app.run())
    except (KeyboardInterrupt, EOFError):
        print("\nExited file explorer.")

```

Run this file (`python examples/file_explorer.py`), and you'll have a basic, interactive file explorer\! Each time you select a directory or "Go Up," the `action` runs, changes the `current_path` state, and Typerdantic automatically calls `get_items()` again to rerender the menu with the new content.

---

## Next Steps

You now know how to create static, nested, and dynamic menus. The next step is to learn more about the different kinds of actions you can perform.

➡️ **Next up: [Using Actions](using-actions.md)**

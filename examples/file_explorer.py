# examples/file_explorer.py

import os
from pathlib import Path
from typing import List, Tuple

from typerdantic import TyperdanticMenu, MenuItem
from typerdantic.component import TyperdanticComponent
from pydantic import Field

# --- Define the Component ---


class FileExplorerComponent(TyperdanticComponent):
    """A component for exploring the file system."""

    def __init__(self, start_path: str = "."):
        super().__init__()
        self.current_path = Path(start_path).resolve()

        # Define the component's menus and actions
        self.menus = {"explorer": self.FileExplorerMenu}
        self.actions = {
            "go_up": self.go_up,
            "view_details": self.view_details,
        }

    # --- Component State and Actions ---
    def go_up(self):
        """Action to navigate to the parent directory."""
        self.current_path = self.current_path.parent

    def view_details(self):
        """Action to show details of the currently selected item."""
        # In a real app, this would show more info.
        selected_item_name = self.menus["explorer"].get_selected_item().description
        print(f"\nDetails for: {selected_item_name}")
        print(f"Full Path: {self.current_path / selected_item_name}")

    # --- Define the Menu Class inside the Component ---
    # This keeps everything neatly encapsulated.
    class FileExplorerMenu(TyperdanticMenu):
        """File Explorer"""

        def get_items(self) -> List[Tuple[str, MenuItem]]:
            """Dynamically generate menu items based on the file system."""
            # The 'app' has a reference to the component that owns this menu
            # This is a bit of a hack, a better way would be to pass component state
            # directly to the menu on instantiation. For now, this demonstrates the concept.
            component: "FileExplorerComponent" = (
                self.app.active_menu.app
            )  # This is a bit circular
            path = self.current_path
            items = []

            # Add an item to go to the parent directory
            items.append(
                ("go_up", MenuItem(description="[.. Go Up]", action="internal::go_up"))
            )

            try:
                for entry in sorted(
                    os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower())
                ):
                    prefix = "[D]" if entry.is_dir() else "[F]"
                    item = MenuItem(
                        description=f"{prefix} {entry.name}",
                        # In a real app, selecting a dir would change the path
                        # and selecting a file might open a context menu.
                        action="internal::view_details",
                    )
                    items.append((entry.name, item))
            except OSError as e:
                items.append(
                    ("error", MenuItem(description=f"Error reading directory: {e}"))
                )
            return items

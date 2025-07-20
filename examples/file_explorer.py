# examples/file_explorer.py

import os
from pathlib import Path
from typing import List, Tuple

from typerdantic import TyperdanticMenu, MenuItem


class FileExplorerMenu(TyperdanticMenu):
    """File Explorer"""

    # The menu now holds its own state
    current_path: Path = Path(".").resolve()

    def go_up(self):
        """Action to navigate to the parent directory."""
        self.current_path = self.current_path.parent

    def view_details(self):
        """Action to show details of the currently selected item."""
        selected_item = self.get_selected_item()
        if not selected_item:
            return

        item_name = selected_item.description.split(" ", 1)[-1]
        print(f"\nDetails for: {item_name}")
        print(f"Full Path: {self.current_path / item_name}")

    def get_items(self) -> List[Tuple[str, MenuItem]]:
        """Dynamically generate menu items based on the file system."""
        items = []

        # Actions now refer to methods on this class instance
        items.append(("go_up", MenuItem(description="[.. Go Up]", action=self.go_up)))

        try:
            # Sort with directories first
            entries = sorted(os.scandir(self.current_path), key=lambda e: (not e.is_dir(), e.name.lower()))
            for entry in entries:
                prefix = "[D]" if entry.is_dir() else "[F]"
                item = MenuItem(
                    description=f"{prefix} {entry.name}",
                    action=self.view_details
                )
                items.append((entry.name, item))
        except OSError as e:
            items.append(("error", MenuItem(description=f"Error reading directory: {e}")))

        return items

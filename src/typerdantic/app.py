# src/typerdantic/app.py

import asyncio
from typing import Dict, Type
from .base import TyperdanticMenu


class TyperdanticApp:
    """
    A top-level application controller that manages and navigates between
    multiple TyperdanticMenu instances.
    """

    def __init__(self, main_menu: Type[TyperdanticMenu]):
        self.menu_registry: Dict[str, Type[TyperdanticMenu]] = {"main": main_menu}
        self.nav_stack: list[str] = ["main"]

    def register_menu(self, name: str, menu_class: Type[TyperdanticMenu]):
        """Registers a new menu class with a unique name."""
        if name in self.menu_registry:
            raise ValueError(f"Menu with name '{name}' is already registered.")
        self.menu_registry[name] = menu_class

    async def run(self):
        """Starts the application and manages the menu navigation loop."""
        while self.nav_stack:
            current_menu_name = self.nav_stack[-1]
            menu_class = self.menu_registry.get(current_menu_name)

            if not menu_class:
                print(f"Error: Menu '{current_menu_name}' not found.")
                self.nav_stack.pop()
                continue

            menu_instance = menu_class()
            selected_item = await menu_instance.run()

            if not selected_item:  # User quit the current menu (q, Ctrl+C)
                self.nav_stack.pop()
                continue

            if selected_item.is_quit:  # A "back" or "exit" action
                self.nav_stack.pop()
                continue

            if selected_item.target_menu:
                self.nav_stack.append(selected_item.target_menu)

            if selected_item.action:
                if asyncio.iscoroutinefunction(selected_item.action):
                    await selected_item.action()
                else:
                    selected_item.action()
                # For actions that don't navigate, pause before re-displaying menu
                if not selected_item.target_menu:
                    input("\nPress Enter to continue...")

# src/typerdantic/app.py

import asyncio
from typing import Dict, Type, Optional

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
# Corrected import: Use PromptSession for robust async prompting
from prompt_toolkit.shortcuts import PromptSession

from .base import TyperdanticMenu
from .models import MenuItem
from .styles import DEFAULT_STYLE


class TyperdanticApp:
    """
    A top-level application controller that manages and navigates between
    multiple TyperdanticMenu instances within a single, persistent UI.
    """

    def __init__(self, main_menu: Type[TyperdanticMenu], style: Optional[Style] = None):
        self.menu_registry: Dict[str, Type[TyperdanticMenu]] = {"main": main_menu}
        self.style = style or DEFAULT_STYLE

        self.nav_stack: list[TyperdanticMenu] = [main_menu()]
        self.active_menu: TyperdanticMenu = self.nav_stack[0]

        self.layout = Layout(Window(FormattedTextControl(self._get_current_fragments, focusable=True)))
        self.key_bindings = self._build_keybindings()
        self.application: Application = Application(
            layout=self.layout,
            key_bindings=self.key_bindings,
            full_screen=True,
            style=self.style,
        )

    def _build_keybindings(self) -> KeyBindings:
        """Builds the keybindings for the entire application."""
        kb = KeyBindings()

        @kb.add("up")
        def _(event):
            self.active_menu.go_up()

        @kb.add("down")
        def _(event):
            self.active_menu.go_down()

        @kb.add("enter")
        async def _(event):
            selected_item = self.active_menu.get_selected_item()
            if selected_item:
                await self.handle_selection(selected_item)

        @kb.add("c-c", "q")
        def _(event):
            self.go_back()

        return kb

    def _get_current_fragments(self):
        """Proxy method to get fragments from the currently active menu."""
        return self.active_menu.get_display_fragments()

    def register_menu(self, name: str, menu_class: Type[TyperdanticMenu]):
        """Registers a new menu class with a unique name."""
        if name in self.menu_registry:
            raise ValueError(f"Menu with name '{name}' is already registered.")
        self.menu_registry[name] = menu_class

    def navigate_to(self, menu_name: str):
        """Navigates to a new menu, adding it to the stack."""
        menu_class = self.menu_registry.get(menu_name)
        if menu_class:
            new_menu = menu_class()
            self.nav_stack.append(new_menu)
            self.active_menu = new_menu
            self.application.invalidate()

    def go_back(self):
        """Goes back one level in the navigation stack, or quits if at the root."""
        if len(self.nav_stack) > 1:
            self.nav_stack.pop()
            self.active_menu = self.nav_stack[-1]
            self.application.invalidate()
        else:
            self.application.exit()

    async def handle_selection(self, item: MenuItem):
        """Handles the logic for a selected menu item."""
        if item.is_quit:
            self.go_back()
            return

        action_was_run = False
        if item.action:
            action_was_run = True
            suspender = self.application.suspend_to_background()
            if suspender:
                with suspender:
                    if asyncio.iscoroutinefunction(item.action):
                        await item.action()
                    else:
                        item.action()
                    # Create a session to use the async prompt
                    session: PromptSession = PromptSession()
                    await session.prompt_async("\nPress Enter to continue...")
            else:  # Fallback for unsupported terminals
                self.application.renderer.clear()
                if asyncio.iscoroutinefunction(item.action):
                    await item.action()
                else:
                    item.action()
                session = PromptSession()
                await session.prompt_async("\nPress Enter to continue...")

        if item.target_menu:
            self.navigate_to(item.target_menu)
        elif action_was_run:
            self.application.invalidate()

    async def run(self):
        """Starts the application's main event loop."""
        await self.application.run_async()

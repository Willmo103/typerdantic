# src/typerdantic/app.py

import asyncio
from typing import Dict, Type, Optional

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import PromptSession

from .base import TyperdanticMenu
from .models import MenuItem
from .styles import DEFAULT_STYLE
from .executors import execute_action_string


class TyperdanticApp:
    """
    A top-level application controller that manages and navigates between menus.
    """

    def __init__(self, main_menu: Type[TyperdanticMenu], style: Optional[Style] = None):
        self.menu_registry: Dict[str, Type[TyperdanticMenu]] = {"main": main_menu}
        self.style = style or DEFAULT_STYLE

        self.nav_stack: list[TyperdanticMenu] = [main_menu(app=self)]
        self.active_menu: TyperdanticMenu = self.nav_stack[0]

        self.layout = Layout(
            Window(FormattedTextControl(self._get_current_fragments, focusable=True))
        )
        self.key_bindings = self._build_keybindings()
        self.application: Application = Application(
            layout=self.layout,
            key_bindings=self.key_bindings,
            full_screen=True,
            style=self.style,
        )

    def register_menu(self, name: str, menu_class: Type[TyperdanticMenu]):
        if name in self.menu_registry:
            raise ValueError(f"Menu '{name}' is already registered.")
        self.menu_registry[name] = menu_class

    def _build_keybindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("up")
        def _(event):
            self.active_menu.go_up()

        @kb.add("down")
        def _(event):
            self.active_menu.go_down()

        @kb.add("enter")
        async def _(event):
            item = self.active_menu.get_selected_item()
            if item:
                await self.handle_selection(item)

        @kb.add("c-c", "q")
        def _(event):
            self.go_back()

        return kb

    def _get_current_fragments(self):
        return self.active_menu.get_display_fragments()

    def navigate_to(self, menu_name: str):
        menu_class = self.menu_registry.get(menu_name)
        if menu_class:
            new_menu = menu_class(app=self)
            self.nav_stack.append(new_menu)
            self.active_menu = new_menu
            self.application.invalidate()

    def go_back(self):
        if len(self.nav_stack) > 1:
            self.nav_stack.pop()
            self.active_menu = self.nav_stack[-1]
            self.application.invalidate()
        else:
            self.application.exit()

    async def handle_selection(self, item: MenuItem):
        if item.is_quit:
            self.go_back()
            return

        action_was_run = False
        if item.action:
            action_was_run = True

            # Construct the context dictionary to pass to actions.
            context = {"app": self, "menu": self.active_menu}

            # The action can be a callable function or a string to be executed.
            # The functools.partial in the loader has already pre-filled the
            # action_string and args for config-driven menus.
            if callable(item.action):
                # For direct callable actions (non-config), we still need to pass args.
                if asyncio.iscoroutinefunction(item.action):
                    await item.action(context=context, args=item.args)
                else:
                    item.action(context=context, args=item.args)

            # After an action, we might need to refresh the menu view
            self.active_menu.refresh_items()
            session: PromptSession = PromptSession()
            await session.prompt_async("\nPress Enter to continue...")

        if item.target_menu:
            self.navigate_to(item.target_menu)
        elif action_was_run:
            self.application.invalidate()

    async def run(self):
        await self.application.run_async()

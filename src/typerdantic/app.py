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

            # Combine pre-defined args with runtime-prompted args
            final_args = item.args.copy() if item.args else {}

            # --- NEW: Prompt for runtime arguments ---
            if item.prompt_args:
                # Temporarily exit the full-screen app to use the prompt
                self.application.suspend_to_background()
                try:
                    session: PromptSession = PromptSession()
                    for arg_spec in item.prompt_args:
                        user_input = await session.prompt_async(
                            f"{arg_spec.prompt}: ",
                            default=str(arg_spec.default or ""),
                        )
                        final_args[arg_spec.name] = user_input
                finally:
                    # Ensure we always resume the application
                    self.application.resume_from_background()

            context = {"app": self, "menu": self.active_menu}

            if callable(item.action):
                if asyncio.iscoroutinefunction(item.action):
                    await item.action(context=context, args=final_args)
                else:
                    item.action(context=context, args=final_args)

            self.active_menu.refresh_items()
            # No need for a separate "Press Enter" prompt, as the prompt session handles it
            if not item.prompt_args:
                session = PromptSession()
                await session.prompt_async("\nPress Enter to continue...")

        if item.target_menu:
            self.navigate_to(item.target_menu)
        elif action_was_run:
            self.application.invalidate()

    async def run(self):
        await self.application.run_async()

# src/typerdantic/base.py

import asyncio
from pydantic import BaseModel
from typing import List, Tuple

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style

from .models import MenuItem


class TyperdanticMenu(BaseModel):
    """
    A base class for creating interactive menus from Pydantic models.

    Subclass this and define your menu items using `MenuItem` fields.
    """

    # Internal state, excluded from Pydantic model
    _menu_items: List[Tuple[str, MenuItem]] = []
    _selected_index: int = 0
    _scroll_offset: int = 0
    _max_display_items: int = 10  # Max items to show at once.

    def __init__(self, **data):
        super().__init__(**data)
        self._menu_items = self._discover_menu_items()

    def _discover_menu_items(self) -> List[Tuple[str, MenuItem]]:
        """Finds all MenuItem fields defined on the subclass."""
        items = []
        # Use `self.model_fields` for Pydantic v2 compatibility.
        for name, field_info in self.model_fields.items():
            if isinstance(field_info.default, MenuItem):
                items.append((name, field_info.default))
        return items

    def _update_scroll(self):
        """Adjusts the scroll offset based on the selected index."""
        # Scroll down if selection is past the visible window
        if self._selected_index >= self._scroll_offset + self._max_display_items:
            self._scroll_offset = self._selected_index - self._max_display_items + 1
        # Scroll up if selection is before the visible window
        elif self._selected_index < self._scroll_offset:
            self._scroll_offset = self._selected_index

    def _get_display_fragments(self):
        """Generates the text to be displayed in the terminal, handling scrolling."""
        fragments = []
        title = self.__doc__ or "Select an option:"
        # Append a tuple directly, not a list containing a tuple
        fragments.append(("class:title", f"--- {title} ---\n"))

        # Slice the items to get only the visible ones
        start = self._scroll_offset
        end = self._scroll_offset + self._max_display_items
        visible_items = self._menu_items[start:end]

        for i, (name, item) in enumerate(visible_items, start=start):
            style = "class:selected" if i == self._selected_index else ""
            prefix = "> " if i == self._selected_index else "  "
            # Append a tuple directly
            fragments.append((style, f"{prefix}{item.description}\n"))

        # Add a scroll indicator if there are more items
        if len(self._menu_items) > self._max_display_items:
            # Append a tuple directly
            fragments.append(
                ("class:title", f"\n(Showing {len(visible_items)} of {len(self._menu_items)} items)"))

        return fragments

    async def run(self):
        """
        Renders the menu and handles user interaction asynchronously.
        """
        # --- Key Bindings ---
        kb = KeyBindings()

        @kb.add("up")
        def _(event):
            self._selected_index = (
                self._selected_index - 1 + len(self._menu_items)) % len(self._menu_items)
            self._update_scroll()

        @kb.add("down")
        def _(event):
            self._selected_index = (
                self._selected_index + 1) % len(self._menu_items)
            self._update_scroll()

        @kb.add("enter")
        async def _(event):
            if not self._menu_items:
                return
            name, selected_item = self._menu_items[self._selected_index]

            if selected_item.is_quit:
                event.app.exit()
                return

            if selected_item.action:
                # Suspend the UI to run the action and clear the screen
                with event.app.suspend_to_background():
                    if asyncio.iscoroutinefunction(selected_item.action):
                        await selected_item.action()
                    else:
                        selected_item.action()
                    # A small pause for the user to see the output of the action
                    input("\nPress Enter to return to the menu...")

        @kb.add("c-c", "q")
        def _(event):
            event.app.exit()

        # --- UI Layout ---
        layout = Layout(
            Window(FormattedTextControl(
                self._get_display_fragments, focusable=True)),
            focused_element=None
        )

        style = Style.from_dict({
            "title": "bold underline",
            "selected": "bg:#0055aa #ffffff bold",
        })

        app = Application(layout=layout, key_bindings=kb,
                          full_screen=True, style=style)

        await app.run_async()

    class Config:
        extra = 'allow'



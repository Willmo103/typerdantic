# src/typerdantic/base.py

from pydantic import BaseModel
from typing import List, Tuple, Optional

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
        for name, field_info in self.model_fields.items():
            if isinstance(field_info.default, MenuItem):
                items.append((name, field_info.default))
        return items

    def _update_scroll(self):
        """Adjusts the scroll offset based on the selected index."""
        if self._selected_index >= self._scroll_offset + self._max_display_items:
            self._scroll_offset = self._selected_index - self._max_display_items + 1
        elif self._selected_index < self._scroll_offset:
            self._scroll_offset = self._selected_index

    def _get_display_fragments(self):
        """Generates the text to be displayed in the terminal, handling scrolling."""
        fragments = [("class:title", f"--- {self.__doc__ or 'Select an option:'} ---\n")]
        start, end = self._scroll_offset, self._scroll_offset + self._max_display_items
        visible_items = self._menu_items[start:end]

        for i, (name, item) in enumerate(visible_items, start=start):
            style = "class:selected" if i == self._selected_index else ""
            prefix = "> " if i == self._selected_index else "  "
            fragments.append((style, f"{prefix}{item.description}\n"))

        if len(self._menu_items) > self._max_display_items:
            fragments.append(("class:title", f"\n(Showing {len(visible_items)} of {len(self._menu_items)} items)"))
        return fragments

    async def run(self) -> Optional[MenuItem]:
        """
        Renders the menu and handles user interaction.
        Returns the selected MenuItem or None if the user quits.
        """
        if not self._menu_items:
            return None

        kb = KeyBindings()

        @kb.add("up")
        def _(event):
            self._selected_index = (self._selected_index - 1 + len(self._menu_items)) % len(self._menu_items)
            self._update_scroll()

        @kb.add("down")
        def _(event):
            self._selected_index = (self._selected_index + 1) % len(self._menu_items)
            self._update_scroll()

        @kb.add("enter")
        async def _(event):
            """This handler is now async."""
            selected_item = self._menu_items[self._selected_index][1]
            event.app.exit(result=selected_item)

        @kb.add("c-c", "q")
        async def _(event):
            """This handler is now async."""
            event.app.exit(result=None)

        layout = Layout(Window(FormattedTextControl(self._get_display_fragments, focusable=True)))
        style = Style.from_dict({"title": "bold underline", "selected": "bg:#0055aa #ffffff bold"})
        app = Application(layout=layout, key_bindings=kb, full_screen=True, style=style)

        return await app.run_async()

    class Config:
        extra = 'allow'

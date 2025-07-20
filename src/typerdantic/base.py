# src/typerdantic/base.py
from __future__ import annotations
from pydantic import BaseModel
from typing import List, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .app import TyperdanticApp

from .models import MenuItem


class TyperdanticMenu(BaseModel):
    """
    A data container for a menu's content and state.
    """
    app: "TyperdanticApp"

    # Internal state
    _menu_items: List[Tuple[str, MenuItem]] = []
    _selected_index: int = 0
    _scroll_offset: int = 0
    _max_display_items: int = 10

    def __init__(self, **data):
        super().__init__(**data)
        self.refresh_items()

    def refresh_items(self):
        """Re-evaluates the menu items. Useful for dynamic menus."""
        self._menu_items = self.get_items()
        # Clamp selected index to be valid
        if self._selected_index >= len(self._menu_items) and self._menu_items:
            self._selected_index = len(self._menu_items) - 1
        elif not self._menu_items:
            self._selected_index = 0

    def get_items(self) -> List[Tuple[str, MenuItem]]:
        """
        Discovers menu items from class fields. Subclasses should override
        this method to provide items dynamically.
        """
        items = []
        for name, field_info in self.__class__.model_fields.items():
            if isinstance(field_info.default, MenuItem):
                items.append((name, field_info.default))
        return items

    def _update_scroll(self):
        if self._selected_index >= self._scroll_offset + self._max_display_items:
            self._scroll_offset = self._selected_index - self._max_display_items + 1
        elif self._selected_index < self._scroll_offset:
            self._scroll_offset = self._selected_index

    def get_display_fragments(self):
        title = self.__doc__ or "Select an option:"
        cleaned_title = title.strip().splitlines()[0]
        fragments = [("class:title", f"--- {cleaned_title} ---\n")]
        start, end = self._scroll_offset, self._scroll_offset + self._max_display_items
        visible_items = self._menu_items[start:end]
        for i, (name, item) in enumerate(visible_items, start=start):
            style = "class:selected" if i == self._selected_index else "class:menu-item"
            prefix = "> " if i == self._selected_index else "  "
            fragments.append((style, f"{prefix}{item.description}\n"))
        if len(self._menu_items) > self._max_display_items:
            fragments.append(("class:title", f"\n(Showing {len(visible_items)} of {len(self._menu_items)} items)"))
        return fragments

    def go_up(self):
        if not self._menu_items:
            return
        self._selected_index = (self._selected_index - 1 + len(self._menu_items)) % len(self._menu_items)
        self._update_scroll()

    def go_down(self):
        if not self._menu_items:
            return
        self._selected_index = (self._selected_index + 1) % len(self._menu_items)
        self._update_scroll()

    def get_selected_item(self) -> Optional[MenuItem]:
        if not self._menu_items:
            return None
        return self._menu_items[self._selected_index][1]

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

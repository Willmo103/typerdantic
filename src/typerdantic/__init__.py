# src/typerdantic/__init__.py

"""
Typerdantic: Declarative, interactive CLI menus.
"""

__version__ = "0.5.0"

from .models import MenuItem
from .base import TyperdanticMenu
from .app import TyperdanticApp
from .styles import load_style_from_file


__all__ = [
    "MenuItem",
    "TyperdanticMenu",
    "TyperdanticApp",
    "load_style_from_file",
    "create_menu_from_dict",
]

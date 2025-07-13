# src/typerdantic/__init__.py

"""
Typerdantic: Declarative, interactive CLI menus.
"""

__version__ = "0.1.0"

from .models import MenuItem
from .base import TyperdanticMenu

__all__ = ["MenuItem", "TyperdanticMenu"]

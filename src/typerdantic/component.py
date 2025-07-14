# src/typerdantic/component.py

from typing import Dict, Type, List, Callable, Any
from .base import TyperdanticMenu


class TyperdanticComponent:
    """
    A base class for creating self-contained, reusable application components.

    A component encapsulates its own menus and actions, which can then be
    registered with a top-level TyperdanticApp.
    """

    # Subclasses should define their menus and actions here.
    # The key is the name used for registration (e.g., "settings_menu").
    # The value is the TyperdanticMenu class itself.
    menus: Dict[str, Type[TyperdanticMenu]] = {}

    # The key is the name for the action (e.g., "my_action").
    # The value is the function to be executed.
    actions: Dict[str, Callable[..., Any]] = {}

    def __init__(self):
        # Components can have their own state
        pass

    def register_with_app(self, app):
        """
        Registers the component's menus and actions with the main app.

        Args:
            app: The TyperdanticApp instance.
        """
        for name, menu_class in self.menus.items():
            app.register_menu(name, menu_class)

        for name, action_func in self.actions.items():
            app.register_action(name, action_func)

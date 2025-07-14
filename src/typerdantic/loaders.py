# src/typerdantic/loaders.py

from typing import Dict, Any, Type
from pydantic import Field, create_model
import functools

from .base import TyperdanticMenu
from .models import MenuItem
from .config_models import MenuConfig
from .executors import execute_action_string


def create_menu_from_config(name: str, config: MenuConfig) -> Type[TyperdanticMenu]:
    """
    Dynamically creates a TyperdanticMenu subclass from a MenuConfig object
    using Pydantic's `create_model` utility.
    """
    field_definitions: Dict[str, Any] = {}

    for item_name, item_config in config.items.items():
        # Create a callable action. If the item has an action string,
        # create a partial function that calls our executor with that string.
        action_callable = None
        if item_config.action:
            action_callable = functools.partial(
                execute_action_string, item_config.action
            )

        # Create a MenuItem instance from the item's configuration
        menu_item = MenuItem(
            description=item_config.description,
            action=action_callable,
            target_menu=item_config.target_menu,
            is_quit=item_config.is_quit,
        )

        # The field definition for create_model is a tuple of (type, default_value).
        # The default value is a Pydantic Field instance.
        field_definitions[item_name] = (MenuItem, Field(default=menu_item))

    # Use pydantic.create_model to build the class correctly
    NewMenu = create_model(name, __base__=TyperdanticMenu, **field_definitions)

    # Set the docstring on the newly created class
    NewMenu.__doc__ = config.doc

    return NewMenu

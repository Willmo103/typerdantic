# src/typerdantic/loaders.py

from typing import Dict, Any, Type
from pydantic import Field, create_model
import functools

from .base import TyperdanticMenu
from .models import MenuItem
from .config_models import MenuConfig, ActionConfig
from .executors import execute_action_string


def create_menu_from_config(name: str, config: MenuConfig) -> Type[TyperdanticMenu]:
    """
    Dynamically creates a TyperdanticMenu subclass from a MenuConfig object.
    """
    field_definitions: Dict[str, Any] = {}

    for item_name, item_config in config.items.items():
        action_callable = None
        action_args = None
        prompt_args = None
        action_string = None

        if isinstance(item_config.action, str):
            action_string = item_config.action
        elif isinstance(item_config.action, ActionConfig):
            action_string = f"{item_config.action.type}::{item_config.action.value}"
            action_args = item_config.action.args
            prompt_args = item_config.action.prompt_args  # <-- Get prompt_args

        if action_string:
            action_callable = functools.partial(
                execute_action_string,
                action_string,
                # Pass pre-defined args to the partial. Runtime args will be handled by the app.
                args=action_args,
            )

        menu_item = MenuItem(
            description=item_config.description,
            action=action_callable,
            target_menu=item_config.target_menu,
            is_quit=item_config.is_quit,
            args=action_args,
            prompt_args=prompt_args,  # <-- Pass prompt_args to the MenuItem
        )

        field_definitions[item_name] = (MenuItem, Field(default=menu_item))

    NewMenu = create_model(name, __base__=TyperdanticMenu, **field_definitions)

    from typerdantic.app import TyperdanticApp  # noqa: F401

    NewMenu.model_rebuild(force=True)

    NewMenu.__doc__ = config.doc
    return NewMenu

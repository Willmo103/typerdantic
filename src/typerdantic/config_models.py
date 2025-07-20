# src/typerdantic/config_models.py

from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, Union


class ActionConfig(BaseModel):
    """
    Defines a structured action with a type, a value, and optional arguments.

    This model is useful for defining actions in a menu configuration file,
    allowing for both simple and complex actions to be executed by the application.
    Args:
        type: The type of action (e.g., 'internal', 'command', 'script').
        value: The target of the action (e.g., function name, command string).
        args: Optional dictionary of arguments to pass to the action.
    Raises:
        ValueError: If the action type is not recognized or if the value is not a valid action target.
    Examples:
    ```json
        "action": "command::ls -l"
    ```

    ```json
        "action": {
            "type": "internal",
            "value": "my_func",
            "args": {"name": "World"},
        }
    ```
    """

    type: str = Field(
        ...,
        description="The type of action (e.g., 'internal', 'command', 'script').",
    )
    value: str = Field(
        ...,
        description="The target of the action (e.g., function name, command string).",
    )
    args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="A dictionary of arguments to pass to the action.",
    )


class MenuItemConfig(BaseModel):
    """
    Defines the structure for a single menu item in a config file.
    The 'action' can now be a simple string or a detailed ActionConfig object.
    """

    description: str
    action: Optional[Union[str, ActionConfig]] = Field(
        default=None,
        description="The action string or a structured action object.",
        examples=[
            "command::ls -l",
            {
                "type": "internal",
                "value": "my_func",
                "args": {"name": "World"},
            },
        ],
    )
    target_menu: Optional[str] = None
    is_quit: bool = False


class MenuConfig(BaseModel):
    """Defines the top-level structure for a menu configuration file."""

    doc: str = "Typerdantic Menu"
    items: Dict[str, MenuItemConfig]

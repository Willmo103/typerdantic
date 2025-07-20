# src/typerdantic/config_models.py

from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, Union, List


class ArgumentSpec(BaseModel):
    """Defines a specification for an argument to be prompted for at runtime."""

    name: str = Field(..., description="The name of the argument variable.")
    prompt: str = Field(..., description="The message to display to the user.")
    default: Optional[Any] = Field(
        None,
        description="An optional default value if the user enters nothing.",
    )


class ActionConfig(BaseModel):
    """
    Defines a structured action with a type, a value, and optional arguments.
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
        default=None, description="A dictionary of pre-defined arguments."
    )
    prompt_args: Optional[List[ArgumentSpec]] = Field(
        default=None,
        description="A list of arguments to prompt for at runtime.",
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

# src/typerdantic/models.py

from pydantic import BaseModel, Field
from typing import Any, Callable, Optional, Dict, List


# Forward reference for ArgumentSpec
class ArgumentSpec(BaseModel):
    name: str
    prompt: str
    default: Optional[Any] = None


class MenuItem(BaseModel):
    """
    Represents a single, selectable item within a TyperdanticMenu.
    """

    description: str = Field(
        ..., description="The text displayed for this menu item."
    )
    action: Optional[Callable[..., Any]] = Field(
        default=None,
        description="A function to execute when this item is selected.",
    )
    target_menu: Optional[str] = Field(
        default=None,
        description="The name of another registered menu to navigate to.",
    )
    is_quit: bool = Field(
        default=False,
        description="If True, selecting this item will go back or exit.",
    )
    args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="A dictionary of pre-defined arguments for the item's action.",
    )
    prompt_args: Optional[List[ArgumentSpec]] = Field(
        default=None,
        description="A list of argument specifications to prompt for at runtime.",
    )

    class Config:
        arbitrary_types_allowed = True

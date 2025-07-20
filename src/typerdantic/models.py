# src/typerdantic/models.py

from pydantic import BaseModel, Field
from typing import Any, Callable, Optional, Dict


class MenuItem(BaseModel):
    """
    Represents a single, selectable item within a TyperdanticMenu.
    """

    description: str = Field(..., description="The text displayed for this menu item.")
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
    # Add a field to hold arguments for the action.
    args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="A dictionary of arguments for the item's action.",
    )

    class Config:
        arbitrary_types_allowed = True

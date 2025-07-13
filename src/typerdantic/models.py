# src/typerdantic/models.py

from pydantic import BaseModel, Field
from typing import Any, Callable, Optional


class MenuItem(BaseModel):
    """
    Represents a single, selectable item within a TyperdanticMenu.

    This is not meant to be instantiated by the user directly, but rather
    used with pydantic.Field to define the properties of a menu choice.
    """

    description: str = Field(..., description="The text displayed for this menu item.")

    action: Optional[Callable[..., Any]] = Field(
        default=None,
        description="The function or coroutine to execute when this item is selected.",
    )

    is_quit: bool = Field(
        default=False,
        description="If True, selecting this item will exit the current menu loop.",
    )

    # This allows the model to be used without validation errors for callables
    class Config:
        arbitrary_types_allowed = True

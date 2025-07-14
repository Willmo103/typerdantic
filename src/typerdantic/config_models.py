# src/typerdantic/config_models.py

from pydantic import BaseModel, Field
from typing import Dict, Optional


class MenuItemConfig(BaseModel):
    """Defines the structure for a single menu item in a config file."""

    description: str
    action: Optional[str] = Field(
        None,
        description="The action string, e.g., 'command::echo Hello World'",
        examples=["command::ls -l", "script::./my_script.sh"],
    )
    target_menu: Optional[str] = None
    is_quit: bool = False


class MenuConfig(BaseModel):
    """Defines the top-level structure for a menu configuration file."""

    doc: str = "Typerdantic Menu"
    items: Dict[str, MenuItemConfig]

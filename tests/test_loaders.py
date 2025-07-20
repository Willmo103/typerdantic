# file: tests/test_loaders.py

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from typerdantic.app import TyperdanticApp
from typerdantic.config_models import MenuConfig
from typerdantic.loaders import create_menu_from_config


async def main():
    """
    Tests the dynamic creation of a menu from a dictionary configuration.
    """
    # Define the menu structure as a Python dictionary
    MENU_CONFIG_DICT = {
        "doc": "Dynamically Loaded Menu",
        "items": {
            "item1": {"description": "A simple item with no action"},
            "command_item": {
                "description": "Run a command",
                "action": "command::echo 'Hello from dynamic menu!'",
            },
            "quit_item": {
                "description": "Exit this menu",
                "is_quit": True,
            },
        },
    }

    # 1. Validate the dictionary with the Pydantic model
    menu_config_obj = MenuConfig(**MENU_CONFIG_DICT)

    # 2. Dynamically create the menu class from the config object
    DynamicMenu = create_menu_from_config("DynamicMenu", menu_config_obj)

    # 3. Run it inside a TyperdanticApp
    app = TyperdanticApp(main_menu=DynamicMenu)
    await app.run()


if __name__ == "__main__":
    print("--- Testing Dynamic Menu Loader ---")
    try:
        asyncio.run(main())
        print("\nDynamic loader test finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\nTest interrupted by user.")

# file: tests/test_loaders.py

from typerdantic.actions import simple_action, another_async_action
from typerdantic.loaders import create_menu_from_dict
from typerdantic.app import TyperdanticApp
import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


async def main():
    """
    Tests the dynamic creation of a menu from a dictionary configuration.
    """
    # Define the menu structure as a Python dictionary
    MENU_CONFIG = {
        "doc": """
        Dynamically Loaded Menu

        This menu was created from a dictionary, not a class.
        """,
        "items": {
            "item1": {"description": "A simple item with no action"},
            "sync_action_item": {
                "description": "Run a simple synchronous action",
                "action": simple_action,  # Pass the function directly
            },
            "async_action_item": {
                "description": "Run an async action",
                "action": another_async_action,
            },
            "quit_item": {
                "description": "Exit this menu",
                "is_quit": True,
            },
        },
    }

    # 1. Dynamically create the menu class from the config
    DynamicMenu = create_menu_from_dict("DynamicMenu", MENU_CONFIG)

    # 2. Run it inside a TyperdanticApp
    app = TyperdanticApp(main_menu=DynamicMenu)
    await app.run()


if __name__ == "__main__":
    print("--- Testing Dynamic Menu Loader ---")
    try:
        asyncio.run(main())
        print("\nDynamic loader test finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\nTest interrupted by user.")

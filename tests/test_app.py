# file: tests/test_app.py

from pydantic import Field
from . import TyperdanticApp, TyperdanticMenu, MenuItem
import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


# --- Define Actions ---


def change_setting():
    print("\n>>> Pretending to change a setting...")


# --- Define Menus ---


class SettingsMenu(TyperdanticMenu):
    """Configure application settings."""

    change_item: MenuItem = Field(
        default=MenuItem(description="Change a setting", action=change_setting)
    )
    back: MenuItem = Field(
        default=MenuItem(description="Back to Main Menu", is_quit=True)
    )


class MainMenu(TyperdanticMenu):
    """This is the main menu."""

    explore: MenuItem = Field(
        default=MenuItem(description="Explore files (not implemented)")
    )
    settings: MenuItem = Field(
        default=MenuItem(
            description="Go to Settings",
            target_menu="settings",  # This name must match a registered menu
        )
    )
    exit_app: MenuItem = Field(
        default=MenuItem(description="Exit Application", is_quit=True)
    )


# --- Main execution block ---


async def main():
    # 1. Create the app with a main menu
    app = TyperdanticApp(main_menu=MainMenu)

    # 2. Register other menus
    app.register_menu("settings", SettingsMenu)

    # 3. Run the application
    await app.run()


if __name__ == "__main__":
    print("Starting TyperdanticApp multi-menu test...")
    try:
        asyncio.run(main())
        print("App finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\nApp interrupted by user.")

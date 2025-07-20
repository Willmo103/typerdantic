# file: tests/test_app.py

from pydantic import Field
from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem
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
async def run_test_app():
    """Run the `Interactive` MainMenu in a TyperdanticApp.

    This will Launch a TyperdanticApp with the MainMenu as the main menu.

    Target metrics for this test:
     - Ensure the MainMenu displays correctly
       **Expected**: MainMenu with "Explore files" and "Settings" options
     - Test navigation between menu items
       **Expected**: Users can navigate using arrow keys
     - Ensure there is a clean pass-off between menus
       **Expected**: Selecting "Settings" opens SettingsMenu, and "Back" returns to
       **Expected**: No visible external "flashes" of the terminal during navigation
     - Ensure the app can handle synchronous and asynchronous actions
         **Expected**: Synchronous actions execute immediately, async actions run without blocking
     - Ensure the app can handle KeyboardInterrupt gracefully.
         **Expected**: App exits cleanly on Ctrl+C
       - Ensure the app can handle EOFError gracefully.
         **Expected**: App exits cleanly on Ctrl+D
    """
    print(run_test_app.__doc__)
    input("Press Enter to start the TyperdanticApp test...")
    # 1. Create the app with a main menu
    app = TyperdanticApp(main_menu=MainMenu)

    # 2. Register other menus
    app.register_menu("settings", SettingsMenu)

    # 3. Run the application
    await app.run()


if __name__ == "__main__":
    print("Starting TyperdanticApp multi-menu test...")
    try:
        asyncio.run(run_test_app())
        print("App finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\nApp interrupted by user.")

# file: tests/test_menu.py

from pydantic import Field
from typerdantic import TyperdanticMenu, MenuItem, TyperdanticApp
import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path to allow importing typerdantic
# This is a common pattern for running test scripts directly.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


# --- Define some actions for the menu items ---


def sync_action():
    """A simple synchronous function to be called by a menu item."""
    print("\n>>> Executing a regular synchronous function!")


async def async_action():
    """A simple asynchronous function to test async action handling."""
    print("\n>>> Starting an asynchronous action...")
    await asyncio.sleep(2)
    print(">>> Finished asynchronous action!")


# --- Define the Test Menu using Typerdantic ---


class TestMenu(TyperdanticMenu):
    """
    Typerdantic Test Menu

    This menu demonstrates basic navigation, scrolling, and action execution.
    """

    # Create more items than _max_display_items (default 10) to test scrolling
    item_1: MenuItem = Field(default=MenuItem(description="Item 1"))
    item_2: MenuItem = Field(default=MenuItem(description="Item 2"))
    item_3: MenuItem = Field(default=MenuItem(description="Item 3"))
    item_4: MenuItem = Field(default=MenuItem(description="Item 4"))
    item_5: MenuItem = Field(default=MenuItem(description="Item 5"))
    item_6: MenuItem = Field(default=MenuItem(description="Item 6"))
    item_7: MenuItem = Field(default=MenuItem(description="Item 7"))
    item_8: MenuItem = Field(default=MenuItem(description="Item 8"))
    item_9: MenuItem = Field(default=MenuItem(description="Item 9"))
    item_10: MenuItem = Field(default=MenuItem(description="Item 10"))
    item_11: MenuItem = Field(
        default=MenuItem(description="Item 11 (should require scrolling)")
    )
    item_12: MenuItem = Field(default=MenuItem(description="Item 12"))

    sync_item: MenuItem = Field(
        default=MenuItem(
            description="Run a Synchronous Action", action=sync_action
        )
    )
    async_item: MenuItem = Field(
        default=MenuItem(
            description="Run an Asynchronous Action", action=async_action
        )
    )

    quit_item: MenuItem = Field(
        default=MenuItem(description="Quit", is_quit=True)
    )


# --- Main execution block ---
async def run_test_menu():
    """Run the `Interactive` TestMenu in a TyperdanticApp.

    This will Launch a TyperdanticApp with the TestMenu as the main menu.

    Target Metrics for this test:
    - Ensure the menu displays all items correctly.
        -Expected: All items should be visible, with scrolling enabled if necessary.
    - Verify that the synchronous action executes correctly.
        -Expected: The synchronous action should print a message to the console, pausing for user input.
    - Verify that the asynchronous action executes correctly.
        -Expected: The asynchronous action should print a message to the console after a delay.
    - Ensure the quit action exits the menu cleanly.
        -Expected: The application should exit without errors when the quit action is selected.
    - Test navigation through the menu.
        -Expected: Users should be able to navigate through the menu items using arrow keys.
    - Ensure the menu can handle more items than can fit on the screen.
        -Expected: Scrolling should work correctly when there are more items than can fit on the
        screen.
    - Test both synchronous and asynchronous actions.
        -Expected: Both actions should execute without errors and produce the expected output.

    """
    app = TyperdanticApp(main_menu=TestMenu)
    app.register_menu("test", TestMenu)

    print("Starting Typerdantic interactive test...")
    try:
        await app.run()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"An error occurred while running the test menu: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(run_test_menu())
        print("Test finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\nTest interrupted by user.")

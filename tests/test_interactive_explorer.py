# file: tests/test_interactive_explorer.py

import asyncio
import sys
from pathlib import Path

# Add project and source directories to the Python path before local imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from examples.file_explorer import FileExplorerMenu
from typerdantic.app import TyperdanticApp


# --- Interactive Test for FileExplorerMenu ---
async def main():
    """
    Launches an interactive test for the refactored FileExplorerMenu.
    """
    print("--- Interactive File Explorer Test ---")
    print("Navigate with arrow keys. Press 'q' or Ctrl+C to exit.")

    # Create an app using the FileExplorerMenu as the entry point
    app = TyperdanticApp(main_menu=FileExplorerMenu)
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\nInteractive explorer test finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\nTest interrupted by user.")

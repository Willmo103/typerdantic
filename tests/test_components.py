# file: tests/test_components.py

from examples.file_explorer import FileExplorerComponent
from typerdantic.app import TyperdanticApp
import asyncio
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# We need to import the example component to test it
sys.path.insert(0, str(project_root))


class TestComponents(unittest.TestCase):
    @patch("os.scandir")
    def test_file_explorer_component(self, mock_scandir):
        """
        Tests that the FileExplorerComponent can be registered and its
        dynamic menu items are generated correctly.
        """
        # --- Setup Mocks ---
        # Mock the file system to return a predictable list of files/dirs
        mock_dir_entry = MagicMock()
        mock_dir_entry.name = "test_dir"
        mock_dir_entry.is_dir.return_value = True

        mock_file_entry = MagicMock()
        mock_file_entry.name = "test_file.txt"
        mock_file_entry.is_dir.return_value = False

        mock_scandir.return_value = [mock_dir_entry, mock_file_entry]

        # --- Test Logic ---
        # 1. Create an instance of our component
        explorer = FileExplorerComponent()

        # 2. Create an app, using the component's main menu
        app = TyperdanticApp(main_menu=explorer.FileExplorerMenu)

        # 3. Register the component with the app
        app.register_component(explorer)

        # 4. Check if the dynamic items were generated correctly
        # The active_menu is an instance of FileExplorerMenu
        menu_items = app.active_menu.get_items()

        self.assertEqual(len(menu_items), 3)  # Go Up, test_dir, test_file.txt
        self.assertEqual(menu_items[0][1].description, "[.. Go Up]")
        self.assertEqual(menu_items[1][1].description, "[D] test_dir")
        self.assertEqual(menu_items[2][1].description, "[F] test_file.txt")

        # 5. Check if the component's actions were registered with the app
        self.assertIn("go_up", app.action_registry)
        self.assertIn("view_details", app.action_registry)


if __name__ == "__main__":
    unittest.main()

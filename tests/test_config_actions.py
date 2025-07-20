# file: tests/test_config_actions.py

from typerdantic.config_models import MenuConfig
from typerdantic.loaders import create_menu_from_config
from typerdantic.app import TyperdanticApp
import asyncio
import sys
import tempfile
import unittest
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


class TestConfigActions(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory and some test scripts."""
        self.tmpdir = tempfile.TemporaryDirectory(delete=False)
        self.tmp_path = Path(self.tmpdir.name)

        # Create a test shell script
        self.script_path = self.tmp_path / "test_script.ps1"
        self.script_output_path = self.tmp_path / "script_output.txt"
        # Use a simple command that works on both Windows and Unix-like systems
        self.script_path.write_text(
            f'echo "script ran" > "{self.script_output_path}"'
        )

    def tearDown(self):
        """Clean up the temporary directory."""
        self.tmpdir.cleanup()

    def test_dynamic_menu_with_external_actions(self):
        """
        Tests creating a menu from a config that executes external commands.
        """
        self.setUp()

        command_output_path = self.tmp_path / "command_output.txt"

        # Define a menu configuration using our Pydantic models
        menu_dict = {
            "doc": "External Action Test Menu",
            "items": {
                "command_item": {
                    "description": "Run a shell command (echo)",
                    # Use a command that works on both Windows and Unix
                    "action": f'command::echo "command ran" > {command_output_path}',
                },
                "script_item": {
                    "description": "Run a shell script",
                    # Use 'bash' for unix, or just run for windows
                    "action": f'script::{"bash " if sys.platform != "win32" else ""}{self.script_path}',
                },
                "quit_item": {"description": "Quit", "is_quit": True},
            },
        }

        # Validate the dictionary with our Pydantic model
        menu_config = MenuConfig(**menu_dict)

        # Create the menu class from the validated config
        DynamicActionMenu = create_menu_from_config(
            "DynamicActionMenu", menu_config
        )

        # We need to run the app to test the actions
        app = TyperdanticApp(main_menu=DynamicActionMenu)

        # To test non-interactively, we can simulate selections
        async def run_test_flow():
            # Simulate selecting the 'command' item
            app.active_menu._selected_index = 0
            command_item = app.active_menu.get_selected_item()
            await app.handle_selection(command_item)

            # Simulate selecting the 'script' item
            app.active_menu._selected_index = 1
            script_item = app.active_menu.get_selected_item()
            await app.handle_selection(script_item)

        # Run the simulation
        asyncio.run(run_test_flow())

        # Assert that the output files were created with the correct content
        self.assertTrue(command_output_path.exists())
        content_from_command = (
            command_output_path.read_text().strip().strip('"')
        )
        self.assertEqual(content_from_command, "command ran")

        self.assertTrue(self.script_output_path.exists())
        # Reading the output from the PowerShell script
        content_from_script = self.script_output_path.read_text(
            encoding="utf-16"
        ).strip()
        self.assertEqual(content_from_script, "script ran")


if __name__ == "__main__":
    unittest.main()

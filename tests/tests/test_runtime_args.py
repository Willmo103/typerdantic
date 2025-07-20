# file: tests/test_runtime_args.py

import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from pathlib import Path
import sys

# Add project and source directories to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

from typerdantic.config_models import MenuConfig
from typerdantic.loaders import create_menu_from_config
from typerdantic.app import TyperdanticApp


class TestRuntimeArgs(unittest.TestCase):

    @patch("typerdantic.executors.run_command", new_callable=AsyncMock)
    @patch(
        "prompt_toolkit.shortcuts.PromptSession.prompt_async",
        new_callable=AsyncMock,
    )
    def test_script_with_runtime_args(
        self, mock_prompt: AsyncMock, mock_run_command: AsyncMock
    ):
        """Verify that the app prompts for args and formats the script command."""
        # Simulate user typing "MyNewFolder" at the prompt
        mock_prompt.return_value = "MyNewFolder"
        mock_run_command.return_value = (0, "Mock output", "")

        menu_dict = {
            "doc": "Runtime Arg Test",
            "items": {
                "make_dir": {
                    "description": "Make a new directory",
                    "action": {
                        "type": "command",
                        "value": "mkdir {dir_name}",
                        "prompt_args": [
                            {
                                "name": "dir_name",
                                "prompt": "Enter directory name",
                                "default": "default_dir",
                            }
                        ],
                    },
                }
            },
        }

        menu_config = MenuConfig.model_validate(menu_dict)
        TestMenu = create_menu_from_config("TestMenu", menu_config)
        app = TyperdanticApp(main_menu=TestMenu)

        item = app.active_menu.get_selected_item()
        asyncio.run(app.handle_selection(item))

        # Verify the user was prompted correctly
        mock_prompt.assert_awaited_once_with(
            "Enter directory name: ", default="default_dir"
        )

        # Verify the command was called with the user's input
        mock_run_command.assert_awaited_once_with("mkdir MyNewFolder")


if __name__ == "__main__":
    unittest.main(verbosity=2)

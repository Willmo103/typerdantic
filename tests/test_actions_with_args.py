# file: tests/test_actions_with_args.py

import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path
import sys

# Add project and source directories to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

from typerdantic.config_models import MenuConfig
from typerdantic.loaders import create_menu_from_config
from typerdantic.app import TyperdanticApp
from typerdantic.registry import register_action, _ACTION_REGISTRY

# --- Mockable Actions for Testing ---


@register_action("test_greet")
def greet_action(context: dict, args: dict):
    """A test action that uses args."""
    name = args.get("name", "World")
    # You could use context here, e.g., context['app'].some_method()
    print(f"Hello, {name}!")


@register_action("test_async_greet")
async def async_greet_action(context: dict, args: dict):
    """An async test action."""
    name = args.get("name", "Async World")
    await asyncio.sleep(0.01)
    print(f"Hello, {name}!")


class TestActionsWithArgs(unittest.TestCase):

    def setUp(self):
        """Clear the registry before each test to ensure isolation."""
        _ACTION_REGISTRY.clear()
        # Re-register our test actions
        register_action("test_greet")(greet_action)
        register_action("test_async_greet")(async_greet_action)

    @patch(
        "prompt_toolkit.shortcuts.PromptSession.prompt_async",
        new_callable=AsyncMock,
    )
    @patch("typerdantic.executors.run_command", new_callable=AsyncMock)
    def test_command_action_with_args(
        self, mock_run_command: AsyncMock, mock_prompt: AsyncMock
    ):
        """Verify that 'command::' actions are formatted with args."""
        # FIX: Configure the mock to return a valid tuple, which the real function would.
        mock_run_command.return_value = (0, "Mock output", "")

        menu_dict = {
            "doc": "Command Test",
            "items": {
                "echo_item": {
                    "description": "Echo Name",
                    "action": {
                        "type": "command",
                        "value": "echo Hello {name}",
                        "args": {"name": "Will"},
                    },
                }
            },
        }
        menu_config = MenuConfig.model_validate(menu_dict)
        TestMenu = create_menu_from_config("TestMenu", menu_config)
        app = TyperdanticApp(main_menu=TestMenu)

        # Simulate selecting the item
        item = app.active_menu.get_selected_item()
        asyncio.run(app.handle_selection(item))

        # Check that run_command was called with the formatted string
        mock_run_command.assert_awaited_once_with("echo Hello Will")

    @patch(
        "prompt_toolkit.shortcuts.PromptSession.prompt_async",
        new_callable=AsyncMock,
    )
    @patch("builtins.print")
    def test_internal_action_with_args_and_context(
        self, mock_print: MagicMock, mock_prompt: AsyncMock
    ):
        """Verify that 'internal::' actions receive context and args."""
        menu_dict = {
            "doc": "Internal Test",
            "items": {
                "greet_item": {
                    "description": "Greet Will",
                    "action": {
                        "type": "internal",
                        "value": "test_greet",
                        "args": {"name": "Will"},
                    },
                }
            },
        }
        menu_config = MenuConfig.model_validate(menu_dict)
        TestMenu = create_menu_from_config("TestMenu", menu_config)
        app = TyperdanticApp(main_menu=TestMenu)

        item = app.active_menu.get_selected_item()
        asyncio.run(app.handle_selection(item))

        # Check that our action printed the correct, formatted message
        mock_print.assert_any_call("Hello, Will!")


if __name__ == "__main__":
    unittest.main(verbosity=2)

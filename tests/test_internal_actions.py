# file: tests/test_internal_actions.py

from typerdantic.registry import register_action
from typerdantic.config_models import MenuConfig
from typerdantic.loaders import create_menu_from_config
from typerdantic.app import TyperdanticApp
import asyncio
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, AsyncMock, MagicMock

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


# --- Define dummy actions for type hinting and as real objects if needed ---

@register_action("say_hello")
def hello_action():
    pass


@register_action("do_async_work")
async def async_work_action():
    pass


class TestInternalActions(unittest.TestCase):
    # Patch the PromptSession to prevent hanging.
    # FIX: Update the patch target to the new, explicit path.
    @patch('typerdantic.app.PromptSession')
    @patch('typerdantic.executors.registry.get_action')
    def test_internal_action_execution(self, mock_get_action, MockPromptSession):
        """
        Tests that the app calls the correct registered internal actions
        by mocking the registry lookup instead of the actions themselves.
        """
        # --- Setup the mocks ---
        # Configure the mock session to return immediately.
        MockPromptSession.return_value.prompt_async = AsyncMock()

        # Create separate mocks for each action.
        mock_hello = MagicMock()
        mock_async = AsyncMock()

        # Configure mock_get_action to return the correct mock based on the name.
        def get_action_side_effect(action_name):
            if action_name == "say_hello":
                return mock_hello
            if action_name == "do_async_work":
                return mock_async
            return None

        mock_get_action.side_effect = get_action_side_effect

        # --- Test logic ---
        menu_dict = {
            "doc": "Internal Action Test Menu",
            "items": {
                "hello_item": {
                    "description": "Say Hello",
                    "action": "internal::say_hello",
                },
                "async_item": {
                    "description": "Do async work",
                    "action": "internal::do_async_work",
                },
            },
        }

        menu_config = MenuConfig(**menu_dict)
        DynamicInternalMenu = create_menu_from_config("DynamicInternalMenu", menu_config)
        app = TyperdanticApp(main_menu=DynamicInternalMenu)

        async def run_test_flow():
            # Simulate selecting the 'hello' item
            app.active_menu._selected_index = 0
            hello_item = app.active_menu.get_selected_item()
            await app.handle_selection(hello_item)

            # Simulate selecting the 'async' item
            app.active_menu._selected_index = 1
            async_item = app.active_menu.get_selected_item()
            await app.handle_selection(async_item)

        asyncio.run(run_test_flow())

        # Check that our mocked actions were called correctly
        mock_hello.assert_called_once()
        mock_async.assert_awaited_once()


if __name__ == "__main__":
    # Clear the registry before running tests to ensure a clean state,
    # just in case this file is run directly multiple times.
    from typerdantic.registry import _ACTION_REGISTRY
    _ACTION_REGISTRY.clear()
    unittest.main()

# file: tests/test_internal_actions.py

from typerdantic.registry import register_action
from typerdantic.config_models import MenuConfig
from typerdantic.loaders import create_menu_from_config
from typerdantic.app import TyperdanticApp
import asyncio
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


# --- Register some internal actions ---


@register_action("say_hello")
def hello_action():
    """A simple, registered synchronous action."""
    print("Hello from a registered action!")


@register_action("do_async_work")
async def async_work_action():
    """A simple, registered asynchronous action."""
    print("Starting async work...")
    await asyncio.sleep(0.01)  # Use a very short sleep for tests
    print("Finished async work.")


class TestInternalActions(unittest.TestCase):
    # FIX: Patch PromptSession where it's used in the app module to prevent hanging.
    @patch('typerdantic.app.PromptSession')
    @patch('builtins.print')
    def test_internal_action_execution(self, mock_print, MockPromptSession):
        """
        Tests creating a menu that calls registered internal actions.
        """
        # --- Setup the mocks ---
        # Configure the mock session and its async method to return immediately.
        mock_session_instance = MockPromptSession.return_value

        # Create a mock for the async method that returns a completed Future
        async_mock = MagicMock()
        future = asyncio.Future()
        future.set_result(None)
        async_mock.return_value = future
        mock_session_instance.prompt_async = async_mock

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
                "quit_item": {"description": "Quit", "is_quit": True},
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

        # Check if our print statements were called by the actions
        mock_print.assert_any_call("Hello from a registered action!")
        mock_print.assert_any_call("Starting async work...")
        mock_print.assert_any_call("Finished async work.")


if __name__ == "__main__":
    unittest.main()

# file: examples/project_wizard.py

import asyncio
import json
import os
from pathlib import Path
import sys

# Add project and source directories to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem
from typerdantic.registry import register_action
from pydantic import Field


@register_action("create_project_file")
def create_project_file(context: dict, args: dict):
    """
    Takes the arguments gathered from the wizard and writes them to a JSON file.
    """
    project_name = args.get("project_name", "my-awesome-project")
    file_name = f"{project_name}.json"

    print(f"\nCreating project file: {file_name}")
    try:
        with open(file_name, "w") as f:
            json.dump(args, f, indent=2)
        print(f"Successfully created '{file_name}'!")
    except Exception as e:
        print(f"Error creating file: {e}")


class ProjectWizardMenu(TyperdanticMenu):
    """
    Project Setup Wizard

    This menu guides the user through creating a new project.
    """

    # This single menu item triggers a series of prompts.
    start_wizard: MenuItem = Field(
        default=MenuItem(
            description="Start New Project Wizard",
            action="internal::create_project_file",
            # Define the series of questions to ask the user.
            prompt_args=[
                {"name": "project_name", "prompt": "Enter project name"},
                {
                    "name": "author_name",
                    "prompt": "Enter author name",
                    "default": f"{os.environ.get('USER', 'Your Username')}",
                },
                {
                    "name": "version",
                    "prompt": "Enter initial version",
                    "default": "0.1.0",
                },
            ],
        )
    )
    quit_app: MenuItem = Field(default=MenuItem(description="Exit", is_quit=True))


if __name__ == "__main__":
    app = TyperdanticApp(main_menu=ProjectWizardMenu)
    try:
        asyncio.run(app.run())
    except (KeyboardInterrupt, EOFError):
        print("\nWizard exited.")

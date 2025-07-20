# file: examples/dynamic_task_runner.py

import asyncio
import json
from pathlib import Path
from typing import List, Tuple
import sys

# Add project and source directories to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))


from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem
from typerdantic.registry import register_action


# --- Register Internal Actions ---
# These are the functions that our tasks.json can call.


@register_action("greet")
def greet(context: dict, args: dict):
    print("\nHello from a registered internal task!")


@register_action("generate_report")
def generate_report(context: dict, args: dict):
    report_name = args.get("report_name", "default_report")
    file_name = f"{report_name}.txt"
    print(f"\nGenerating report '{file_name}'...")
    Path(file_name).write_text(f"This is the report for {report_name}.")
    print("Report generated successfully.")


# --- Dynamic Menu Definition ---


class TaskRunnerMenu(TyperdanticMenu):
    """Dynamic Task Runner"""

    def get_items(self) -> List[Tuple[str, MenuItem]]:
        """
        Dynamically loads tasks from tasks.json and creates menu items.
        """
        items: List[Tuple[str, MenuItem]] = []
        tasks_file = Path("tasks.json")

        if not tasks_file.exists():
            items.append(
                ("error", MenuItem(description="ERROR: tasks.json not found."))
            )
            return items

        try:
            with open(tasks_file, "r") as f:
                data = json.load(f)

            for i, task in enumerate(data.get("tasks", [])):
                # Create a MenuItem for each task defined in the JSON file.
                menu_item = MenuItem(
                    description=task.get("description", "No description"),
                    action=task.get("action"),
                    prompt_args=task.get("prompt_args"),
                )
                # Use the task name and index for a unique key.
                items.append((f"task_{i}_{task.get('name')}", menu_item))

        except Exception as e:
            items.append(
                (
                    "error",
                    MenuItem(description=f"ERROR: Could not parse tasks.json: {e}"),
                )
            )

        items.append(("quit", MenuItem(description="[Exit Task Runner]", is_quit=True)))
        return items


if __name__ == "__main__":
    app = TyperdanticApp(main_menu=TaskRunnerMenu)
    try:
        asyncio.run(app.run())
    except (KeyboardInterrupt, EOFError):
        print("\nTask runner exited.")

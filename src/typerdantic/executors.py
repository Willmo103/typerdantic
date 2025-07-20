# src/typerdantic/executors.py

import asyncio
import sys
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

from . import registry

# --- Action Executor ---


async def run_command(command: str) -> Tuple[int, str, str]:
    """
    Runs a shell command asynchronously and returns status and output.
    """
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        process.returncode if process.returncode is not None else -1,
        stdout.decode("utf-8", errors="ignore"),
        stderr.decode("utf-8", errors="ignore"),
    )


async def execute_action_string(
    action_string: str,
    context: Optional[Dict[str, Any]] = None,
    args: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Parses and executes an action string from a menu configuration.
    - `action_string`: The core action, e.g., "internal::my_func".
    - `context`: App-level context (e.g., the active menu).
    - `args`: Item-specific arguments from the config.
    """
    if not isinstance(action_string, str):
        print(
            f"\nError: Invalid action format. Expected a string, got {type(action_string)}"
        )
        return

    try:
        action_type, value = action_string.split("::", 1)
        action_type = action_type.strip().lower()
        value = value.strip()
    except ValueError:
        print(
            f"\nError: Invalid action format '{action_string}'. Expected 'type::value'."
        )
        return

    # Ensure args is a dictionary for formatting
    args = args or {}

    print(f"\nExecuting {action_type}: {value}")

    if action_type == "internal":
        action_func = registry.get_action(value)
        if action_func:
            # Pass both context from the app and args from the menu item
            if asyncio.iscoroutinefunction(action_func):
                await action_func(context=context, args=args)
            else:
                action_func(context=context, args=args)
        else:
            print(f"\nError: Internal action '{value}' not found in registry.")

    elif action_type in ["command", "script"]:
        # Format the command or script path with the provided arguments
        command_to_run = value.format(**args)

        if action_type == "script":
            script_path = Path(command_to_run)
            if (
                sys.platform == "win32"
                and script_path.suffix.lower() == ".ps1"
            ):
                command_to_run = f'powershell.exe -ExecutionPolicy Bypass -File "{script_path}"'
            elif script_path.suffix.lower() in [".sh", ".bash"]:
                command_to_run = f'bash "{script_path}"'
            elif script_path.suffix.lower() in [".bat", ".cmd"]:
                command_to_run = f'cmd.exe /c "{script_path}"'
            elif script_path.suffix.lower() == ".py":
                command_to_run = f'"{sys.executable}" "{script_path}"'
            elif script_path.suffix.lower() == ".js":
                command_to_run = f'node "{script_path}"'

        return_code, stdout, stderr = await run_command(command_to_run)

        print("-" * 20)
        if stdout:
            print("Output:\n" + stdout)
        if stderr:
            print("Errors:\n" + stderr)
        print(f"Process finished with exit code: {return_code}")
        print("-" * 20)

    else:
        print(f"\nError: Unknown action type '{action_type}'.")

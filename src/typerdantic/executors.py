# src/typerdantic/executors.py

import asyncio
import shlex
from typing import Tuple

from . import registry  # <-- More explicit import

# --- Action Executor ---


async def run_command(command: str) -> Tuple[int, str, str]:
    """
    Runs a shell command asynchronously and returns status and output.
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        process.returncode,
        stdout.decode('utf-8', errors='ignore'),
        stderr.decode('utf-8', errors='ignore')
    )


async def execute_action_string(action_string: str):
    """
    Parses and executes an action string from a menu configuration.
    """
    if not isinstance(action_string, str):
        print(f"\nError: Invalid action format. Expected a string, got {type(action_string)}")
        return

    try:
        action_type, value = action_string.split("::", 1)
        action_type = action_type.strip().lower()
        value = value.strip()
    except ValueError:
        print(f"\nError: Invalid action format '{action_string}'. Expected 'type::value'.")
        return

    print(f"\nExecuting {action_type}: {value}")

    if action_type == "internal":
        # Use the explicit path to look up the action
        action_func = registry.get_action(value)
        if action_func:
            if asyncio.iscoroutinefunction(action_func):
                await action_func()
            else:
                action_func()
        else:
            print(f"\nError: Internal action '{value}' not found in registry.")

    elif action_type in ["command", "script"]:
        return_code, stdout, stderr = await run_command(value)
        print("-" * 20)
        if stdout:
            print("Output:\n" + stdout)
        if stderr:
            print("Errors:\n" + stderr)
        print(f"Process finished with exit code: {return_code}")
        print("-" * 20)

    else:
        print(f"\nError: Unknown action type '{action_type}'.")

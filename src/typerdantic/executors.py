# src/typerdantic/executors.py

import asyncio
from typing import Tuple

# --- Action Executor ---


async def run_command(command: str) -> Tuple[int | None, str, str]:
    """
    Runs a shell command asynchronously and returns status and output.

    Args:
        command: The command string to execute.

    Returns:
        A tuple of (return_code, stdout, stderr).
    """

    # We run the blocking subprocess call in a separate thread
    # to avoid freezing the asyncio event loop.
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
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

    if action_type in ["command", "script"]:
        # For both 'command' and 'script', we execute a shell command.
        # The distinction can be handled by the caller if needed (e.g., checking file existence).
        return_code, stdout, stderr = await run_command(value)

        print("-" * 20)
        if stdout:
            print("Output:\n" + stdout)
        if stderr:
            print("Errors:\n" + stderr)
        print(f"Process finished with exit code: {return_code}")
        print("-" * 20)

    elif action_type == "python":
        # In the future, this could execute a Python script or string
        print("\n'python::' action type is not yet implemented.")

    else:
        print(f"\nError: Unknown action type '{action_type}'.")

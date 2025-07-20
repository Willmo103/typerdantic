import asyncio
import sys
from pathlib import Path
from typing import Tuple

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
        process.returncode,
        stdout.decode("utf-8", errors="ignore"),
        stderr.decode("utf-8", errors="ignore"),
    )


async def execute_action_string(action_string: str):
    """
    Parses and executes an action string from a menu configuration.
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

    print(f"\nExecuting {action_type}: {value}")

    if action_type == "internal":
        action_func = registry.get_action(value)
        if action_func:
            if asyncio.iscoroutinefunction(action_func):
                await action_func()
            else:
                action_func()
        else:
            print(f"\nError: Internal action '{value}' not found in registry.")

    elif action_type in ["command", "script"]:
        # --- FIX STARTS HERE ---
        # By default, the command is the raw value from the config.
        command_to_run = value

        # If the action is a script, build a more specific command to ensure
        # it's executed by an interpreter instead of opened by a default program.
        if action_type == "script":
            script_path = Path(value)
            # For PowerShell scripts on Windows, explicitly call powershell.exe.
            if sys.platform == "win32" and script_path.suffix.lower() == ".ps1":
                command_to_run = f'powershell.exe -File "{script_path}"'
            # For Python scripts, it's good practice to use the current interpreter.
            elif script_path.suffix.lower() == ".py":
                command_to_run = f'"{sys.executable}" "{script_path}"'

        return_code, stdout, stderr = await run_command(command_to_run)
        # --- FIX ENDS HERE ---

        print("-" * 20)
        if stdout:
            print("Output:\n" + stdout)
        if stderr:
            print("Errors:\n" + stderr)
        print(f"Process finished with exit code: {return_code}")
        print("-" * 20)

    else:
        print(f"\nError: Unknown action type '{action_type}'.")

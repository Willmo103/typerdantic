# Using Actions: Making Menus Do Things

Menus are great for showing options, but their real power comes from *actions*. An action is what happens when a user selects a menu item. Typerdantic supports a wide variety of actions, from simple function calls to running external scripts.

This guide covers the three main ways to define actions.

---

## 1. Callable Actions (The Standard Way)

The most common way to define an action is by passing a Python callable (like a function or a method) to the `action` argument of a `MenuItem`.

### Synchronous Actions

If your action is a quick, blocking operation, a regular synchronous function is perfect.

```python
def show_user_info():
    """A simple synchronous function."""
    # This function runs to completion before the user can do anything else.
    print("\nUser: Will Morris")
    print("Status: Active")

# In your TyperdanticMenu class:
user_info_item: MenuItem = Field(
    default=MenuItem(description="Show User Info", action=show_user_info)
)
````

When selected, `show_user_info` runs, prints the details, and the app waits for the user to press Enter before returning to the menu.

### Asynchronous Actions

For long-running tasks, like making a web request or processing a large file, you should use an `async` function. This keeps your UI from freezing.

```python
async def fetch_data():
    """An asynchronous function that doesn't block the UI."""
    print("\nFetching data from the server...")
    await asyncio.sleep(3) # Simulate a network request
    print("...Data fetched successfully!")

# In your TyperdanticMenu class:
fetch_data_item: MenuItem = Field(
    default=MenuItem(description="Fetch Server Data", action=fetch_data)
)
```

When this item is selected, Typerdantic will correctly `await` the coroutine, allowing other tasks to run if needed. The user sees the "Fetching..." message, and the UI remains responsive.

### Lambda Actions

For very simple, one-line actions, you can use a `lambda` function to avoid cluttering your code with lots of small `def` statements.

```python
# In your TyperdanticMenu class:
simple_item: MenuItem = Field(
    default=MenuItem(
        description="Quick Action",
        action=lambda: print("\nLambda action executed!")
    )
)
```

---

## 2\. String Actions (For Config-Driven Menus)

When you create menus from configuration files (see `config-driven-menus.md`), you can't use Python callables directly. Instead, you use special "action strings." Typerdantic parses these strings and executes the appropriate task.

An action string always follows the format `type::value`.

### `command::` - Running Shell Commands

This action type executes a command directly in your system's shell.

**Example `config.toml`:**

```toml
[items.list_files]
description = "List files in current directory"
# On Windows/PowerShell, this would be 'command::Get-ChildItem'
action = "command::ls -l"
```

When selected, Typerdantic runs `ls -l` (or `Get-ChildItem`) and prints the standard output and standard error to the screen.

### `script::` - Executing External Scripts

This is perfect for running more complex logic stored in external script files. Since you prefer PowerShell, let's use that as our example.

**Example PowerShell Script (`backup.ps1`):**

```powershell
# file: backup.ps1
param (
    [string]$Destination = "C:\Backups"
)

Write-Host "Starting backup process..."
# Add your real backup logic here
Start-Sleep -Seconds 2
Write-Host "Backup completed successfully to $Destination."
```

**Example `config.toml`:**

```toml
[items.run_backup]
description = "Run PowerShell Backup Script"
action = "script::C:/Scripts/backup.ps1"
```

Typerdantic will intelligently execute the script using the appropriate interpreter (e.g., `powershell.exe -File ...` for `.ps1` files on Windows).

### `internal::` - Using the Action Registry

This is the most powerful string action type. It allows you to map a string name to a Python function in your code. This is ideal when you need the flexibility of a config file but the power of Python for the action's logic.

**Step 1: Register the action in your Python code.**

```python
# file: my_app.py
from typerdantic.registry import register_action

@register_action("do_complex_thing")
def my_complex_python_function():
    """This function can now be called from a config file."""
    print("\nRunning complex logic from inside Python!")
    # ... do something interesting ...
```

**Step 2: Refer to it in your config file.**

```toml
# file: config.toml
[items.complex]
description = "Do a complex thing"
action = "internal::do_complex_thing"
```

When the item is selected, Typerdantic looks up `"do_complex_thing"` in its registry and executes the associated Python function.

---

## Next Steps

Now you're a master of actions\! You can make your menus perform any task you need, from simple print statements to complex, registered Python logic.

➡️ **Next up: [Config-Driven Menus](config-driven-menus.md)**

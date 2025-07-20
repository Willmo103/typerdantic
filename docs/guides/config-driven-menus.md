# **Config-Driven Menus: Separating UI from Code**

While defining menus in Python code is powerful, sometimes you want to separate your application's UI structure from its logic. This is especially useful if you want to allow end-users to customize their experience without touching the Python source code.

Typerdantic supports this out of the box by allowing you to define entire menus in simple TOML configuration files.

## **The "Why": Benefits of Config-Driven Menus**

* **Separation of Concerns**: Your Python code handles the *how* (the application logic), while the config file handles the *what* (the menu's appearance and options).
* **User Customization**: You can ship your application with a default menu configuration, and advanced users can override or extend it to suit their needs.
* **Rapid Prototyping**: Quickly sketch out complex menu flows in a simple text file without recompiling or re-running complex Python scripts.
* **Readability**: A well-structured TOML file can be easier to read for non-programmers than a Python class definition.

## **Step 1: Create the Menu Configuration File**

First, create a TOML file. Let's call it menu\_config.toml. This file will define the menu's title and all of its items. We'll use the three types of string actions we learned about in the previous guide.

\# file: menu\_config.toml

\# The 'doc' key becomes the menu's title.
doc \= "Dynamic Utility Menu (from TOML)"

\# The 'items' table contains all the menu items.
\# The key for each item (e.g., "list\_files") is an internal name.
\[items\]

  \[items.list\_files\]
  description \= "List files (PowerShell)"
  action \= "command::Get-ChildItem \-Name"

  \[items.run\_script\]
  description \= "Run a local PowerShell script"
  \# Make sure this script exists\!
  action \= "script::./my\_utility\_script.ps1"

  \[items.internal\_action\]
  description \= "Run a registered Python function"
  action \= "internal::say\_hello"

  \[items.quit\]
  description \= "Exit Menu"
  is\_quit \= true

You'll also need the PowerShell script referenced in the config. Create my\_utility\_script.ps1:

\# file: my\_utility\_script.ps1
Write-Host "Hello from an external PowerShell script\!"
Start-Sleep \-Seconds 1
Write-Host "The script has finished."

## **Step 2: Write the Python Loader**

Now, let's write the Python code to load, parse, and run this menu. The key functions here are tomllib.load (or tomli.load for Python \< 3.11) and Typerdantic's create\_menu\_from\_config.

\# file: config\_loader\_app.py

import asyncio
import sys
from pathlib import Path

\# Use the new tomllib for Python 3.11+, fall back to tomli for older versions
if sys.version\_info \>= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from typerdantic import TyperdanticApp
from typerdantic.config\_models import MenuConfig
from typerdantic.loaders import create\_menu\_from\_config
from typerdantic.registry import register\_action

\# \--- Register an internal action \---
\# This makes the "internal::say\_hello" action in the TOML file work.
@register\_action("say\_hello")
def hello\_from\_python():
    print("\\nThis message is from a registered Python function\!")

\# \--- Main Application Logic \---

async def main():
    """
    Loads a menu from a TOML file and runs it.
    """
    config\_path \= Path("menu\_config.toml")
    if not config\_path.exists():
        print(f"Error: Configuration file not found at '{config\_path}'")
        return

    \# 1\. Load the raw dictionary from the TOML file.
    with open(config\_path, "rb") as f:
        config\_dict \= tomllib.load(f)

    \# 2\. Validate the dictionary with our Pydantic model.
    \# This ensures the config file has the correct structure.
    try:
        menu\_config\_obj \= MenuConfig.model\_validate(config\_dict)
    except Exception as e:
        print(f"Error validating config file: {e}")
        return

    \# 3\. Dynamically create the menu class from the validated config.
    DynamicMenu \= create\_menu\_from\_config("DynamicMenu", menu\_config\_obj)

    \# 4\. Run it inside a TyperdanticApp.
    app \= TyperdanticApp(main\_menu=DynamicMenu)
    await app.run()

if \_\_name\_\_ \== "\_\_main\_\_":
    print("--- Testing Dynamic Menu Loader from TOML \---")
    try:
        asyncio.run(main())
        print("\\nDynamic loader test finished cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\\nTest interrupted by user.")

## **Step 3: Run It**

Make sure menu\_config.toml, my\_utility\_script.ps1, and config\_loader\_app.py are all in the same directory. Then, run the application:

python .\\config\_loader\_app.py

You will see the fully interactive menu, generated entirely from your TOML file\! Each item, when selected, will perform its configured command, script, or internal Python action.

## **Next Steps**

You've now seen the full power of separating your UI from your logic. This is a key feature for building maintainable and extensible CLI tools. The final piece of the puzzle is making it all look good.

➡️ **Next** up: [**Styling**](styling-guide.md)

# Styling Menus

Typerdantic uses the powerful `prompt-toolkit` library for rendering, which means you have full control over the look and feel of your menus. You can change colors, add underlines, make text bold, and more.

The easiest way to apply a custom look is by loading a simple TOML style file.

---

## The Core Style Classes

By default, Typerdantic uses three main style classes for its components:

- `class:title`: Applied to the menu's title (the docstring of your menu class).
- `class:selected`: Applied to the currently selected menu item (the one with the `>` cursor).
- `class:menu-item`: Applied to all other non-selected menu items.

You can override the styles for these classes to theme your application.

---

## Step 1: Create a `styles.toml` File

Create a file named `styles.toml`. In this file, you'll define your new styles under a `[style]` table. Let's recreate the "Forest" theme from your guide.

```toml
# file: styles.toml

[style]
# Style for the menu title: bold, underlined, and a bright green color.
title = "bold underline fg:#34d399"

# Style for the selected item: a dark blue background with bold white text.
selected = "bg:#1e3a8a #ffffff bold"

# Style for non-selected items: a lime green color.
menu-item = "fg:#a3e635"
```

Styling Syntax Quick Reference
**bg:#rrggbb**: Sets the background color using a hex code.
**fg:#rrggbb**: Sets the foreground (text) color using a hex code.

You can also use standard color names like green, blue, white, etc.

Attributes like bold, underline, and italic can be added to the string. from the docs:

> ## Style strings
>
> Many user interface controls, like Window accept a style argument which can be used to pass the formatting as a string. For instance, we can select a foreground color:
>
> - "fg:ansired" (ANSI color palette)
> - "fg:ansiblue" (ANSI color palette)
> - "fg:#ffaa33" (hexadecimal notation)
> - "fg:darkred" (named color)
>
> Or a background color:
>
> - "bg:ansired" (ANSI color palette)
> - "bg:#ffaa33" (hexadecimal notation)
>
> Or we can add one of the following flags:
>
> - "bold"
> - "italic"
> - "underline"
> - "blink"
> - "reverse" (reverse foreground and background on the terminal.)
> - "hidden"
>

For a complete list of all possible colors and attributes, refer to the official `prompt-toolkit` documentation on [Styling](https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html).

## Step 2: Load the Style in Your Application

Now, modify your application's entry point to load this file and pass the resulting style object to your TyperdanticApp.

```python

# file: styled_app.py

import asyncio
from pathlib import Path
from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem
from typerdantic.styles import load_style_from_file # <-- Import the loader
from pydantic import Field

# --- A simple menu for demonstration ---

class MainMenu(TyperdanticMenu):
    """My Styled Application"""
    item_one: MenuItem = Field(default=MenuItem(description="First Option"))
    item_two: MenuItem = Field(default=MenuItem(description="Second Option"))
    quit_item: MenuItem = Field(default=MenuItem(description="Exit", is_quit=True))

# --- Main application logic ---

from typerdantic.styles import load_style_from_file
from pathlib import Path
from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem
from pydantic import Field
import asyncio

async def main():
    # Define the path to your style file.
    style_path = Path("./styles.toml")

    # Load the custom style from the file.
    custom_style = load_style_from_file(style_path)

    # Create the app, passing the loaded style to the 'style' parameter.
    app = TyperdanticApp(main_menu=MainMenu, style=custom_style)

    # Run the application.
    await app.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nApplication exited.")
```

Step 3: Run and See the Changes
Place styles.toml and styled_app.py in the same directory and run the application:

```PowerShell
  python .\styled_app.py
```

Your menu will now be displayed with the "Forest" theme instead of the default blue and white. The title will be bright green and underlined, the selected item will be highlighted with a dark blue background, and the other items will be lime green.

What's Next?
Congratulations, you've completed the user guides! You now know how to create, navigate, action, and style Typerdantic menus.

For a more detailed breakdown of the available classes and functions, feel free to browse the API Reference.

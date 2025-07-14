## **Guide: Styling Typerdantic Menus**

Typerdantic allows you to customize the look and feel of your menus by providing a custom style object. You can define these styles in a simple TOML file and load them into your application.

### **1\. Create a Style File**

First, create a style configuration file. Let's call it styles.toml and place it in your project's root directory. The styles are defined under a \[style\] table.

Here is an example styles.toml with a "Forest" theme:

\# file: styles.toml

\[style\]  
\# Style for the menu title  
title \= "bold underline \#34d399"  \# Bright green

\# Style for the selected menu item  
selected \= "bg:\#1e3a8a \#ffffff bold" \# Dark blue background, white text

\# Style for non-selected menu items  
menu-item \= "\#a3e635" \# Lime green text

You can find a full list of available colors and attributes in the [prompt-toolkit styling documentation](https://www.google.com/search?q=https://python-prompt-toolkit.readthedocs.io/en/master/pages/styling.html).

### **2\. Load the Style in Your Application**

Next, update your main application script (e.g., tests/test\_app.py) to load this file and pass the resulting style to your TyperdanticApp.

\# file: tests/test\_app.py

import asyncio  
from pathlib import Path  
\# ... other imports

\# Import the style loader  
from typerdantic.styles import load\_style\_from\_file

\# \--- (Menu and Action definitions remain the same) \---

async def main():  
    \# Define the path to your style file  
    style\_path \= Path(\_\_file\_\_).parent / "styles.toml"

    \# Load the custom style  
    custom\_style \= load\_style\_from\_file(style\_path)

    \# 1\. Create the app, passing the loaded style  
    app \= TyperdanticApp(main\_menu=MainMenu, style=custom\_style)

    \# 2\. Register other menus  
    app.register\_menu("settings", SettingsMenu)

    \# 3\. Run the application  
    await app.run()

if \_\_name\_\_ \== "\_\_main\_\_":  
    \# ...

### **3\. Run and See the Changes**

Now, when you run your test application (uv run \-m tests.test\_app), the menu will appear with your new custom "Forest" theme instead of the default blue and white.
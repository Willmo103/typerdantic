# **Getting Started with Typerdantic**

Welcome\! This guide will walk you through creating your very first interactive command-line application with Typerdantic. We'll build a simple menu with a few options that execute different kinds of actions.

## **Prerequisites**

Before you begin, make sure you have Python (3.8 or newer) and pip installed.

## **Step 1: Installation**

First, let's install Typerdantic from PyPI. Open your terminal (PowerShell is a great choice) and run the following command:

pip install typerdantic

This will install Typerdantic and its dependencies, pydantic and prompt-toolkit.

## **Step 2: Create Your First Menu**

Now, let's write some code. Create a new file named my\_app.py and add the following content.

\# file: my\_app.py

import asyncio
from pydantic import Field
from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem

\# \--- 1\. Define Your Actions \---
\# An action can be any callable function. Typerdantic handles
\# both standard synchronous functions and async functions.

def show\_info():
    """A simple synchronous function."""
    print("\\nTyperdantic makes creating CLI menus easy\!")

async def perform\_long\_task():
    """A simple asynchronous function."""
    print("\\nStarting a long task (simulated with a sleep)...")
    await asyncio.sleep(2)
    print("...long task finished\!")

\# \--- 2\. Define Your Menu \---
\# A menu is a Pydantic model that inherits from TyperdanticMenu.
\# Each menu item is a field of the model.

class MainMenu(TyperdanticMenu):
    """
    My First Typerdantic App

    The docstring of the class is used as the title of the menu.
    """

    \# Use pydantic.Field to define a MenuItem.
    info\_item: MenuItem \= Field(
        default=MenuItem(
            description="Show App Info",  \# The text displayed in the menu
            action=show\_info             \# The function to call on selection
        )
    )

    task\_item: MenuItem \= Field(
        default=MenuItem(
            description="Perform a Long Task (Async)",
            action=perform\_long\_task
        )
    )

    \# A special menu item to exit the current menu or the app.
    quit\_item: MenuItem \= Field(
        default=MenuItem(
            description="Exit",
            is\_quit=True
        )
    )

\# \--- 3\. Run the Application \---
\# The main execution block initializes and runs the app.

if \_\_name\_\_ \== "\_\_main\_\_":
    \# Create an instance of the app, passing your main menu class.
    app \= TyperdanticApp(main\_menu=MainMenu)

    print("Starting the Typerdantic application... Press 'q' or Ctrl+C to exit.")

    \# Run the application.
    try:
        asyncio.run(app.run())
        print("\\nApplication exited cleanly.")
    except (KeyboardInterrupt, EOFError):
        print("\\nApplication interrupted by user.")

## **Step 3: Run Your Application**

Save the my\_app.py file and run it from your terminal:

python my\_app.py

You will see your interactive menu\!

\--- My First Typerdantic App \---
\> Show App Info
  Perform a Long Task (Async)
  Exit

You can use the **up** and **down** arrow **keys** to navigate and **Enter** to select an option.

* Selecting "Show App Info" will immediately print the message and wait for you to press Enter.
* Selecting "Perform a Long Task" will show the start message, pause for two seconds, and then show the finished message. The UI remains responsive during the async operation.
* Selecting "Exit" (or pressing q) will close the application.

## **Next Steps**

Congratulations\! You've successfully built a basic interactive CLI application.

Now that you have a feel for the basics, you're ready to explore more advanced features.

➡️ **Next up: [Creating Menus](creating-menus.md)**

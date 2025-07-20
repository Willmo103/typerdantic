# Typerdantic

**Declarative, interactive CLI menus powered by Pydantic.**

Tired of writing clunky command-line interfaces with dozens of flags? Typerdantic lets you build modern, user-friendly, and interactive applications with shockingly little code. By leveraging the power of Pydantic for data validation and structure, you can define your menus as simple Python classes.

---

## Key Features

- **Declarative & Simple**: Define complex menus as Pydantic models. If you know Pydantic, you already know Typerdantic.
- **Interactive by Default**: Get arrow-key navigation, scrolling, and selection out-of-the-box.
- **Async Ready**: Seamlessly run `async` functions as menu actions without blocking the UI.
- **Config-Driven**: Define your entire UI in a TOML file, separating code from presentation.
- **Fully Stylable**: Customize every color and attribute to match your application's brand.

---

## Quick Start

Here's how easy it is to create an interactive menu.

```python
import asyncio
from typerdantic import TyperdanticApp, TyperdanticMenu, MenuItem
from pydantic import Field

class MainMenu(TyperdanticMenu):
    """My Awesome App"""

    say_hello: MenuItem = Field(
        default=MenuItem(
            description="Say Hello",
            action=lambda: print("Hello, world!")
        )
    )
    quit_app: MenuItem = Field(
        default=MenuItem(description="Exit", is_quit=True)
    )

if __name__ == "__main__":
    app = TyperdanticApp(main_menu=MainMenu)
    asyncio.run(app.run())

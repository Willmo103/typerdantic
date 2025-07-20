# src/typerdantic/styles.py

import tomllib
from pathlib import Path
from typing import Dict

from prompt_toolkit.styles import Style

# Define the default style dictionary for the application
DEFAULT_STYLE_DICT: Dict[str, str] = {
    "title": "bold underline",
    "selected": "bg:#0055aa fg:#ffffff bold",
    "menu-item": "",  # Default style for non-selected items
}

# Create the default Style object
DEFAULT_STYLE = Style.from_dict(DEFAULT_STYLE_DICT)


def load_style_from_file(path: Path) -> Style:
    """
    Loads a custom style configuration from a TOML file.

    If the file cannot be found or parsed, it returns the default style.

    Args:
        path: The path to the TOML style file.

    Returns:
        A prompt_toolkit Style object.
    """
    if not path.is_file():
        # Silently fall back to default if no style file is found
        return DEFAULT_STYLE

    try:
        with open(path, "rb") as f:
            custom_style_data = tomllib.load(f)

        # Merge custom styles with defaults, allowing overrides
        merged_styles = DEFAULT_STYLE_DICT.copy()
        if "style" in custom_style_data and isinstance(
            custom_style_data["style"], dict
        ):
            merged_styles.update(custom_style_data["style"])

        return Style.from_dict(merged_styles)
    except (tomllib.TOMLDecodeError, OSError) as e:
        print(f"Warning: Could not load or parse style file '{path}': {e}")
        return DEFAULT_STYLE

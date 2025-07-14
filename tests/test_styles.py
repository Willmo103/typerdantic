# file: tests/test_styles.py

from typerdantic.styles import load_style_from_file, DEFAULT_STYLE_DICT
import sys
import tempfile
import unittest
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


class TestStyles(unittest.TestCase):
    def test_load_default_style_on_missing_file(self):
        """
        Verify that load_style_from_file returns the default style
        when the specified path does not exist.
        """
        print("\nRunning test: Fallback to default on missing file...")
        missing_path = Path("this/path/does/not/exist.toml")
        style = load_style_from_file(missing_path)

        # Convert the list of tuples to a dict for comparison
        style_dict = dict(style.style_rules)
        self.assertEqual(style_dict, DEFAULT_STYLE_DICT)
        print("✓ Test passed")

    def test_load_custom_style_from_file(self):
        """
        Verify that a valid custom style TOML file is loaded and
        merged correctly with the default styles.
        """
        print("\nRunning test: Load valid custom style file...")
        custom_style_content = """
[style]
title = "bold #ff00ff"      # Override default
selected = "bg:#ffff00 #000000" # Override default
new_class = "italic"        # Add a new style class
"""
        with tempfile.NamedTemporaryFile(
            "w", delete=False, suffix=".toml", encoding="utf-8"
        ) as tmp:
            tmp.write(custom_style_content)
            tmp_path = Path(tmp.name)

        try:
            style = load_style_from_file(tmp_path)
            # Convert the list of tuples to a dict for easy lookup
            rules = dict(style.style_rules)

            # Check that styles were overridden and new ones were added
            self.assertEqual(rules.get("title"), "bold #ff00ff")
            self.assertEqual(rules.get("selected"), "bg:#ffff00 #000000")
            self.assertEqual(rules.get("new_class"), "italic")
            # Check that a default style was preserved
            self.assertEqual(rules.get("menu-item"), "")
            print("✓ Test passed")

        finally:
            # Clean up the temporary file
            tmp_path.unlink()

    def test_load_default_on_malformed_file(self):
        """
        Verify that a malformed TOML file causes a fallback to the
        default style without crashing.
        """
        print("\nRunning test: Fallback on malformed style file...")
        malformed_content = "this is not valid toml"
        with tempfile.NamedTemporaryFile(
            "w", delete=False, suffix=".toml", encoding="utf-8"
        ) as tmp:
            tmp.write(malformed_content)
            tmp_path = Path(tmp.name)

        try:
            # This should print a warning but not raise an exception
            style = load_style_from_file(tmp_path)
            # Convert the list of tuples to a dict for comparison
            style_dict = dict(style.style_rules)
            self.assertEqual(style_dict, DEFAULT_STYLE_DICT)
            print("✓ Test passed (Warning is expected)")
        finally:
            tmp_path.unlink()


if __name__ == "__main__":
    print("--- Testing Typerdantic Style System ---")
    unittest.main(verbosity=0)
    print("\nAll style tests passed successfully!")

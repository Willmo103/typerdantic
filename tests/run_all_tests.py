# file: run_all_tests.py

import unittest
import sys
from pathlib import Path


def run_tests():
    """
    Discovers and runs all tests in the 'tests/' directory.
    """
    project_root = Path(__file__).parent
    # Add the src directory to the path to allow imports
    sys.path.insert(0, str(project_root / "src"))
    # Add the project root to find the examples module
    sys.path.insert(0, str(project_root))

    print("--- Discovering and Running All Typerdantic Tests ---")

    loader = unittest.TestLoader()
    # Discover tests in the 'tests' directory, looking for files named 'test_*.py'
    suite = loader.discover(start_dir='tests', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n--- Test Run Complete ---")
    if result.wasSuccessful():
        print("✅ All automated tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ Some automated tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()

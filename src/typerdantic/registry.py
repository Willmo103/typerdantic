# src/typerdantic/registry.py

from typing import Dict, Callable, Any

# A simple dictionary to act as our global action registry.
# The key is the string name (e.g., "backup_database"), and the value is the function.
_ACTION_REGISTRY: Dict[str, Callable[..., Any]] = {}


def register_action(name: str):
    """
    A decorator to register a function as a named internal action.

    Example:
        @register_action("my_cool_action")
        def some_function():
            print("Action running!")
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if name in _ACTION_REGISTRY:
            raise ValueError(f"Action with name '{name}' is already registered.")
        _ACTION_REGISTRY[name] = func
        return func
    return decorator


def get_action(name: str) -> Callable[..., Any] | None:
    """
    Retrieves a registered action function by its name.
    """
    return _ACTION_REGISTRY.get(name)

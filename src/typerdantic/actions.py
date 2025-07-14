# src/typerdantic/actions.py

import asyncio


def simple_action():
    """A simple synchronous function to be called by a menu item."""
    print("\n>>> A simple action was executed!")


async def another_async_action():
    """A simple asynchronous function to test async action handling."""
    print("\n>>> Another async action is running...")
    await asyncio.sleep(1)
    print(">>> Done.")

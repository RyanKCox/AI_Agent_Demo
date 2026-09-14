from typing import Optional

def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting, if name is provided it will be used
    Args:
        name(str, option): The name of the person to greet. Defaults to a generic greeting if not given.

    Returns:
        str: A friendly greeting message
        """
    if name:
        greeting = f"Hello, {name}!"
    else:
        greeting = "Hello There!"
    return greeting
def say_goodbye(name: Optional[str] = None) -> str:
    if name:
        return f"Goodbye, {name}!"
    else :
        return "Goodbye!"
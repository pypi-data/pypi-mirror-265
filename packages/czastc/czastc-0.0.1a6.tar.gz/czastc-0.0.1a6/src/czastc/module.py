"""
Moudule for providing utility functions.
"""
def greet(target) -> str:
    """
    Generate a greeting message for the target.

    Args:
        target: The target of the reeting, can be any object that can
            be printed.

    Returns:
        str: A greeting message for the target.
    """
    return f"Hello, {target}!"

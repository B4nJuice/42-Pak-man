from typing import Any


def is_list_of(obj: list[Any], t: type) -> bool:
    """
    Check whether the list of condition holds.

    Args:
        obj: Obj used by the operation.
        t: Interpolation factor between the two values.

    Returns:
        Whether the operation succeeded or the condition is true.
    """
    return all(isinstance(s, t) for s in obj)

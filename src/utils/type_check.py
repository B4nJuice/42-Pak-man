from typing import Any


def is_list_of(obj: list[Any], t: type) -> bool:
    return all(isinstance(s, t) for s in obj)
from typing import Optional

class weekday(object):
    def __init__(self, weekday: int, n: Optional[int] = ...) -> None: ...

    def __call__(self, n: int) -> weekday: ...

    def __eq__(self, other) -> bool: ...

    def __repr__(self) -> str: ...

    def __hash__(self) -> int: ...

    weekday: int
    n: int

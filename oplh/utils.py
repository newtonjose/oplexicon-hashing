from functools import lru_cache
from typing import TypeVar, Callable

T = TypeVar("T")


Provider = Callable[[], T]


def singleton(constructor: Callable[[], T]) -> Provider[T]:
    @lru_cache
    def init() -> T:
        return constructor()

    return init

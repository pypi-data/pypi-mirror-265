from typing import Iterator, Protocol

from .common import T


class Collectible(Protocol[T]):
    def collect(self) -> list[T]:
        return list(self)

    def next(self) -> T:
        return next(self)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        raise NotImplementedError(f"{self.__class__.__name__}.__next__()")

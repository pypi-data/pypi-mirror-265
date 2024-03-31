from __future__ import annotations

import functools
import itertools
from typing import Callable, Iterable

from . import collectible
from .common import T, U


def create(objects: Iterable[T]) -> Proq[T]:
    return Proq(objects)


class Proq(collectible.Collectible[T]):
    def __init__(self, items: Iterable[T]):
        self.items = iter(items)

    def __next__(self) -> T:
        return next(self.items)

    def append(self, items: Iterable[T]) -> Proq[T]:
        return Proq(itertools.chain(self.items, items))

    def prepend(self, items: Iterable[T]) -> Proq[T]:
        return Proq(itertools.chain(items, self.items))

    def flatten(self: Proq[Iterable[T]]) -> Proq[T]:
        return Proq(itertools.chain(*self.items))

    def map(self, f: Callable[[T], U]) -> Proq[U]:
        return Proq(map(f, self.items))

    def flat_map(self, f: Callable[[T], Iterable[U]]) -> Proq[U]:
        return Proq(itertools.chain(*map(f, self.items)))

    def foreach(self, f: Callable[[T], U]) -> Proq[T]:
        def _foreach(item: T) -> T:
            f(item)
            return item

        return self.map(_foreach)

    def filter(self, f: Callable[[T], bool]) -> Proq[T]:
        return Proq(filter(f, self.items))

    def reduce(self, f: Callable[[T, T], T], initial: T | None = None) -> Proq[T]:
        if initial is None:
            return Proq(functools.reduce(f, self.items) for _ in range(1))
        return Proq(functools.reduce(f, self.items, initial) for _ in range(1))

    def tee(self, n: int = 2) -> tuple[Proq[T], ...]:
        return tuple(Proq(iterator) for iterator in itertools.tee(self.items, n))

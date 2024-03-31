from __future__ import annotations

import enum
import multiprocessing as mp
from typing import Iterable

from . import collectible
from .common import T


class MessageType(enum.Enum):
    Item = 0
    End = 1


class ClosedProqQueueError(RuntimeError):
    pass


class ProqQueue(collectible.Collectible[T]):
    def __init__(self, items: Iterable[T] | None = None):
        self._q: mp.Queue = mp.Queue()
        if items:
            self.fill(items)

    def get(self) -> T:
        message_type, item = self._q.get()
        if message_type == MessageType.End:
            self.close()
            raise ClosedProqQueueError()
        return item

    def fill(self, items: Iterable[T]) -> ProqQueue:
        for item in items:
            self.put(item)
        return self

    def put(self, item: T) -> ProqQueue:
        self._q.put((MessageType.Item, item))
        return self

    def close(self) -> ProqQueue:
        self._q.put((MessageType.End, None))
        return self

    def __next__(self) -> T:
        try:
            return self.get()
        except ClosedProqQueueError:
            raise StopIteration()

from queue import Queue

from .events import Event


class EventQueue:
    """Small process-local FIFO queue for accepted events."""

    def __init__(self) -> None:
        self._queue: Queue[Event] = Queue()

    def enqueue(self, event: Event) -> None:
        self._queue.put(event)

    def dequeue(self) -> Event:
        return self._queue.get_nowait()

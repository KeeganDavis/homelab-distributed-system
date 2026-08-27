from datetime import UTC, datetime
from queue import Empty

import pytest
from drl_backend.events import Event
from drl_backend.in_memory_queue import EventQueue


def make_event(event_id: str, event_type: str) -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"source": "test"},
    )


def test_event_queue_preserves_fifo_order() -> None:
    first = make_event(
        "123e4567-e89b-12d3-a456-426614174000",
        "first",
    )
    second = make_event(
        "123e4567-e89b-12d3-a456-426614174001",
        "second",
    )
    event_queue = EventQueue()

    event_queue.enqueue(first)
    event_queue.enqueue(second)

    assert event_queue.dequeue() == first
    assert event_queue.dequeue() == second


def test_event_queue_raises_empty_when_no_event_is_available() -> None:
    event_queue = EventQueue()

    with pytest.raises(Empty):
        event_queue.dequeue()

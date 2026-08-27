from datetime import UTC, datetime
from queue import Empty

import pytest
from drl_backend.events import Event
from drl_backend.in_memory_queue import EventQueue
from drl_backend.processed_event_store import InMemoryProcessedEventStore
from drl_backend.worker import EventProcessingWorker


def make_event(event_id: str, event_type: str) -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"source": "test"},
    )


def test_process_one_normalizes_stores_and_returns_event() -> None:
    event = make_event(
        "123e4567-e89b-12d3-a456-426614174000",
        " Temperature_Reading ",
    )
    event_queue = EventQueue()
    store = InMemoryProcessedEventStore()
    worker = EventProcessingWorker(event_queue, store)
    event_queue.enqueue(event)

    processed_event = worker.process_one()

    assert processed_event.event_id == event.event_id
    assert processed_event.event_type == "temperature_reading"
    assert processed_event.created_at == event.created_at
    assert processed_event.payload == event.payload
    assert store.list_all() == [processed_event]


def test_process_one_raises_empty_when_queue_has_no_events() -> None:
    worker = EventProcessingWorker(
        EventQueue(),
        InMemoryProcessedEventStore(),
    )

    with pytest.raises(Empty):
        worker.process_one()


def test_run_until_empty_processes_all_queued_events() -> None:
    event_queue = EventQueue()
    store = InMemoryProcessedEventStore()
    worker = EventProcessingWorker(event_queue, store)
    first = make_event(
        "123e4567-e89b-12d3-a456-426614174000",
        "first",
    )
    second = make_event(
        "123e4567-e89b-12d3-a456-426614174001",
        "second",
    )
    event_queue.enqueue(first)
    event_queue.enqueue(second)

    processed_count = worker.run_until_empty()

    assert processed_count == 2
    assert [event.event_type for event in store.list_all()] == [
        "first",
        "second",
    ]

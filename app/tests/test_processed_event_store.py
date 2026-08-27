from datetime import UTC, datetime

from drl_backend.processed_event_store import InMemoryProcessedEventStore
from drl_backend.processed_events import ProcessedEvent


def make_processed_event(event_id: str, event_type: str) -> ProcessedEvent:
    return ProcessedEvent(
        event_id=event_id,
        event_type=event_type,
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"source": "test"},
    )


def test_store_lists_events_in_save_order() -> None:
    first = make_processed_event(
        "123e4567-e89b-12d3-a456-426614174000",
        "first",
    )
    second = make_processed_event(
        "123e4567-e89b-12d3-a456-426614174001",
        "second",
    )
    store = InMemoryProcessedEventStore()

    store.save(first)
    store.save(second)

    assert store.list_all() == [first, second]


def test_store_finds_all_events_with_matching_id() -> None:
    matching_first = make_processed_event(
        "123e4567-e89b-12d3-a456-426614174000",
        "first",
    )
    matching_second = make_processed_event(
        "123e4567-e89b-12d3-a456-426614174000",
        "second",
    )
    other = make_processed_event(
        "123e4567-e89b-12d3-a456-426614174001",
        "other",
    )
    store = InMemoryProcessedEventStore()

    store.save(matching_first)
    store.save(other)
    store.save(matching_second)

    assert store.find_by_event_id(matching_first.event_id) == [
        matching_first,
        matching_second,
    ]


def test_list_all_returns_a_copy_of_the_internal_list() -> None:
    event = make_processed_event(
        "123e4567-e89b-12d3-a456-426614174000",
        "temperature_reading",
    )
    store = InMemoryProcessedEventStore()
    store.save(event)

    returned_events = store.list_all()
    returned_events.clear()

    assert store.list_all() == [event]

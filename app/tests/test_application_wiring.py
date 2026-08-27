from datetime import UTC, datetime

from drl_backend.events import Event
from drl_backend.main import event_queue, event_worker, processed_event_store


def test_application_worker_consumes_application_queue() -> None:
    event = Event(
        event_id="123e4567-e89b-12d3-a456-426614174002",
        event_type=" Application_Test ",
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"source": "application-wiring-test"},
    )
    event_queue.enqueue(event)

    processed_event = event_worker.process_one()

    assert processed_event.event_id == event.event_id
    assert processed_event.event_type == "application_test"
    assert processed_event_store.find_by_event_id(event.event_id) == [
        processed_event,
    ]

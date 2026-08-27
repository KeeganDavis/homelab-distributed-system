from queue import Empty

from drl_backend.main import app, event_queue
from fastapi.testclient import TestClient

client = TestClient(app)

VALID_EVENT = {
    "event_id": "123e4567-e89b-12d3-a456-426614174000",
    "event_type": "temperature_reading",
    "created_at": "2026-08-27T14:00:00Z",
    "payload": {"temperature_c": 21.5},
}


def test_post_events_accepts_valid_event_and_enqueues_it() -> None:
    response = client.post("/events", json=VALID_EVENT)

    assert response.status_code == 202
    assert response.json() == {
        "status": "accepted",
        "event_id": VALID_EVENT["event_id"],
    }

    queued_event = event_queue.dequeue()
    assert str(queued_event.event_id) == VALID_EVENT["event_id"]
    assert queued_event.event_type == VALID_EVENT["event_type"]
    assert queued_event.payload == VALID_EVENT["payload"]


def test_post_events_rejects_invalid_event_without_enqueuing() -> None:
    invalid_event = {
        **VALID_EVENT,
        "event_id": "not-a-uuid",
    }

    response = client.post("/events", json=invalid_event)

    assert response.status_code == 422
    assert response.json()["detail"]

    try:
        event_queue.dequeue()
    except Empty:
        pass
    else:
        raise AssertionError("invalid events must not be enqueued")

from datetime import UTC, datetime

from drl_backend import main
from drl_backend.processed_event_store import InMemoryProcessedEventStore
from drl_backend.processed_events import ProcessedEvent
from fastapi.testclient import TestClient

client = TestClient(main.app)


def make_store() -> InMemoryProcessedEventStore:
    store = InMemoryProcessedEventStore()
    store.save(
        ProcessedEvent(
            event_id="123e4567-e89b-12d3-a456-426614174010",
            event_type="temperature_reading",
            created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
            payload={"temperature_c": 21.5},
        )
    )
    return store


def test_get_processed_events_returns_events_from_the_store(monkeypatch) -> None:
    monkeypatch.setattr(main, "processed_event_store", make_store())

    response = client.get("/processed-events")

    assert response.status_code == 200
    assert response.json() == [
        {
            "event_id": "123e4567-e89b-12d3-a456-426614174010",
            "event_type": "temperature_reading",
            "created_at": "2026-08-27T14:00:00Z",
            "payload": {"temperature_c": 21.5},
            "status": "processed",
        }
    ]


def test_get_processed_events_returns_empty_list_when_store_is_empty(monkeypatch) -> None:
    monkeypatch.setattr(main, "processed_event_store", InMemoryProcessedEventStore())

    response = client.get("/processed-events")

    assert response.status_code == 200
    assert response.json() == []


def test_get_processed_events_filters_by_event_id(monkeypatch) -> None:
    store = make_store()
    matching_event = store.list_all()[0]
    store.save(
        ProcessedEvent(
            event_id="123e4567-e89b-12d3-a456-426614174011",
            event_type="humidity_reading",
            created_at=datetime(2026, 8, 27, 14, 1, tzinfo=UTC),
            payload={"humidity_percent": 45},
        )
    )
    monkeypatch.setattr(main, "processed_event_store", store)

    response = client.get(
        "/processed-events",
        params={"event_id": str(matching_event.event_id)},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "event_id": "123e4567-e89b-12d3-a456-426614174010",
            "event_type": "temperature_reading",
            "created_at": "2026-08-27T14:00:00Z",
            "payload": {"temperature_c": 21.5},
            "status": "processed",
        }
    ]


def test_get_processed_events_returns_empty_list_for_unknown_event_id(monkeypatch) -> None:
    monkeypatch.setattr(main, "processed_event_store", make_store())

    response = client.get(
        "/processed-events",
        params={"event_id": "123e4567-e89b-12d3-a456-426614174099"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_processed_events_rejects_malformed_event_id(monkeypatch) -> None:
    monkeypatch.setattr(main, "processed_event_store", make_store())

    response = client.get(
        "/processed-events",
        params={"event_id": "not-a-uuid"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]

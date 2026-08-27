from datetime import UTC, datetime

from drl_backend.processed_events import ProcessedEvent


def test_processed_event_has_stable_processed_status() -> None:
    processed_event = ProcessedEvent(
        event_id="123e4567-e89b-12d3-a456-426614174000",
        event_type="temperature_reading",
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"temperature_c": 21.5},
    )

    assert processed_event.status == "processed"
    assert processed_event.event_type == "temperature_reading"
    assert processed_event.payload == {"temperature_c": 21.5}


def test_processed_event_rejects_unknown_fields() -> None:
    try:
        ProcessedEvent(
            event_id="123e4567-e89b-12d3-a456-426614174000",
            event_type="temperature_reading",
            created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
            payload={},
            unexpected="value",
        )
    except ValueError as error:
        assert "unexpected" in str(error)
    else:
        raise AssertionError("unknown fields must be rejected")

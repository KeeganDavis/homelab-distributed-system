from datetime import UTC, datetime
from uuid import UUID

import pytest
from drl_backend.events import Event
from pydantic import ValidationError


def test_event_accepts_valid_data() -> None:
    event = Event(
        event_id="123e4567-e89b-12d3-a456-426614174000",
        event_type="temperature_reading",
        created_at="2026-08-27T14:00:00Z",
        payload={"temperature_c": 21.5},
    )

    assert event.event_id == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert event.event_type == "temperature_reading"
    assert event.created_at == datetime(
        2026,
        8,
        27,
        14,
        0,
        tzinfo=UTC,
    )
    assert event.payload == {"temperature_c": 21.5}


def test_event_rejects_invalid_uuid() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="not-a-uuid",
            event_type="temperature_reading",
            created_at="2026-08-27T14:00:00Z",
            payload={"temperature_c": 21.5},
        )


def test_event_rejects_blank_event_type() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="123e4567-e89b-12d3-a456-426614174000",
            event_type="   ",
            created_at="2026-08-27T14:00:00Z",
            payload={"temperature_c": 21.5},
        )


def test_event_rejects_timezone_naive_timestamp() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="123e4567-e89b-12d3-a456-426614174000",
            event_type="temperature_reading",
            created_at="2026-08-27T14:00:00",
            payload={"temperature_c": 21.5},
        )


def test_event_rejects_unexpected_fields() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="123e4567-e89b-12d3-a456-426614174000",
            event_type="temperature_reading",
            created_at="2026-08-27T14:00:00Z",
            payload={"temperature_c": 21.5},
            source="test-generator",
        )
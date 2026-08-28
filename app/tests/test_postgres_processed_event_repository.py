from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import UUID

from drl_backend.postgres_processed_event_repository import (
    PostgresProcessedEventRepository,
)
from drl_backend.processed_events import ProcessedEvent
from psycopg.types.json import Jsonb


def test_save_inserts_processed_event_and_commits() -> None:
    event = ProcessedEvent(
        event_id="123e4567-e89b-12d3-a456-426614174000",
        event_type="temperature_reading",
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"temperature_c": 21.5},
    )
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    repository = PostgresProcessedEventRepository(connection)

    repository.save(event)

    statement, parameters = cursor.execute.call_args.args
    assert " ".join(statement.split()) == (
        "INSERT INTO processed_events "
        "(event_id, event_type, created_at, payload, status) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    assert parameters[:3] == (
        event.event_id,
        event.event_type,
        event.created_at,
    )
    assert isinstance(parameters[3], Jsonb)
    assert parameters[3].obj == event.payload
    assert parameters[4] == event.status
    connection.commit.assert_called_once_with()


def test_list_all_returns_events_in_database_order() -> None:
    first = ProcessedEvent(
        event_id="123e4567-e89b-12d3-a456-426614174000",
        event_type="first",
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"position": 1},
    )
    second = ProcessedEvent(
        event_id="123e4567-e89b-12d3-a456-426614174001",
        event_type="second",
        created_at=datetime(2026, 8, 27, 14, 1, tzinfo=UTC),
        payload={"position": 2},
    )
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        (
            UUID(str(first.event_id)),
            first.event_type,
            first.created_at,
            first.payload,
            first.status,
        ),
        (
            UUID(str(second.event_id)),
            second.event_type,
            second.created_at,
            second.payload,
            second.status,
        ),
    ]
    repository = PostgresProcessedEventRepository(connection)

    assert repository.list_all() == [first, second]

    statement = cursor.execute.call_args.args[0]
    assert " ".join(statement.split()) == (
        "SELECT event_id, event_type, created_at, payload, status "
        "FROM processed_events ORDER BY id"
    )
    connection.commit.assert_not_called()


def test_find_by_event_id_returns_matching_events_in_database_order() -> None:
    event_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    expected = ProcessedEvent(
        event_id=event_id,
        event_type="temperature_reading",
        created_at=datetime(2026, 8, 27, 14, 0, tzinfo=UTC),
        payload={"temperature_c": 21.5},
    )
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        (
            expected.event_id,
            expected.event_type,
            expected.created_at,
            expected.payload,
            expected.status,
        )
    ]
    repository = PostgresProcessedEventRepository(connection)

    assert repository.find_by_event_id(event_id) == [expected]

    statement, parameters = cursor.execute.call_args.args
    assert " ".join(statement.split()) == (
        "SELECT event_id, event_type, created_at, payload, status "
        "FROM processed_events WHERE event_id = %s ORDER BY id"
    )
    assert parameters == (event_id,)
    connection.commit.assert_not_called()
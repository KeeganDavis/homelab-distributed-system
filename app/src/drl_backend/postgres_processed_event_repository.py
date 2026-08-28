from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb

from .processed_events import ProcessedEvent


class PostgresProcessedEventRepository:
    """PostgreSQL-backed persistence for processed events."""

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def save(self, event: ProcessedEvent) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO processed_events
                    (event_id, event_type, created_at, payload, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    event.event_id,
                    event.event_type,
                    event.created_at,
                    Jsonb(event.payload),
                    event.status,
                ),
            )
        self._connection.commit()

    def list_all(self) -> list[ProcessedEvent]:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT event_id, event_type, created_at, payload, status
                FROM processed_events
                ORDER BY id
                """
            )
            rows = cursor.fetchall()

        return [self._to_processed_event(row) for row in rows]

    def find_by_event_id(self, event_id: UUID) -> list[ProcessedEvent]:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT event_id, event_type, created_at, payload, status
                FROM processed_events
                WHERE event_id = %s
                ORDER BY id
                """,
                (event_id,),
            )
            rows = cursor.fetchall()

        return [self._to_processed_event(row) for row in rows]

    @staticmethod
    def _to_processed_event(row: tuple[Any, ...]) -> ProcessedEvent:
        event_id, event_type, created_at, payload, status = row
        return ProcessedEvent(
            event_id=event_id,
            event_type=event_type,
            created_at=created_at,
            payload=payload,
            status=status,
        )
from uuid import UUID

from .processed_events import ProcessedEvent


class InMemoryProcessedEventStore:
    """Process-local store for events produced by the worker."""

    def __init__(self) -> None:
        self._events: list[ProcessedEvent] = []

    def save(self, event: ProcessedEvent) -> None:
        self._events.append(event)

    def list_all(self) -> list[ProcessedEvent]:
        return list(self._events)

    def find_by_event_id(self, event_id: UUID) -> list[ProcessedEvent]:
        return [event for event in self._events if event.event_id == event_id]

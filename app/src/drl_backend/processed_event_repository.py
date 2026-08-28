from typing import Protocol
from uuid import UUID

from .processed_events import ProcessedEvent


class ProcessedEventRepository(Protocol):
    """Read-model persistence boundary for processed events."""

    def save(self, event: ProcessedEvent) -> None: ...

    def list_all(self) -> list[ProcessedEvent]: ...

    def find_by_event_id(self, event_id: UUID) -> list[ProcessedEvent]: ...
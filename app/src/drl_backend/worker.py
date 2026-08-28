from queue import Empty

from .events import Event
from .in_memory_queue import EventQueue
from .processed_event_repository import ProcessedEventRepository
from .processed_events import ProcessedEvent


class EventProcessingWorker:
    """Consumes queued events and stores their processed representations."""

    def __init__(
        self,
        event_queue: EventQueue,
        processed_event_store: ProcessedEventRepository,
    ) -> None:
        self._event_queue = event_queue
        self._processed_event_store = processed_event_store

    def process_one(self) -> ProcessedEvent:
        event: Event = self._event_queue.dequeue()
        processed_event = ProcessedEvent(
            event_id=event.event_id,
            event_type=event.event_type.strip().lower(),
            created_at=event.created_at,
            payload=event.payload,
        )
        self._processed_event_store.save(processed_event)
        return processed_event

    def run_until_empty(self) -> int:
        processed_count = 0

        while True:
            try:
                self.process_one()
            except Empty:
                return processed_count

            processed_count += 1

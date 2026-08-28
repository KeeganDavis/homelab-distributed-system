import logging
from uuid import UUID

from fastapi import FastAPI, status

from .events import Event
from .in_memory_queue import EventQueue
from .logging_config import configure_logging
from .processed_event_repository import ProcessedEventRepository
from .processed_event_store import InMemoryProcessedEventStore
from .processed_events import ProcessedEvent
from .worker import EventProcessingWorker

configure_logging()
logger = logging.getLogger(__name__)
event_queue = EventQueue()
processed_event_store: ProcessedEventRepository = InMemoryProcessedEventStore()
event_worker = EventProcessingWorker(event_queue, processed_event_store)

app = FastAPI(
    title="Distributed Reliability Lab Backend",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}


@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
def ingest_event(event: Event) -> dict[str, str | UUID]:
    event_queue.enqueue(event)
    logger.info(
        "Event accepted event_id=%s event_type=%s",
        event.event_id,
        event.event_type,
    )

    return {
        "status": "accepted",
        "event_id": event.event_id,
    }


@app.get("/processed-events", response_model=list[ProcessedEvent])
def list_processed_events(event_id: UUID | None = None) -> list[ProcessedEvent]:
    """Return the processed events currently held by the read store."""
    if event_id is None:
        processed_events = processed_event_store.list_all()
    else:
        processed_events = processed_event_store.find_by_event_id(event_id)

    logger.debug(
        "Processed-event query returned count=%d event_id=%s",
        len(processed_events),
        event_id,
    )
    return processed_events

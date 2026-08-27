import logging
from uuid import UUID

from fastapi import FastAPI, status

from .events import Event
from .in_memory_queue import EventQueue
from .logging_config import configure_logging
from .processed_event_store import InMemoryProcessedEventStore
from .worker import EventProcessingWorker

configure_logging()
logger = logging.getLogger(__name__)
event_queue = EventQueue()
processed_event_store = InMemoryProcessedEventStore()
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

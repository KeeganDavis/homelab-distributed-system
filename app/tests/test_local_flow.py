import json
import socket
import threading
import time
from urllib.request import urlopen

import pytest
import uvicorn
from drl_backend import main
from drl_backend.generator import create_synthetic_event, send_event
from drl_backend.in_memory_queue import EventQueue
from drl_backend.processed_event_store import InMemoryProcessedEventStore
from drl_backend.worker import EventProcessingWorker


@pytest.fixture
def local_api(monkeypatch):
    event_queue = EventQueue()
    processed_event_store = InMemoryProcessedEventStore()
    monkeypatch.setattr(main, "event_queue", event_queue)
    monkeypatch.setattr(main, "processed_event_store", processed_event_store)
    monkeypatch.setattr(
        main,
        "event_worker",
        EventProcessingWorker(event_queue, processed_event_store),
    )

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen()
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(main.app, log_level="warning"))
    server_thread = threading.Thread(
        target=server.run,
        kwargs={"sockets": [listener]},
        daemon=True,
    )
    try:
        server_thread.start()

        for _ in range(100):
            if server.started:
                break
            time.sleep(0.01)
        else:
            raise RuntimeError("Local API did not start")

        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        if server_thread.is_alive():
            server_thread.join(timeout=5)
        if listener.fileno() != -1:
            listener.close()


def test_local_flow_sends_processes_and_queries_an_event(local_api) -> None:
    event = create_synthetic_event()

    ingestion_response = send_event(local_api, event)

    assert ingestion_response == {
        "status": "accepted",
        "event_id": str(event.event_id),
    }
    assert main.event_worker.run_until_empty() == 1

    with urlopen(f"{local_api}/processed-events?event_id={event.event_id}") as response:
        processed_events = json.load(response)

    assert processed_events == [
        {
            **event.model_dump(mode="json"),
            "event_type": "temperature_reading",
            "status": "processed",
        }
    ]

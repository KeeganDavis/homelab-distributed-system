# Phase 3, Chunk 5: Synthetic Generator and Local Flow

## Delivered

- Added a synthetic event generator that creates one valid temperature-reading
  event with a new UUID and UTC timestamp.
- Added a generator CLI: `python -m drl_backend.generator`. Its optional
  `--api-url` argument defaults to `http://127.0.0.1:8000`.
- The generator sends events only through `POST /events`; it does not access
  the queue, worker, or processed-event store directly.
- Added focused generator tests and a local end-to-end test using real
  localhost HTTP.

## Local flow behavior

The verified local sequence is:

```text
generator --POST /events--> in-memory queue
manual worker step -------> processed-event store
query API --GET /processed-events?event_id=...--> processed event
```

The end-to-end test starts the existing FastAPI application on a temporary
localhost port. It sends an event with the generator, explicitly calls
`event_worker.run_until_empty()`, and queries the processed event by ID. The
result retains the event ID, timestamp, and payload, while the worker
normalizes `" Temperature_Reading "` to `"temperature_reading"`.

## Verification

From the repository root:

```bash
python -m pytest app/tests/test_local_flow.py -q
python -m pytest -q
```

Result: the local-flow test passed, and the complete suite passed with 27
tests.

The generator CLI interface was also verified without sending an event:

```bash
python -m drl_backend.generator --help
```

## Limitations and boundaries

The queue and processed-event store are intentionally process-local and held
only in memory. The automated local-flow test therefore keeps the FastAPI
application and explicitly invoked worker in the same Python process, though
the generator and query operations use real localhost HTTP.

A separately launched worker process would have a different, empty in-memory
queue; this local flow is not a production multi-process architecture. Events
and processed results are lost on restart. Kafka, PostgreSQL, persistence,
retries, background worker startup, authentication, monitoring, and deployment
configuration remain deferred.

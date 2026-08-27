# Phase 3, Chunk 2: Ingestion API

## Delivered

- Added a process-local FIFO `EventQueue` boundary.
- Added `POST /events` using the shared `Event` model for validation.
- Valid events return `202 Accepted` with their stable `event_id`.
- Invalid requests return FastAPI validation errors with status `422`.
- Added focused queue and ingestion API tests.

## Verification

```bash
python -m pytest -q
```

Result: 10 tests passed.

## Limitations and Boundaries

The queue is in memory and process-local; events are lost on restart. Kafka,
persistence, deduplication, retries, workers, query behavior, and the
synthetic generator remain deferred to later chunks or phases.

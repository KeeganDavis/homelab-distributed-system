# Phase 3, Chunk 3: Processing Worker

## Delivered

- Added a `ProcessedEvent` model for the worker's output.
- Added an `InMemoryProcessedEventStore` boundary for processed events.
- Added an `EventProcessingWorker` that consumes events from the existing
  process-local FIFO queue.
- Connected the application-owned queue, worker, and processed-event store in
  `main.py`.
- Added focused model, store, worker, and application-wiring tests.

## Processing behavior

For each queued `Event`, `process_one()`:

1. Dequeues one event.
2. Normalizes `event_type` with `strip().lower()`.
3. Preserves the event ID, creation timestamp, and payload.
4. Creates a `ProcessedEvent` with `status="processed"`.
5. Saves the result in the in-memory store and returns it.

The transformation is deterministic and intentionally small so the worker's
behavior is easy to observe and test.

## Worker lifecycle

The worker is manually controlled:

- `process_one()` handles exactly one event. If the queue is empty, it raises
  `queue.Empty`.
- `run_until_empty()` repeatedly processes events until the queue is empty and
  returns the number of processed events.

There is no background thread, service manager, retry loop, or automatic worker
startup yet.

## Boundaries and limitations

The queue and processed-event store are process-local and in memory. Events and
processed results are lost when the process exits. The store preserves insertion
order and does not perform deduplication. Kafka, PostgreSQL, Redis, retries,
authentication, persistence, and deployment configuration remain deferred.

The query API is also deferred to Phase 3, Chunk 4. It will consume the store
through a separate read boundary rather than having the worker expose HTTP
behavior.

## Verification

From the repository root:

```bash
python -m pytest -q
```

Result: 19 tests passed.

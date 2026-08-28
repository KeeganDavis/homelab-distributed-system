# Phase 3, Chunk 4: Query API

## Delivered

- Added `GET /processed-events` for reading processed events.
- Added optional `event_id` filtering through the query string.
- Returned the existing `ProcessedEvent` model as a JSON array.
- Connected the API to the application-owned processed-event store rather than
  coupling it to the worker implementation.
- Added focused tests for listing, filtering, empty results, and invalid IDs.

## Query behavior

The endpoint supports two request forms:

```text
GET /processed-events
GET /processed-events?event_id=<uuid>
```

Without `event_id`, the API calls `processed_event_store.list_all()` and
returns all processed events in store order. With a valid `event_id`, it calls
`processed_event_store.find_by_event_id()` and returns the matching events.

Both an empty store and a valid lookup with no matches return `200 OK` with an
empty JSON array:

```json
[]
```

FastAPI validates the optional query parameter as a UUID. A malformed value
returns `422 Unprocessable Entity` before the endpoint calls the store.

## Application boundary

The worker owns processing and writing results to the store. The query API owns
HTTP request handling and reads only through the store's public methods. This
keeps the HTTP layer independent from the worker lifecycle and leaves a clear
boundary for replacing the in-memory store with a PostgreSQL read model later.

## Limitations

The processed-event store remains process-local and in memory. Results are lost
when the process exits. There is no persistence, pagination, authentication,
deduplication, retry behavior, background worker startup, or PostgreSQL
integration. The synthetic generator and local end-to-end flow remain deferred
to Phase 3, Chunk 5.

## Verification

From the repository root:

```bash
python -m pytest -q
```

Result: 24 tests passed.

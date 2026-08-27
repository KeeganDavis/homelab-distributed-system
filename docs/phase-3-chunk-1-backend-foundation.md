# Phase 3, Chunk 1: Backend Foundation

## Delivered

- Python package layout under `app/src/drl_backend` with tests under `app/tests`.
- Project and dependency configuration in `pyproject.toml`.
- Environment-backed `APP_ENV` and `LOG_LEVEL` settings.
- Standard-library application logging.
- FastAPI application with `GET /health` returning `{"status": "ok"}`.
- Shared Pydantic `Event` model and validation tests.

## Event Contract

`Event` requires:

- `event_id`: UUID; stable across retries and suitable for future deduplication.
- `event_type`: non-blank string, 1-100 characters.
- `created_at`: timezone-aware datetime.
- `payload`: JSON-like object; may be empty.

Unexpected top-level fields are rejected. Uniqueness enforcement and idempotent
processing are not implemented yet.

## Verification

```bash
python -m pytest -q
```

Current result: 6 tests passed without warnings.

## Boundaries

Kafka, PostgreSQL, Redis, OTel, ingestion, workers, query behavior, and
generator behavior remain deferred. Chunk 2 will introduce `POST /events`.

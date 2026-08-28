# Phase 4, Chunk 1: PostgreSQL Foundation

## Outcome

Chunk 1 is complete and verified. PostgreSQL 16 runs on `drl-ops-01` and the
application has a PostgreSQL repository implementation without changing the
runtime worker or query API from their in-memory store.

## Verified database foundation

- Database: `drl`
- Application role: `drl_app`, a login role without administrative privileges
- Credential handling: the password was set interactively and is not stored in
  the repository
- Table: `processed_events`
- Lookup: a non-unique B-tree index on `event_id`

The table stores the existing `ProcessedEvent` fields: event ID, normalized
event type, timezone-aware creation time, JSON payload, and processed status.
A database-generated identity key preserves insertion order and permits the
same duplicate-event-ID behavior as the in-memory store.

Manual verification as `drl_app` confirmed TCP password authentication, one
insert, and an event-ID lookup. The PostgreSQL service was `online` on port
5432 during verification.

## Application boundary

`ProcessedEventRepository` defines `save`, `list_all`, and `find_by_event_id`.
`PostgresProcessedEventRepository` uses Psycopg 3, parameterized SQL, `JSONB`
adaptation, explicit commits for writes, and a row-to-`ProcessedEvent` mapper.
The existing in-memory store remains the runtime implementation.

Verification: `python -m pytest -q` completed with 30 passing tests, including
three focused PostgreSQL repository tests.

## Limits and next work

Kafka, Redis, Docker, runtime PostgreSQL wiring, remote PostgreSQL exposure,
and migrations were not added. The next Phase 4 chunk is Kafka KRaft
foundation and requires an explicit user decision.

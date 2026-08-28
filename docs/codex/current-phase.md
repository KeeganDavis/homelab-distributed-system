# Current Project State

## Current Phase

Phase 3: Backend Application - complete.

Phase 4: Data and Messaging - in progress; Chunk 1 complete.

See the [Phase 3 definition](../project-plan.md#phase-3-backend-application)
and [Phase 4 definition](../project-plan.md#phase-4-data-and-messaging) in the
project plan.

## Current Objective

Phase 3's intentionally small backend application is complete and verified.
Phase 4 Chunk 1 established and verified the PostgreSQL foundation on
`drl-ops-01`: PostgreSQL 16, the `drl` database, the least-privilege
`drl_app` role, the processed-event schema, and a tested repository boundary.
Kafka, Redis, and runtime application integration have not started. The Phase 2
server criteria remain deferred by explicit user decision.

## Phase 0 Completion

Phase 0: Repository Foundation is complete.

Completed outcomes:

- Repository directory scaffold established with Git placeholders.
- Project plan, environment notes, current-phase tracking, and task template added.
- Architecture overview and ADR guidance added.
- Repository guidance and pull request workflow established.
- Phase 0 documentation and repository structure manually reviewed.

## Phase 1 Completion

Phase 1: Virtual Infrastructure is complete.

Completed outcomes:

- Microsoft Hyper-V is enabled and verified on the Windows 11 host.
- The approved Internal switch, private subnet, static VM inventory, and
  host/guest name-resolution design are implemented.
- Four Ubuntu Server 24.04.3 Generation 2 VMs exist with their approved
  hostnames, static addresses, storage paths, 2 vCPU, and fixed 4 GB memory.
- Windows-host SSH access, guest-side name resolution, and the baseline UFW
  policy were verified, including the intended blocked guest-to-guest SSH paths.
- Reboot verification and final handoff documentation were completed.

Source documents: [docs/environment.md](../environment.md), [Phase 1 virtual
infrastructure runbook](../../runbooks/phase-1-virtual-infrastructure.md), and
[ADR 001](../../architecture/adr/001-hyper-v-lab-network.md).

Status: complete.
## Phase 2 Summary

The Phase 2 canary learning milestone is complete for `drl-ops-01`. Chunks 1
through 4 were performed and verified on the canary, and Chunk 5 documented the
manual procedures, observations, limitations, and future automation candidates.
The detailed evidence remains in the [Phase 2 Chunk 1 runbook](../../runbooks/phase-2-chunk-1-operating-model-and-baseline.md),
[Chunk 2 runbook](../../runbooks/phase-2-chunk-2-identity-and-access.md),
[Chunk 3 runbook](../../runbooks/phase-2-chunk-3-system-operations.md), and
[Chunk 4 runbook](../../runbooks/phase-2-chunk-4-networking-and-resource-monitoring.md).

The control plane and both workers were not manually updated or verified for
the deferred Phase 2 Chunk 2 and Chunk 3 work. The user has explicitly chosen
to begin Phase 3 before those requirements are satisfied.

The deferred work must be completed during the future Phase 7 Ansible phase.
All four servers must be updated and verified, including the deferred identity,
access, and system-operations procedures, before the Ansible phase can be
considered complete. At that point the outstanding Phase 2 requirements can be
reviewed and marked satisfied.

## Current Chunk

Phase 4, Chunk 1: PostgreSQL foundation and data model - complete and
verified. Do not begin Chunk 2 without an explicit user decision.

## Phase 3 Completion

Phase 3: Backend Application is complete.

Completed outcomes:

- Created the Python/FastAPI project foundation, health endpoint, shared event
  contract, configuration, and logging.
- Added `POST /events` and an application-owned process-local FIFO queue.
- Added a manually controlled worker that normalizes event types and saves
  processed events to an in-memory store.
- Added `GET /processed-events`, including optional event-ID filtering.
- Added a synthetic generator and verified the local
  ingestion-to-processing-to-query flow using localhost HTTP.

Verification: 27 tests passed with `python -m pytest -q`.

Source documentation:

- [Chunk 2: Ingestion API](../phase-3-chunk-2-ingestion-api.md)
- [Chunk 3: Processing Worker](../phase-3-chunk-3-processing-worker.md)
- [Chunk 4: Query API](../phase-3-chunk-4-query-api.md)
- [Chunk 5: Synthetic Generator and Local Flow](../phase-3-chunk-5-synthetic-generator-and-local-flow.md)

The Phase 3 queue and processed-event store are intentionally process-local and
in memory. They are learning-stage adapters, not a production multi-process
design.

## Phase 4 Plan: Data and Messaging

Status: in progress; Chunk 1 complete. Chunks 2 through 5 have not started.

Phase 4 will replace the learning-stage in-memory boundaries in small,
verifiable steps. Redis is not planned as a default component: it will be
introduced only if a concrete caching or temporary-state requirement is
identified.

### Chunk 1: PostgreSQL foundation and data model

Install and operate PostgreSQL manually, define the smallest processed-event
schema, and add a narrowly scoped repository boundary with focused tests.
Verify connectivity, schema creation, and persistence independently of Kafka.

Status: complete and verified. See the
[Chunk 1 record](../phase-4-chunk-1-postgresql-foundation.md).

### Chunk 2: Kafka KRaft foundation

Install and operate a single local Kafka broker in KRaft mode. Create and
inspect an event topic, then practice producer and consumer commands before
connecting application code. Verify topics, partitions, records, and offsets.

### Chunk 3: Ingestion producer integration

Replace only the ingestion API's in-memory queue handoff with a Kafka producer.
Keep the existing event contract and request behavior where possible. Verify an
accepted request produces one record in the intended topic.

### Chunk 4: Worker consumer and PostgreSQL read model

Replace the worker's in-memory queue consumption with a Kafka consumer and
write processed events through the PostgreSQL repository boundary. Update the
query API to read from PostgreSQL. Verify consumer-group and offset behavior,
worker normalization, durable results, and query results after a restart.

### Chunk 5: Delivery behavior and end-to-end verification

Exercise and document partitions, offsets, consumer groups, backpressure,
retry behavior, and idempotency limits using controlled local scenarios. Verify
the complete generator-to-query flow and document operational procedures,
limitations, and deferred work.

Each Phase 4 chunk is a learning and verification checkpoint. Do not begin a
later chunk until its predecessor is verified.

## Later Phases Not Started

- Redis
- Docker
- Jenkins
- Ansible
- Terraform / Floci
- Kubernetes
- Observability
- Reliability engineering
- External API
- Real AWS validation

## Phase 2 Status

Status: canary milestone complete; full criteria deferred until the future
Ansible phase. The four-server identity/access and system-operations rollout
and verification remain outstanding. Phase 2 will be considered satisfied only
after all four servers are updated and verified during that Ansible work.

## Current Constraints

- Host: Windows 11
- CPU: Intel Core i7-9700K
- RAM: 32 GB
- GPU: RTX 2070 Super
- Multiple local drives available
- Resource usage should remain reasonable for concurrent desktop use

## Phase Advancement

Phase 3 is complete and Phase 4 Chunk 1 is complete. Starting any later
Phase 4 chunk requires an explicit user decision. The documented Phase 2 gaps
remain open and must not be represented as completed. Before the future Ansible
phase is closed, all four servers must receive and pass the deferred Phase 2
updates and verification.

# Current Project State

## Current Phase

Phase 3: Backend Application - starting

See the [Phase 3 definition in the project plan](../project-plan.md#phase-3-backend-application).

## Current Objective

Build the intentionally small backend application: a synthetic event generator,
FastAPI ingestion API, processing worker, and query API. Phase 3 is starting by
explicit user decision even though the full Phase 2 server criteria remain
deferred.

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

Phase 3: Backend Application - starting.

## Future Work Not Started

- Kafka
- PostgreSQL / Redis
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

Phase 3 is starting by explicit user decision while the documented Phase 2
gaps remain open. Those gaps must not be represented as completed. Before the
future Ansible phase is closed, all four servers must receive and pass the
deferred Phase 2 updates and verification.

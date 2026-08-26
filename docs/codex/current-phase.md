# Current Project State

## Current Phase

Phase 2: Linux Administration

See the [Phase 2 definition in the project plan](../project-plan.md#phase-2-linux-administration).

## Current Objective

Phase 1 is complete. Phase 2 will manually establish Linux administration
fundamentals across the existing Ubuntu VMs using a production-shaped workflow:
baseline, plan, canary change, verification, controlled rollout, and
documentation. Automation will be considered only after the corresponding
manual procedure is understood and verified.

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
## Phase 2 Work Breakdown

Phase 2 goal: configure all four servers manually once, verify the results, and
then use the lessons learned to guide later automation. Keep the work practical:
make a change, verify it, and break and recover something when the concept is
understood.

### Chunk 1: Baseline and safe change workflow

- Capture a simple baseline for all four servers.
- Define the access model, recovery path, canary server, and rollout order.
- Use pre-change checks, one-server changes, verification, and recorded results.

Verification: the baseline and change workflow are understood before server
configuration begins.

### Chunk 2: Identity and access

- Configure users/groups, sudo, permissions, environment variables, and
  SSH keys.
- Apply least privilege and preserve a known-good console or SSH recovery path.

Verification: permitted and denied access behaves as intended on all four
servers, including after reboot.

### Chunk 3: System operations

- Practice package management, systemd, journald, filesystem and storage
  inspection, log rotation, and cron/systemd timers.
- Make small, observable changes and verify service, log, storage, and schedule
  behavior.

Verification: the system state and operational changes are understood and
repeatable on all four servers.

### Chunk 4: Networking and resource monitoring

- Verify network identity, listening services, firewall rules, and required or
  prohibited traffic.
- Monitor CPU, memory, load, disk capacity, processes, services, and recent
  errors.

Verification: the servers remain reachable and secure, and abnormal resource or
network behavior can be identified from evidence.

### Chunk 5: Break, recover, and document

- Introduce one controlled failure at a time after the manual configuration is
  stable.
- Investigate from symptom to evidence, recovery, and prevention.
- Document the manual procedures and identify what is ready for later
  automation.

Verification: at least one failure is recovered successfully, the manual
workflow is documented, and the Phase 2 completion criteria are met.

## Phase 2 Working Method

For each chunk, use this simple production-shaped loop:

1. Make the smallest change on drl-ops-01 first.
2. Verify the change, including reboot behavior when relevant.
3. Roll out the verified change to the other three servers.
4. Record what changed, what was observed, and how to recover it.

Use least privilege, do not commit secrets, keep a recovery path open, and stop
to investigate unexpected results. Manual configuration comes first; automation
comes after the procedure is understood and verified.

## Current Chunk

Chunk 1: Baseline and safe change workflow - Verified complete.

The baseline and change-control verification gate passed. The documented
operating model and baseline are recorded in the [Phase 2 Chunk 1 operating
model and baseline runbook](../../runbooks/phase-2-chunk-1-operating-model-and-baseline.md).
Chunk 2 has not started; do not begin it until the user explicitly decides to
advance.

## Not Started

- Phase 2 Chunks 2-5
- Backend application
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

## Phase 2 Completion Criteria

Phase 2 is complete when:

- Users, groups, sudo, permissions, environment variables, and SSH keys are
  manually configured and verified on all four servers.
- Package management, systemd, journald, filesystem/storage, log rotation, and
  cron or systemd timers are manually practiced and verified.
- Firewall behavior and resource monitoring are understood and verified.
- At least one controlled failure is investigated, recovered, and documented.
- The manual procedures, security decisions, known limitations, and future
  automation candidates are documented.

Status: started. These criteria will be evaluated as the five Phase 2
chunks are completed and verified.

## Current Constraints

- Host: Windows 11
- CPU: Intel Core i7-9700K
- RAM: 32 GB
- GPU: RTX 2070 Super
- Multiple local drives available
- Resource usage should remain reasonable for concurrent desktop use

## Phase Advancement

Do not advance to Phase 3 until all Phase 2 chunks are verified, the Linux
failure labs and handoff documentation are complete, and the user explicitly
decides to proceed.

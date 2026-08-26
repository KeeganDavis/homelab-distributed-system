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
repeatable on the verified canary, with fleet-wide completion still
outstanding.

### Chunk 4: Networking and resource monitoring

- Verify network identity, listening services, firewall rules, and required or
  prohibited traffic.
- Monitor CPU, memory, load, disk capacity, processes, services, and recent
  errors.

Verification: the servers remain reachable and secure, and abnormal resource or
network behavior can be identified from evidence.

### Chunk 5: Document

- Document the manual procedures and identify what is ready for later
  automation.

Verification: The manual workflow, results, known limitations, and future
automation candidates are documented; the Phase 2 completion criteria are then
reviewed.

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

Chunk 3: System operations - Verified complete for `drl-ops-01` canary scope.

Chunk 1 is verified complete. Its documented operating model and baseline are
recorded in the [Phase 2 Chunk 1 operating model and baseline runbook](../../runbooks/phase-2-chunk-1-operating-model-and-baseline.md).

The `drl-ops-01` canary identity and access procedure is verified. The canary
now has the documented `drladmin`, `drlread`, and `drl-operators` model;
unnecessary `lxd` membership was removed from `opsadmin`; key-only SSH,
password-required sudo, controlled directory permissions, environment
variables, and post-reboot behavior were verified. The manual canary record is
in the [Phase 2 Chunk 2 identity and access runbook](../../runbooks/phase-2-chunk-2-identity-and-access.md).

Scope amendment approved by the user on 2026-08-26: close Chunk 2 for the
current manual learning milestone after the canary verification. Defer the
rollout to `drl-k8s-cp-01`, `drl-k8s-wk-01`, and `drl-k8s-wk-02` to the future
Ansible phase. The deferred fleet rollout must not be described as manually
configured or verified, and the original Phase 2 criterion requiring all four
servers remains outstanding until that future work is completed.

The `drl-ops-01` canary system-operations procedure is verified. Package
management, systemd, journald, filesystem and LVM inspection, logrotate, cron,
and systemd timer behavior were manually inspected and recorded. The canary
record is in the [Phase 2 Chunk 3 system operations runbook](../../runbooks/phase-2-chunk-3-system-operations.md).
The other three VMs were not changed or verified for Chunk 3, so the original
all-four-server criterion remains outstanding.

## Not Started

- Phase 2 Chunk 4
- Phase 2 Chunk 5 documentation and handoff
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

## Deferred from the current manual milestone

- Fleet-wide Phase 2 Chunk 2 identity and access rollout, including
  post-reboot verification on the control plane and workers; planned for the
  future Ansible phase.
- Phase 2 Chunk 3 system-operations rollout and verification on the control
  plane and workers; not included in the canary milestone.

## Phase 2 Completion Criteria

Phase 2 is complete when:

- Users, groups, sudo, permissions, environment variables, and SSH keys are
  manually configured and verified on all four servers.
- Package management, systemd, journald, filesystem/storage, log rotation, and
  cron or systemd timers are manually practiced and verified.
- Firewall behavior and resource monitoring are understood and verified.
- The manual procedures, system-operation results, security decisions, known
  limitations, and future automation candidates are documented.

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

Do not advance to Phase 3 until all Phase 2 chunks are verified, the handoff
documentation is complete, and the user explicitly decides to proceed.

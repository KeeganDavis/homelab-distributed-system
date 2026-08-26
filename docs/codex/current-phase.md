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

Phase 2 follows the Linux Administration scope in the project plan. Each chunk
must be completed on a canary VM first, verified with evidence, and then applied
to the remaining VMs when the change is safe to roll out. Record the commands,
observations, deviations, and rollback or recovery steps as the work proceeds.

### Chunk 1: Operating model and baseline capture

- Define the administrative account, group, privilege, and access model before
  changing users or sudo.
- Establish the change workflow: pre-change checks, one-VM canary, verification
  gate, rollout order, rollback point, and post-change evidence.
- Capture a baseline for hostname, IP, routes, users, groups, privileges,
  packages, services, processes, storage, mounts, memory, CPU, and logs.
- Decide how Hyper-V checkpoints or other recovery points will be used as a
  learning aid; do not treat a checkpoint as a production backup.

Verification: the baseline is captured for all four VMs, the intended change
scope is written down, and the canary and rollout order are approved before
configuration changes begin.

Status: ready to begin. No Phase 2 configuration changes have been made.

### Chunk 2: Users, groups, permissions, and sudo

- Implement the approved least-privilege account and group model.
- Practice ownership, modes, umask, ACL awareness, and permission diagnosis.
- Configure and verify narrowly scoped sudo access without locking out the
  existing administrative path.
- Test both permitted and denied operations using separate sessions or test
  accounts where appropriate.

Verification: account and group membership are correct, privileged and
unprivileged actions behave as designed, file access tests pass, and the
original recovery/admin path remains available.

### Chunk 3: SSH administration and hardening

- Establish key-based SSH access from the Windows administrative host without
  committing private keys or passwords.
- Preserve a second known-good session or console path during changes.
- Review effective sshd configuration, authentication behavior, service state,
  and the existing UFW source restriction.
- Apply only approved hardening changes, then verify both successful access and
  rejected access.

Verification: key-based administrative access works to every intended VM,
unapproved authentication or source paths are rejected as designed, and a
reboot does not remove access.

### Chunk 4: Packages and update management

- Learn apt repository, cache, package installation, removal, upgrade, and
  held-package behavior.
- Establish a documented update procedure with pre-change and post-change
  package inventory.
- Identify services that require restart after updates and verify them.
- Do not introduce unattended upgrades or a new patching policy without first
  documenting the choice and its tradeoffs.

Verification: a controlled package change succeeds on the canary, package
state is recorded before and after, required services remain healthy, and the
same procedure can be repeated without unexplained errors.

### Chunk 5: Processes and systemd

- Inspect processes, parent/child relationships, signals, priorities, and
  resource use.
- Learn systemd unit status, dependencies, enablement, restart behavior, and
  failure reporting.
- Practice a controlled service lifecycle change and document its impact.
- Use journal and service evidence rather than assuming a process is healthy
  because it exists.

Verification: process and systemd checks identify the expected state, a
controlled stop/start or restart is recovered and verified, and the procedure
has a documented rollback or recovery path.

### Chunk 6: Journald and log rotation

- Inspect logs with journalctl by boot, unit, priority, time, and failure.
- Decide and document the learning-lab journal persistence and retention
  settings.
- Learn logrotate configuration, rotation triggers, permissions, compression,
  and retention.
- Generate a controlled test event and verify that it is discoverable and
  handled according to the documented policy.

Verification: required service and system events can be located, journal and
rotated-log retention is understood, and no log policy change causes loss of
the evidence needed for troubleshooting.

### Chunk 7: Storage and filesystems

- Inventory block devices, partitions, filesystems, mounts, UUIDs, and free
  space without changing the approved VM disks accidentally.
- Practice safe directory, mount, ownership, and capacity checks.
- Learn how to identify disk pressure and inode pressure and how to recover
  from a controlled test condition.
- Document what is persistent across reboot and what is temporary.

Verification: storage and filesystem state is understood on every VM, mount
and capacity checks produce expected results after reboot, and any test change
has a documented recovery procedure.

### Chunk 8: Networking and firewall operations

- Inspect interfaces, addresses, routes, neighbor state, name resolution, and
  listening sockets.
- Reconfirm the approved Phase 1 network identity before making changes.
- Practice a controlled UFW rule lifecycle, including ordering, source
  restriction, logging, verification, and rollback.
- Test required administrative traffic and prohibited traffic from the
  correct source systems.

Verification: no address or route drift exists, required SSH access works,
prohibited traffic remains blocked, and firewall changes are explainable from
the resulting rules and connection evidence.

### Chunk 9: Resource monitoring and operational checks

- Build a lightweight recurring check for CPU, memory, load, disk capacity,
  inode use, network state, processes, services, and recent errors.
- Capture normal resource observations for the four-VM desktop-constrained
  environment.
- Define symptoms that should trigger investigation rather than automatic
  remediation.
- Practice comparing current state with the captured baseline.

Verification: resource and health checks produce repeatable evidence, normal
behavior is documented, and abnormal results lead to an investigation path.

### Chunk 10: Linux failure labs and Phase 2 handoff

- Introduce one controlled Linux failure at a time after the preceding chunks
  are stable, such as a stopped service, a bad permission, log growth, or a
  deliberately incorrect firewall rule.
- Investigate from symptom to evidence, hypothesis, root cause, mitigation,
  recovery verification, and prevention.
- Record the exercise as an incident or troubleshooting document without
  revealing the fault before investigation.
- Consolidate verified procedures into runbooks and identify which procedures
  are ready for later automation.

Verification: each failure lab has an observable symptom, evidence trail,
recovery proof, and follow-up action. The Phase 2 manual procedures and known
limitations are documented before Phase 3 is considered.

## Phase 2 operating workflow

Every configuration change should use this sequence:

1. State the objective, scope, expected impact, and rollback or recovery path.
2. Capture the relevant pre-change state.
3. Apply the smallest manual change to the canary VM.
4. Verify service, security, networking, data, and reboot behavior as relevant.
5. Stop and investigate if evidence differs from the expected result.
6. Roll out to the remaining VMs only after the canary passes.
7. Record the final state, deviations, and any automation candidate.

The canary is initially drl-ops-01 unless a chunk documents a safer target.
The existing Windows-to-guest SSH path and Hyper-V console are recovery paths;
they must remain available while access changes are being tested.

## Current Chunk

Chunk 1: Operating model and baseline capture - Ready to begin.

Phase 2 is active, but no Phase 2 implementation work is complete yet. Do not
begin Chunk 2 until Chunk 1's baseline and change-control verification gate has
passed.

## Not Started

- Phase 2 Chunks 1-10, except for the Phase 2 plan above
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

- The approved account, group, permission, and sudo model is documented and
  verified with both permitted and denied actions.
- Key-based SSH administration and any approved hardening are verified after
  reboot without losing the recovery path.
- Package state and the controlled update procedure are documented and verified.
- Process and systemd checks, lifecycle operations, and recovery evidence are
  documented.
- Journald and logrotate behavior, retention, and test-event investigation are
  understood and verified.
- Storage, filesystem, mount, capacity, and reboot behavior are documented and
  verified without unintended disk changes.
- Network identity, routes, listening sockets, UFW rules, and required or
  prohibited traffic are verified without Phase 1 drift.
- Resource and health checks produce repeatable evidence and normal operating
  observations are documented.
- At least one controlled Linux failure lab is investigated from symptom through
  recovery and prevention, with an incident or troubleshooting record.
- Verified manual procedures, limitations, and candidates for later automation
  are documented before Phase 3 begins.

Status: not started. These criteria will be evaluated as the Phase 2 chunks are
completed and verified.
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

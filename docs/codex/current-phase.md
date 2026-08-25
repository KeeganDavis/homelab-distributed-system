# Current Project State

## Current Phase

Phase 1: Virtual Infrastructure

See the [Phase 1 definition in the project plan](../project-plan.md#phase-1-virtual-infrastructure).

## Current Objective

Build and verify the local Ubuntu Server VM foundation needed for the later
Linux administration, application, container, and Kubernetes phases. Work should
progress in small, independently verified chunks.

## Phase 0 Completion

Phase 0: Repository Foundation is complete.

Completed outcomes:

- Repository directory scaffold established with Git placeholders.
- Project plan, environment notes, current-phase tracking, and task template added.
- Architecture overview and ADR guidance added.
- Repository guidance and pull request workflow established.
- Phase 0 documentation and repository structure manually reviewed.

## Phase 1 Work Breakdown

The project plan remains the source of truth for Phase 1 scope. The following
chunks divide that scope into small learning and verification steps:

### Chunk 1: Hypervisor and host readiness

- Select and configure the hypervisor.
- Confirm storage locations and reasonable CPU/RAM allocations for concurrent desktop use.
- Define the VM naming convention and initial inventory.

Verification: the hypervisor is ready, the resource budget is documented, and
the VM inventory is approved before creating guests.

Status: complete. Microsoft Hyper-V is selected and verified; the approved
storage paths, resource budget, and initial VM inventory are documented.

### Chunk 2: Virtual network and addressing design

- Define the virtual network or switch arrangement.
- Create the hostname and IP plan for the operations, control-plane, and worker VMs.
- Decide how local DNS or name resolution will work.
- Document the intended SSH and firewall boundaries.

Verification: the addressing and connectivity plan is written down before VM
deployment begins.

Status: complete. The dedicated Internal switch design, private subnet, static
hostname/IP plan, hosts-file name resolution approach, and intended SSH and
firewall boundaries were approved and documented in
[ADR 001](../../architecture/adr/001-hyper-v-lab-network.md). Implementation
of the design is tracked in Chunks 3-6.

### Chunk 3: Operations VM

- Create one Ubuntu Server operations VM.
- Configure its hostname and network identity.
- Establish administrative SSH access from the Windows host.

Verification: the operations VM boots reliably, has the expected identity and
network reachability, and can be accessed through SSH.

Status: complete. The `drl-ops-01` Ubuntu Server VM was created with the
approved resources and storage paths, configured with hostname
`drl-ops-01` and address `192.168.50.10/24`, and independently verified after
reboot. SSH access from the Windows host was verified on TCP port 22.

### Chunk 4: Kubernetes control-plane VM

- Create the control-plane VM from the validated Ubuntu process.
- Apply its hostname, IP configuration, SSH access, and baseline firewall rules.

Verification: the control-plane VM is independently reachable and its resource
usage is acceptable. Kubernetes installation is out of scope for Phase 1.

Status: complete. `drl-k8s-cp-01` was created with the approved storage paths,
Generation 2 configuration, 2 vCPU, and fixed 4 GB memory. The guest reports
hostname `drl-k8s-cp-01` and address `192.168.50.20/24`. SSH from the Windows
host was verified on TCP port 22, and UFW was verified active with default-deny
incoming traffic and an SSH allow rule from `192.168.50.1`. No Kubernetes
services or worker VMs were created. NAT and DNS remain out of scope for this
chunk.

### Chunk 5: Worker VMs

- Create worker VM 1 and verify it completely.
- Create worker VM 2 only after worker VM 1 passes verification.
- Apply the same identity, access, and baseline network configuration.

Verification: each worker is validated independently before the next VM is
created.

Status: complete. `drl-k8s-wk-01` was created and fully verified before
`drl-k8s-wk-02` was created. Both workers use Generation 2, 2 vCPU, fixed 4 GB
memory with dynamic memory disabled, approved storage paths, and the `drl-lab`
switch. Each guest reports its approved hostname and static address, SSH from
the Windows host was verified on TCP port 22, and UFW was verified active with
default-deny incoming traffic and SSH allowed from `192.168.50.1`. Both workers
were reboot-verified, and no Kubernetes services were installed.

### Chunk 6: Shared access and name-resolution verification

- Verify SSH connectivity from the intended administrative host to every VM.
- Verify hostname and IP resolution between the planned systems.
- Confirm the baseline firewall behavior for required administrative traffic.

Verification: expected connections succeed, prohibited connections are blocked,
and failures are understood rather than hidden by automatic fixes.

Status: complete. Direct-IP and hostname-based SSH
from the Windows host succeeded for all four VMs. Static hosts-file mappings
were added to the Windows host and all guests, and guest-side resolution was
verified. All four guest firewall boundaries were verified with default-deny
incoming traffic and SSH allowed from `192.168.50.1`; guest-originated TCP
port 22 connections to the protected VMs were blocked.

### Chunk 7: Phase 1 handoff documentation

- Record the final VM inventory, hostnames, IPs, and resource allocations.
- Document the verified access and network behavior.
- Capture any deviations, limitations, or follow-up work for Phase 2.

Verification: another session can use the documentation to understand and
operate the virtual infrastructure safely.

## Current Chunk

Chunk 6: Shared access and name-resolution verification - Complete.

Chunk 5 and Chunk 6 are complete. Do not begin Chunk 7 or Phase 2 until the
user explicitly decides to proceed.

## Not Started

- Linux administration
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

## Phase 1 Completion Criteria

Phase 1 is complete when:

- The planned operations, control-plane, and two worker Ubuntu VMs exist.
- Hostnames and IP assignments are documented and stable.
- SSH access is verified for all planned administrative paths.
- Name resolution works according to the documented design.
- A baseline firewall policy is applied and verified.
- Resource usage is reasonable for concurrent desktop use.
- The final state and known limitations are documented.

## Current Constraints

- Host: Windows 11
- CPU: Intel Core i7-9700K
- RAM: 32 GB
- GPU: RTX 2070 Super
- Multiple local drives available
- Resource usage should remain reasonable for concurrent desktop use

## Phase Advancement

Do not advance to Phase 2 until the Phase 1 completion criteria are verified
and the user explicitly decides to proceed.

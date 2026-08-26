# Runbook: Phase 2 Chunk 1 Operating Model and Baseline

## Purpose and boundary

This runbook defines the manual operating model and read-only baseline for
Phase 2 Linux administration. It is intended to be performed manually before
any equivalent procedure is considered for Ansible.

This chunk makes no guest or Windows configuration changes. It does not create
users, groups, sudo rules, SSH keys, packages, services, firewall rules,
routes, mounts, or logging policy.

## Lab inventory

| VM | Role | Address | Canary/rollout position |
|---|---|---|---|
| `drl-ops-01` | Operations | `192.168.50.10/24` | Canary, first |
| `drl-k8s-cp-01` | Kubernetes control plane | `192.168.50.20/24` | Second |
| `drl-k8s-wk-01` | Kubernetes worker 1 | `192.168.50.21/24` | Third |
| `drl-k8s-wk-02` | Kubernetes worker 2 | `192.168.50.22/24` | Fourth |

Administrative traffic originates from the Windows host at `192.168.50.1`
over the `drl-lab` Internal Hyper-V switch. Guest-to-guest SSH is not an
administrative path.

## Current administrative access model

- Account: `opsadmin` on all four VMs.
- SSH origin: Windows host `192.168.50.1`.
- Primary recovery path: the existing Windows-to-guest SSH path.
- Secondary recovery path: Hyper-V console access.
- Current sudo policy: `opsadmin` may run `(ALL : ALL) ALL`.
- Sudo authentication: interactive password required.
- Observed group membership: `adm`, `cdrom`, `sudo`, `dip`, `plugdev`, and
  `lxd`.
- `/usr/sbin/lxc` is present on all four VMs, but `lxd.service` was reported
  as absent and inactive on all four.

This is the observed current state, not the approved least-privilege target
for Chunk 2. The `lxd` membership requires explicit review before the account
model is changed.

## Change workflow

Every future configuration change follows this sequence:

1. State the objective, scope, expected impact, and rollback or recovery path.
2. Capture the relevant pre-change state.
3. Apply the smallest manual change to `drl-ops-01`.
4. Verify the expected service, access, security, networking, data, and reboot
   behavior relevant to the change.
5. Stop and investigate if evidence differs from the expected result.
6. Roll out in the documented order only after the canary verification gate
   passes.
7. Capture post-change evidence, deviations, and any later automation
   candidate.

The existing Windows SSH path and Hyper-V console must remain available while
access-related changes are tested.

## Checkpoint and recovery policy

No Hyper-V checkpoint was created for this observation-only chunk.

For a later risky canary change, a temporary checkpoint may be created
immediately before the change as a learning recovery aid. Before creating one,
record:

- VM name and checkpoint name;
- creation time and VM state;
- checkpoint type and storage location;
- expected storage impact; and
- the restore and removal procedure.

A checkpoint is not a backup. It must not be retained as the lab's backup
strategy or allowed to accumulate indefinitely. After successful verification,
remove the temporary checkpoint. If recovery is required, stop the rollout,
restore the documented checkpoint, verify the recovery path, and reassess the
change before trying again.

## Read-only baseline procedure

Run the following manually on each VM as `opsadmin`. The output is summarized
for comparison rather than pasted into the chat.

```bash
printf 'TIME='; date --iso-8601=seconds
printf 'HOST='; hostnamectl --static
printf 'ADDR='; ip -br addr | grep -v '^lo'
printf 'ROUTES='; ip route | tr '\n' ';'; echo
printf 'SSH_LISTEN='; ss -lnt | grep -E '(:22[[:space:]]|:22$)' | tr '\n' ';'; echo
printf 'PACKAGES='; dpkg-query -W | wc -l
printf 'RUNNING_SERVICES='; systemctl list-units --type=service --state=running --no-legend | wc -l
printf 'FAILED_SERVICES='; systemctl --failed --no-legend | tail -n +2 | grep -v '^$' | wc -l
printf 'ROOT_FS='; df -hT / | tail -n 1
printf 'MEMORY='; free -h | awk '/^Mem:/ {print $3 "/" $2}'
printf 'LOAD='; uptime
printf 'LOG_WARNINGS_OR_HIGHER='; journalctl -b -p warning..alert --no-pager | wc -l
```

The broader one-time inspection also included package inventory, enabled and
running services, failed units, top processes, block devices, mounts, filesystems,
inode use, CPU details, memory, boot history, and recent warning-or-higher
journal entries.

## Baseline observations - 2026-08-26

The operator reviewed the compact digest for all four VMs. No unexpected
differences were reported in hostname, address, routes, listening SSH service,
package/service state, root filesystem, memory/load, or recent journal health.
Exact compact-digest values were not retained in this document; the digest was
used as a manual comparison check for this learning exercise.

The account and access inspection produced the following attributable evidence:

| VM | Collection time (UTC) | SSH source | Result |
|---|---|---|---|
| `drl-ops-01` | `2026-08-26T16:39:50Z` | `192.168.50.1` | Expected |
| `drl-k8s-cp-01` | `2026-08-26T16:44:57Z` | `192.168.50.1` | Expected |
| `drl-k8s-wk-01` | `2026-08-26T16:47:27Z` | `192.168.50.1` | Expected |
| `drl-k8s-wk-02` | `2026-08-26T16:47:57Z` | `192.168.50.1` | Expected |

All four VMs reported the same `opsadmin` account, group membership, sudo
policy, LXC client presence, and inactive/missing LXD service. The workers,
control plane, and operations VM differed only in expected hostname, IP,
session, boot, and log timestamps.

During collection on `drl-k8s-wk-02`, three sudo password attempts failed before
the command succeeded. The operator confirmed these were caused by a mistyped
password; this is recorded as a collection note, not a system fault.

## Chunk 1 verification gate

- [x] Administrative account, origin, privilege assumptions, and recovery paths
      identified.
- [x] Canary and rollout order selected.
- [x] Change workflow and verification gate defined.
- [x] Checkpoint use and limitations defined; no checkpoint created for this
      chunk.
- [x] Read-only baseline reviewed for all four VMs.
- [x] No unexpected baseline differences reported.
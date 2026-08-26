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

The compact baseline was previously reviewed for all four VMs during the Phase
1 handoff, and the operator confirmed that the three non-canary VMs still match
the expected inventory and the canary. The detailed baseline below is the
attributable canary evidence collected during this Chunk 1 lesson; the other
three VMs were not re-collected in this session because their prior parity was
already verified and confirmed.

The canary collection window was approximately
`2026-08-26T18:00:19Z`-`2026-08-26T18:23:46Z`.

| Category | `drl-ops-01` observation | Assessment |
|---|---|---|
| Identity | Ubuntu Server 24.04.3; hostname `drl-ops-01`; `192.168.50.10/24` | Matches inventory |
| Access | `opsadmin` UID 1000; full `(ALL : ALL) ALL` sudo; groups include `sudo` and `lxd` | Administrative access works; `lxd` requires later least-privilege review |
| Network | `eth0` is up; static default route via `192.168.50.1`; local `/etc/hosts` resolution succeeds | The default route is explicitly present in netplan despite NAT being out of scope; record as configuration drift and do not change in this chunk |
| Packages | 682 installed packages; manually installed set is base Ubuntu/server packages plus `openssh-server` | No application stack is installed |
| Services | 48 enabled; 18 running; `ssh.service` and `ufw.service` active | One failed unit is described below |
| Processes | `systemd` and expected Ubuntu services/kernel workers; no application processes | Expected for Phase 2 start |
| Storage | 40 GB disk; 18.47 GB root LV; 18.47 GB free in `ubuntu-vg`; root filesystem 27% used | Matches the default Ubuntu LVM layout; unused VG capacity is recorded, not changed |
| Resources | 2 CPUs; 3.8 GiB memory; 426 MiB used; load average 0.00 | Healthy at collection time |
| Logs | Recent journal contains warnings listed below | Classified as baseline observations; no automatic remediation |

The isolated-network behavior is intentional: external DNS and NAT are not
expected. The local VM names resolve through `/etc/hosts`; `systemd-resolved`
has no upstream DNS scope, which is expected for this design.

The explicit default route is not caused by the Hyper-V Internal switch. It is
defined in the guest's netplan and points at the Windows host address even
though no NAT is configured. The route is therefore a documented baseline
discrepancy, not proof of working external connectivity.

The account and access inspection produced the following attributable evidence:

| VM | Collection time (UTC) | SSH source | Result |
|---|---|---|---|
| `drl-ops-01` | `2026-08-26T16:39:50Z` | `192.168.50.1` | Expected |
| `drl-k8s-cp-01` | `2026-08-26T16:44:57Z` | `192.168.50.1` | Expected |
| `drl-k8s-wk-01` | `2026-08-26T16:47:27Z` | `192.168.50.1` | Expected |
| `drl-k8s-wk-02` | `2026-08-26T16:47:57Z` | `192.168.50.1` | Expected |

All four VMs were previously reported with the same `opsadmin` account, group
membership, sudo policy, LXC client presence, and inactive/missing LXD service.
The workers, control plane, and operations VM differed only in expected
hostname, IP, session, boot, and log timestamps. The operator reconfirmed that
parity before this runbook was finalized.

The canary had one failed unit:

- `fwupd-refresh.service` attempted to refresh LVFS metadata and exited with
  status 1. This is an expected isolated-environment exception because the VMs
  intentionally have no Internet/NAT. The unit is timer-triggered and is not a
  Phase 2 application dependency.

Other canary journal observations were an unclean-shutdown journal replacement,
a cron warning for an unset optional `EXTRA_OPTS` variable, and a
systemd-networkd warning about the `eth0` name match. These remain recorded for
later system-operations review; no configuration changes were made in Chunk 1.

During collection on `drl-k8s-wk-02`, three sudo password attempts failed before
the command succeeded. The operator confirmed these were caused by a mistyped
password; this is recorded as a collection note, not a system fault.

## Chunk 1 verification gate

- [x] Dated baseline captured or confirmed for all four VMs, with attributable
      canary evidence and prior parity verification recorded.
- [x] Administrative account, origin, privilege assumptions, and recovery paths
      identified.
- [x] Canary and rollout order selected.
- [x] Change workflow and verification gate defined.
- [x] Checkpoint use and limitations defined; no checkpoint created for this
      chunk.
- [x] Read-only baseline reviewed for all four VMs.
- [x] Baseline differences and expected isolated-network exceptions identified
      and recorded for later investigation.
- [x] No Phase 2 server configuration changes were made.
- [x] Results reviewed before beginning Chunk 2.

Chunk 1 is verified complete. The documented route discrepancy, `lxd` group
membership, and expected `fwupd-refresh` failure are inputs to later lessons;
they are not silently corrected here.

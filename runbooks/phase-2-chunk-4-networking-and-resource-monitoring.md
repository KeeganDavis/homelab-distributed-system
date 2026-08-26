# Runbook: Phase 2 Chunk 4 Networking and Resource Monitoring

## Purpose and boundary

This runbook records the manual networking and resource-monitoring procedure
verified on the `drl-ops-01` canary on 2026-08-26.

The work was read-only apart from harmless connection tests. No networking,
routes, DNS, firewall policy, storage layout, packages, services, or
monitoring software were changed. The other three VMs were not configured or
verified for this chunk.

## Access and recovery

- Canary: `drl-ops-01`
- Primary administrative path: Windows host SSH over `drl-lab`
- Administrative source: `192.168.50.1`
- Secondary recovery path: Hyper-V VMConnect console
- SSH service remained active throughout the inspection.
- VMConnect was opened after inspection and the Ubuntu console/login screen
  was available.

## Network identity and interface state

Collection time: `2026-08-26T21:04:28+00:00`.

| Item | Observation | Assessment |
|---|---|---|
| Hostname | `drl-ops-01` | Matches the approved inventory |
| Interface | `eth0` up, MTU 1500 | Expected |
| IPv4 address | `192.168.50.10/24` | Matches the approved inventory |
| IPv6 address | Link-local `fe80::215:5dff:fe01:b001/64` | Expected; no global IPv6 address |
| Connected route | `192.168.50.0/24` via `eth0` | Expected lab subnet |
| Default route | `192.168.50.1` via `eth0` | Existing documented route; not changed |

Interface counters showed zero RX errors, RX drops, TX errors, TX drops,
carrier errors, and collisions. The interface had 3,382 received packets and
2,766 transmitted packets at the later collection time.

Static name resolution succeeded:

```text
192.168.50.10 drl-ops-01
192.168.50.20 drl-k8s-cp-01
192.168.50.21 drl-k8s-wk-01
192.168.50.22 drl-k8s-wk-02
```

`systemd-resolved` reported no active DNS scope or upstream DNS server. This
matches the intentional isolated-network design; local `/etc/hosts` entries
provide the lab name resolution.

## Listening sockets and service mapping

The listener inspection used `sudo ss -lntup`.

| Listener | Process | Owning service | Assessment |
|---|---|---|---|
| `0.0.0.0:22/tcp` and `[::]:22/tcp` | `sshd`, PID 961 | `ssh.service` / `ssh.socket` | Expected administrative listener; restricted by UFW |
| `127.0.0.53:53/tcp,udp` and `127.0.0.54:53/tcp,udp` | `systemd-resolved`, PID 615 | `systemd-resolved.service` | Loopback-only resolver; not exposed on `eth0` |

No application, database, Kafka, or other unexpected network listeners were
present.

Both `ssh.service` and `systemd-resolved.service` were `active` and `enabled`.
SSH reported `ssh.socket` as its triggering unit, and `sshd` passed its
startup configuration test. Two established SSH sessions from
`192.168.50.1` were present during the later inspection.

## Firewall and traffic verification

The existing UFW state was inspected without changing policy:

```text
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
22/tcp ALLOW IN 192.168.50.1
```

Traffic behavior was verified as follows:

- Windows `Test-NetConnection` to `192.168.50.10:22` succeeded.
- Connection attempts from `drl-ops-01` to `192.168.50.20:22`,
  `192.168.50.21:22`, and `192.168.50.22:22` timed out as expected.
- No login or configuration operation was performed on the other VMs.

The SSH log recorded one reset at `21:10:15` from `192.168.50.1`. The timing,
source, active SSH service, and continuing established sessions identify it as
the Windows TCP probe closing before SSH negotiation, not an SSH availability
failure.

## Resource and system health snapshot

Collection time: `2026-08-26T21:11:35+00:00`.

| Category | Observation | Assessment |
|---|---|---|
| CPUs | 2 | Matches VM allocation |
| Load | `0.00, 0.00, 0.00` | Healthy at collection time |
| Memory | 420 MiB used of 3.8 GiB; 3.4 GiB available | Healthy at collection time |
| Swap | 0 B used of 2.0 GiB | No memory pressure observed |
| Root filesystem | 19 GiB, 4.6 GiB used, 27% | Matches prior baseline |
| `/boot` | 2.0 GiB, 101 MiB used, 6% | Healthy |
| Root inodes | 96K used of 1.2M, 9% | Healthy |
| `/boot` inodes | 309 used of 128K, 1% | Healthy |
| Disk layout | 40 GiB disk; EFI, `/boot`, LVM; 18.5 GiB root LV | Matches existing layout |
| Running services | 19 | Consistent with the canary state; no application stack installed |
| Top processes | Normal systemd, kernel workers, resolver, timesync, and SSH processes | No unexpected workload |

`systemctl is-system-running` reported `degraded` because the known
`fwupd-refresh.service` failure remains present. The failed-unit list contained
only:

```text
fwupd-refresh.service - Refresh fwupd metadata and update motd
```

This is expected in the isolated environment without Internet/NAT and was not
repaired.

## Recent warnings and errors

The warning-or-higher journal review found the previously documented:

- virtual PCI support warning;
- device-mapper IMA configuration warning;
- successful LVM physical-volume and volume-group completion messages logged at
  warning priority;
- predictable `eth0` network-name matching warning;
- non-fatal cron warning for the unset optional `EXTRA_OPTS` variable; and
- expected `fwupd-refresh.service` failure caused by the isolated environment.

The single SSH connection-reset message was generated by the Windows-host TCP
probe, as described above. No persistent resource, service, interface, or
access failure was observed.

## Operational interpretation

Evidence that would require investigation in a future check includes an
interface that is down, increasing packet errors or drops, an unexpected
non-loopback listener, a successful prohibited guest-to-guest connection, a
failed Windows-host SSH test, sustained load inconsistent with the two CPUs,
low available memory or swap activity, rapid filesystem or inode growth, new
failed units, or repeated unexplained journal errors.

The explicit default route, lack of NAT, lack of upstream DNS, and
`fwupd-refresh.service` failure remain known baseline conditions. They were
recorded and not changed.

## Verification checklist

- [x] Network identity, addresses, routes, and interface state inspected.
- [x] Interface error and drop counters inspected.
- [x] Listening sockets mapped to owning processes and services.
- [x] UFW state inspected without changing policy.
- [x] Windows-host SSH access verified.
- [x] Guest-to-guest SSH prohibition verified from the canary.
- [x] CPU, memory, load, disk, inode, process, and service state captured.
- [x] Recent warning-or-higher journal entries reviewed and classified.
- [x] SSH and Hyper-V recovery paths confirmed available.
- [x] No other VM was configured or verified.
- [x] No secrets or security-sensitive values were recorded.

Chunk 4 is verified complete for the `drl-ops-01` canary scope only.

## Chunk 5 handoff and future automation candidates

The manual Phase 2 workflow is now documented across the Chunk 1, Chunk 2,
Chunk 3, and this Chunk 4 runbook. The canary procedure is suitable for later
automation review after the deferred fleet work is completed.

Potential future Ansible candidates are:

- collect and report host, network, service, storage, and resource facts;
- validate the approved UFW policy and required SSH origin;
- validate expected listeners and systemd service state;
- collect failed units and filtered journal evidence; and
- perform repeatable post-change and post-reboot verification.

Automation must preserve the documented separation between provisioning,
configuration, deployment, and orchestration. It must not silently repair the
known isolated-network exceptions.

The remaining limitation is scope: the other three VMs have not received the
manual Chunk 2 or Chunk 3 procedures, and this Chunk 4 inspection was also
canary-only. Those outstanding criteria prevent Phase 2 from being declared
complete or Phase 3 from being started.

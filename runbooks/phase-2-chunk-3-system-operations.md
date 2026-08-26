# Runbook: Phase 2 Chunk 3 System Operations

## Purpose and boundary

This runbook records the manual system-operations procedure verified on the
`drl-ops-01` canary during Phase 2 Chunk 3 on 2026-08-26.

The work covered package-management inspection, systemd service and unit
inspection, journald filtering, filesystem and storage inspection, logrotate
inspection and execution, and cron/systemd timer verification.

This was a canary-only exercise. No commands were run against
`drl-k8s-cp-01`, `drl-k8s-wk-01`, or `drl-k8s-wk-02`. This runbook must not be
read as fleet-wide configuration or verification.

No networking, firewall policy, storage layout, application stack, or secret
configuration was changed. The known `fwupd-refresh.service` and LXD
observations were not repaired or modified.

## Access and recovery

- Canary: `drl-ops-01`
- Primary administrative path: Windows host SSH over `drl-lab`
- Daily administrative account used for operational checks: `drladmin`
- Break-glass account: `opsadmin`
- Secondary recovery path: Hyper-V console
- Sudo authentication remained password-required.

The initial pre-change capture was made as `opsadmin` at
`2026-08-26T19:53:19+00:00`. The package, service, journal, storage, and
timer work was then performed as `drladmin` using `sudo` where required.

## Change workflow used

1. Capture relevant canary state before making changes.
2. Inspect the package, service, journal, filesystem, storage, and schedule
   state.
3. Make one small, observable change: restart `cron.service`.
4. Verify service state and journal evidence.
5. Run logrotate's debug evaluation, then execute its oneshot service once.
6. Verify the result, timer state, storage state, and absence of failed units.

The existing SSH and Hyper-V recovery paths remained available throughout.

## Pre-change evidence

The canary reported:

- Hostname: `drl-ops-01`
- Systemd state: `running`
- Uptime: approximately 15 minutes at capture time
- Load average: `0.00, 0.00, 0.00`
- Root filesystem: ext4 on `ubuntu-lv`, approximately 19 GiB, 27% used
- Root inode usage: 9%
- Disk layout: 40 GiB disk with EFI, `/boot`, and an LVM partition
- Volume group: `ubuntu-vg`, approximately 36.95 GiB total and 18.47 GiB free
- No upgradeable packages were listed.
- `dpkg --audit` produced no output.
- No unexpected failed units were reported in the final verification.

The journal contained the previously recorded isolated-lab warnings involving
PCI support, device-mapper IMA configuration, the predictable `eth0` netplan
name match, and the unset optional cron variable `EXTRA_OPTS`.

## Package management

### Inspection and operation

The installed and candidate versions for `openssh-server` were inspected with
`apt-cache policy`:

```text
Installed: 1:9.6p1-3ubuntu13.13
Candidate: 1:9.6p1-3ubuntu13.13
```

`apt list --upgradable` listed no upgrades. `dpkg --audit` produced no output
before or after the following safe package-database operation:

```bash
sudo dpkg --configure --pending
```

### Result

The package database was clean and no pending package configuration required
action. No package was installed, removed, or upgraded.

### Operational lesson

`apt` resolves package versions and repositories, while `dpkg` maintains the
local installed-package database. A clean audit and matching installed and
candidate versions indicate that package changes were not required for this
canary exercise.

## systemd and journald

### Service inspection

`cron.service` was inspected as an existing, low-risk service:

- Unit file: `/usr/lib/systemd/system/cron.service`
- Enabled: yes
- Initial state: active/running
- Main PID before restart: `918`
- No drop-in units
- `ExecStart` uses `/usr/sbin/cron -f -P $EXTRA_OPTS`
- The optional `/etc/default/cron` environment file is referenced.

### Observable change and verification

The service was restarted with:

```bash
sudo systemctl restart cron.service
```

The restart completed successfully at approximately `20:02:01 UTC`. The new
cron process was PID `1476`, and the service returned to `active (running)`.

Privileged journal filtering showed:

- systemd stopping and starting `cron.service`;
- cron initialization messages;
- the expected `EXTRA_OPTS` warning; and
- scheduled `sysstat` cron activity at `19:45:01` and `19:55:01 UTC`.

The warning is non-fatal: cron remained active and processed scheduled work.
It was recorded, not repaired.

### Operational lesson

`systemctl status`, `is-active`, and `is-enabled` answer different questions:
current health, current runtime state, and boot-time enablement. `journalctl`
can be narrowed by boot, unit, and priority. `drladmin` needed `sudo` to view
all system journal files.

## Filesystem and storage inspection

The canary's storage remained at the existing default Ubuntu LVM layout:

- Physical disk: approximately 40 GiB
- EFI partition: approximately 1 GiB
- `/boot`: approximately 2 GiB ext4 partition
- LVM physical volume: approximately 36.9 GiB
- Volume group: `ubuntu-vg`
- Logical volume: `ubuntu-lv`, 18.47 GiB ext4 root filesystem
- Free volume-group capacity: 18.47 GiB
- Root filesystem use: 4.6 GiB of 19 GiB, or 27%
- Root inode use: 96K of approximately 1.2M, or 9%

No partition, volume, mount, filesystem, or storage-capacity change was made.
The unused volume-group capacity was recorded for future planning only.

## Log rotation

### Configuration inspection

The logrotate debug run read `/etc/logrotate.conf` and the configuration files
under `/etc/logrotate.d`. It evaluated 13 log policies. No log met its current
rotation threshold, no postrotate script was run, and debug mode made no file
changes.

### Service verification

The logrotate oneshot service was executed manually:

```bash
sudo systemctl start logrotate.service
```

The execution completed at `2026-08-26 20:08:49 UTC` with:

```text
Result=success
ExecMainStatus=0
```

Because `logrotate.service` is a oneshot unit, its final state was
`inactive/dead` after successful completion. That is expected and differs from
the persistent `active/running` state expected for cron.

## Cron and systemd timers

The cron journal demonstrated that scheduled `sysstat` jobs ran successfully.
The `logrotate.timer` unit was also inspected:

- Enabled: yes
- State: active/waiting
- Schedule: `OnCalendar=daily`
- Accuracy: one hour
- Persistent: yes
- Next scheduled activation: `2026-08-27 00:00:00 UTC`
- Activated service: `logrotate.service`

After the manual logrotate execution, the timer remained active. No custom
cron job or timer was added.

## Final verification gate

The final canary checks reported:

- `HOST=drl-ops-01`
- `SYSTEMD=running`
- `CRON_ACTIVE=active`
- `CRON_ENABLED=enabled`
- `LOGROTATE_TIMER=active`
- `logrotate.service` result: `success`
- `logrotate.service` exit status: `0`
- No failed units were listed
- Root filesystem: 27% used
- Root inode usage: 9%

The canary remained reachable through the existing recovery paths. No other VM
was changed or verified as part of this task.

## Known limitations and follow-up

- The `EXTRA_OPTS` cron warning remains a known baseline observation.
- The expected isolated-environment `fwupd-refresh.service` behavior remains
  unchanged.
- No reboot was performed for Chunk 3 because no persistent access or service
  configuration was changed; reboot and recovery behavior were verified during
  Chunk 2.
- The other three VMs have not received manual Chunk 3 configuration or
  verification.
- The procedure is a candidate for later automation only after the canary
  observations and boundaries are reviewed.

## Verification checklist

- [x] Canary pre-change state captured.
- [x] Package state inspected and package database checked.
- [x] Systemd unit and service state inspected.
- [x] Cron service restarted and returned healthy.
- [x] Journald filtered by service and priority.
- [x] Filesystem, inode, block-device, and LVM state inspected.
- [x] Logrotate configuration dry-run completed without changes.
- [x] Logrotate oneshot service completed successfully.
- [x] Cron activity and systemd timer state verified.
- [x] Existing recovery paths preserved.
- [x] Other three VMs left outside the task scope.
- [x] No secrets or security-sensitive material recorded.

Chunk 3 is verified complete for the `drl-ops-01` canary scope only.

# Runbook: Phase 2 Chunk 2 Identity and Access

## Purpose and boundary

This runbook records the manual identity and access procedure for the verified
Phase 2 Chunk 2 canary milestone. It is the source procedure for later
automation. The user-approved fleet rollout is deferred to the future Ansible
phase and is not represented here as complete.

This chunk covers users, groups, sudo access, controlled ownership and
permissions, non-secret shell environment context, and SSH keys. It does not
change networking, firewall policy, storage, logging policy, or application
services.

## Target access model

| Identity | Intended use | Access |
|---|---|---|
| `opsadmin` | Break-glass recovery | Existing password SSH and full sudo retained; no direct `lxd` membership |
| `drladmin` | Daily human administrator | Ed25519 SSH key, password-required sudo, member of `sudo` and `drl-operators` |
| `drlread` | Read-only access test account | Password SSH; no sudo, `lxd`, or `drl-operators` membership |
| `drl-operators` | Controlled permission exercises | Group ownership for `/srv/drl/shared` |

No service accounts are created until application services exist. Password SSH
and Hyper-V console access remain recovery paths; password authentication is
not hardened or disabled by this chunk.

## Canary status: `drl-ops-01`

Verified on 2026-08-26:

- `opsadmin` no longer belongs to `lxd`; `sudo` access remains `(ALL : ALL) ALL`.
- `drladmin` exists, belongs to `sudo` and `drl-operators`, and can use
  password-required sudo.
- `drlread` exists without administrative or operator-group membership and is
  denied sudo.
- `/srv/drl/shared` is owned by `root:drl-operators` with mode `2770` and
  setgid enabled.
- `drladmin` created a file in the shared path with inherited group ownership
  and mode `660`.
- `drlread` was denied directory listing, file reading, and file creation.
- Key-only SSH from the Windows host to `drladmin` succeeded using a dedicated
  Ed25519 key. Password authentication was explicitly disabled for the test.
- `/etc/profile.d/drl-lab.sh` provided `DRL_ENVIRONMENT=lab`, dynamic
  `DRL_NODE_NAME`, and `DRL_NODE_ROLE=operations`.
- Key login, sudo, group membership, environment variables, shared-path
  access, and recovery access survived a canary reboot.

## Known observations

- Running `sudo lxc list` unexpectedly invoked the installed
  `lxd-installer.socket`; the attempted LXD snap installation failed because
  the isolated lab could not reach its source. No LXD snap was installed.
  This was recorded as an observation and was not repaired or disabled.
- The pre-existing `fwupd-refresh.service` failure remains an expected
  isolated-network baseline exception.
- No private key, password, or other secret belongs in this repository.

## Scope amendment and deferred rollout

On 2026-08-26, the user approved closing the current manual learning milestone
after the verified `drl-ops-01` canary. The remaining VM rollout is deferred to
the future Ansible phase. This is an explicit scope amendment, not evidence
that the other three VMs have been configured or verified.

The verified canary procedure remains to be performed manually, one VM at a
time, in this order, when the deferred rollout is eventually undertaken:

1. `drl-k8s-cp-01` with `DRL_NODE_ROLE=k8s-control-plane`
2. `drl-k8s-wk-01` with `DRL_NODE_ROLE=k8s-worker`
3. `drl-k8s-wk-02` with `DRL_NODE_ROLE=k8s-worker`

Each VM requires identity creation, key installation, controlled permission
setup, role-specific environment verification, and reboot verification before
the next VM is changed.

## Recovery notes

- Keep `opsadmin` password SSH and Hyper-V console access available during all
  access changes.
- Restore direct LXD group membership only if a later, evidence-based decision
  requires it: `sudo gpasswd --add opsadmin lxd`.
- Do not remove `opsadmin`, disable password authentication, or remove its sudo
  access until replacement access and console recovery have been independently
  verified.

## Verification gate

- [x] Target identity and access model defined.
- [x] Canary users, groups, sudo, permissions, environment, and SSH key access
      verified.
- [x] Canary reboot and recovery paths verified.
- [x] Amended canary milestone reviewed and closed.
- [deferred] Control plane rollout and reboot verification; future Ansible phase.
- [deferred] Worker 1 rollout and reboot verification; future Ansible phase.
- [deferred] Worker 2 rollout and reboot verification; future Ansible phase.
- [deferred] Fleet-wide final review; future Ansible phase.

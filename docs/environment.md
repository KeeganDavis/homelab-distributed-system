# Environment

This document records the actual lab environment as it is implemented.

Do not document planned infrastructure here as though it already exists.

## Host

- OS: Windows 11 x64
- CPU: Intel Core i7-9700K
- RAM: 32 GB
- GPU: NVIDIA RTX 2070 Super
- Storage: multiple local drives

## Hypervisor

- Selected: Microsoft Hyper-V
- Status: enabled and verified
- Verification:
  - Windows 11 Education host
  - Hypervisor detected and Hyper-V Virtual Machine Management (`vmms`) service running automatically
  - Required Hyper-V features enabled
- Default VM configuration path: `C:\Hyper-V\VMs`
- Default virtual disk path: `C:\Hyper-V\VHDX`

## Virtual Machines

### Implemented VMs

| Hostname | Role | OS | Generation | CPU | RAM | IP | Storage |
|---|---|---|---:|---:|---:|---|---|
| drl-ops-01 | Operations server | Ubuntu Server 24.04.3 | 2 | 2 | 4 GB | `192.168.50.10/24` | `C:\Hyper-V\VMs`, `C:\Hyper-V\VHDX\drl-ops-01.vhdx` |
| drl-k8s-cp-01 | Kubernetes control plane | Ubuntu Server 24.04.3 | 2 | 2 | 4 GB | `192.168.50.20/24` | `C:\Hyper-V\VMs`, `C:\Hyper-V\VHDX\drl-k8s-cp-01.vhdx` |
| drl-k8s-wk-01 | Kubernetes worker 1 | Ubuntu Server 24.04.3 | 2 | 2 | 4 GB | `192.168.50.21/24` | `C:\Hyper-V\VMs`, `C:\Hyper-V\VHDX\drl-k8s-wk-01.vhdx` |
| drl-k8s-wk-02 | Kubernetes worker 2 | Ubuntu Server 24.04.3 | 2 | 2 | 4 GB | `192.168.50.22/24` | `C:\Hyper-V\VMs`, `C:\Hyper-V\VHDX\drl-k8s-wk-02.vhdx` |

Verification completed:

- The VM boots from its installed VHDX after reboot.
- The guest reports hostname `drl-ops-01`.
- The guest reports address `192.168.50.10/24`.
- The VM uses a 40 GB dynamically expanding VHDX with the default Ubuntu LVM layout.
- The Windows host can reach the guest on TCP port 22 over `drl-lab`.
- The control-plane VM boots from its installed VHDX after reboot.
- The control-plane guest reports hostname `drl-k8s-cp-01` and address `192.168.50.20/24`.
- The control-plane VM uses fixed 4 GB memory with Hyper-V dynamic memory disabled.
- The Windows host can reach the control-plane guest on TCP port 22 over `drl-lab`.
- The control-plane guest firewall is active with default-deny incoming and an SSH allow rule from `192.168.50.1`.
- Both worker VMs boot from their installed VHDX after reboot.
- Worker 1 reports hostname `drl-k8s-wk-01` and address `192.168.50.21/24`.
- Worker 2 reports hostname `drl-k8s-wk-02` and address `192.168.50.22/24`.
- Both worker VMs use 40 GB dynamically expanding VHDX disks with the default Ubuntu LVM layout.
- Both worker VMs use fixed 4 GB memory with Hyper-V dynamic memory disabled.
- The Windows host can reach both workers on TCP port 22 over `drl-lab`.
- Both worker guest firewalls are active with default-deny incoming traffic and SSH allowed from `192.168.50.1`.
- Windows-host SSH using each VM hostname was verified for all four VMs.
- Static hosts-file mappings were added to the Windows host and all four guests and verified with TCP and `getent hosts` checks.
- Guest-to-guest TCP port 22 from `drl-ops-01` to the control-plane and workers was blocked by their firewall policies.
- `drl-ops-01` UFW is active with default-deny incoming traffic and SSH allowed from `192.168.50.1`.
- TCP port 22 from the control-plane and worker guests to `drl-ops-01` was blocked after the firewall remediation.
- No Kubernetes services have been installed.

### Resource Summary

| Hostname | Role | OS | CPU | RAM | IP |
|---|---|---|---:|---:|---|
| All four VMs | Phase 1 lab allocation | Ubuntu Server 24.04.3 | 8 total | 16 GB total | `192.168.50.10`-`192.168.50.22` |

- Full implemented guest allocation: 8 vCPU and 16 GB RAM.
- Active VM configuration and virtual disks use the internal `C:` SSD.
- The USB-connected `D:` drive is reserved for future VM exports and backups.

## Networking

### Implemented and Planned Networking

Implemented:

- Lab subnet in use: `192.168.50.0/24`
- Dedicated Hyper-V Internal switch: `drl-lab`
- Windows host-side adapter: `vEthernet (drl-lab)`
- Windows host-side address: `192.168.50.1/24`
- `drl-ops-01` connected to `drl-lab` with static address `192.168.50.10/24`
- `drl-k8s-cp-01` connected to `drl-lab` with static address `192.168.50.20/24`
- `drl-k8s-wk-01` connected to `drl-lab` with static address `192.168.50.21/24`
- `drl-k8s-wk-02` connected to `drl-lab` with static address `192.168.50.22/24`
- Windows NAT `drl-lab-nat` is active for `192.168.50.0/24`
- `drl-ops-01` uses `192.168.1.1` as its upstream DNS resolver and has verified
  outbound package access through the host NAT
- Windows host to `drl-ops-01` TCP port 22 connectivity verified
- Windows host to `drl-k8s-cp-01` TCP port 22 connectivity verified
- Windows host to both worker VMs TCP port 22 connectivity verified

Not yet implemented or verified:

- Outbound Internet access from the control-plane and worker VMs
- Physical LAN or Internet isolation has not been independently verified;
  direct inbound access is not intended
- Connectivity from WSL2 or other administrative origins

Existing host networks checked for overlap:

- Physical Ethernet: `192.168.1.0/24`
- Default Switch: `192.168.64.0/20`
- WSL: `172.24.96.0/20`

## SSH

### Implemented and Planned SSH

Implemented and verified:

- Windows host to `drl-ops-01` over lab-subnet SSH, TCP `22`
- Windows host to `drl-ops-01` using the `opsadmin` account
- Windows host to `drl-k8s-cp-01` over lab-subnet SSH, TCP `22`
- Windows host to `drl-k8s-cp-01` using the `opsadmin` account
- Windows host to `drl-k8s-wk-01` over lab-subnet SSH, TCP `22`, using `opsadmin`
- Windows host to `drl-k8s-wk-02` over lab-subnet SSH, TCP `22`, using `opsadmin`
- Windows host to `drl-ops-01` as `drladmin` using a dedicated Ed25519 key,
  with password authentication disabled during verification
- Ubuntu `openssh-server` installed; SSH service active and enabled
- Control-plane UFW active with default-deny incoming and SSH allowed from
  `192.168.50.1`
- Worker UFW active with default-deny incoming and SSH allowed from
  `192.168.50.1`
- Operations VM UFW active with default-deny incoming and SSH allowed from
  `192.168.50.1`
- Guest-to-guest TCP port 22 from `drl-ops-01` to the control-plane and workers
  was blocked by the target UFW policies.
- Guest-to-guest TCP port 22 from the control-plane and worker guests to
  `drl-ops-01` was blocked by the operations VM UFW policy.

Not yet implemented or verified:

- `drl-ops-01` to the control-plane and worker VMs over SSH for administration
  and automation
- Physical LAN or Internet SSH exposure has not been independently verified;
  direct exposure is not intended
- Later cluster traffic rules remain unconfigured
- Key-based access for `drl-k8s-cp-01`, `drl-k8s-wk-01`, and `drl-k8s-wk-02`
  remains deferred to the future Ansible phase
- Password-authentication hardening; password recovery remains intentionally
  enabled

## DNS / Name Resolution

### Approved Design - Configured and Verified

- No dedicated lab DNS server is planned initially.
- Static hosts-file entries will provide name resolution for the four planned
  VMs.
- Static entries are present on the Windows host and each guest for all four
  VM hostnames and addresses.
- There is no automatic registration or reverse DNS.
- Windows-host hostname-based SSH succeeds for all four VMs.
- Each guest resolves all four VM hostnames to their documented `192.168.50.x`
  addresses with `getent hosts`.

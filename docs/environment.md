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
- No worker VMs have been created and Kubernetes has not been installed.

### Remaining Approved Pre-Provisioning Plan

| Hostname | Role | OS | CPU | RAM | Planned IP |
|---|---|---|---:|---:|---|
| drl-k8s-wk-01 | Kubernetes worker 1 | Ubuntu Server | 2 | 4 GB | `192.168.50.21` |
| drl-k8s-wk-02 | Kubernetes worker 2 | Ubuntu Server | 2 | 4 GB | `192.168.50.22` |

- Full planned guest allocation: 8 vCPU and 16 GB RAM; currently implemented allocation: 4 vCPU and 8 GB RAM.
- Active VM configuration and virtual disks use the internal `C:` SSD.
- The USB-connected `D:` drive is reserved for future VM exports and backups.
- The worker entries remain approved pre-provisioning values; they have not been
  created or configured.

## Networking

### Implemented and Planned Networking

Implemented:

- Lab subnet in use: `192.168.50.0/24`
- Dedicated Hyper-V Internal switch: `drl-lab`
- Windows host-side adapter: `vEthernet (drl-lab)`
- Windows host-side address: `192.168.50.1/24`
- `drl-ops-01` connected to `drl-lab` with static address `192.168.50.10/24`
- `drl-k8s-cp-01` connected to `drl-lab` with static address `192.168.50.20/24`
- Windows host to `drl-ops-01` TCP port 22 connectivity verified
- Windows host to `drl-k8s-cp-01` TCP port 22 connectivity verified

Not yet implemented or verified:

- Planned NAT gateway behavior using `192.168.50.1`
- Planned guest Internet access: outbound through host NAT only
- Physical LAN or Internet isolation has not been independently verified;
  direct inbound access is not intended
- Guest firewall policy and behavior for `drl-ops-01` and future worker VMs
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
- Ubuntu `openssh-server` installed; SSH service active and enabled
- Control-plane UFW active with default-deny incoming and SSH allowed from
  `192.168.50.1`

Not yet implemented or verified:

- `drl-ops-01` to the control-plane and worker VMs over SSH for administration
  and automation
- Physical LAN or Internet SSH exposure has not been independently verified;
  direct exposure is not intended
- Worker guest firewalls and later cluster traffic rules remain unconfigured
- Key-based authentication and password-authentication hardening

## DNS / Name Resolution

### Approved Design - Not Yet Configured

- No dedicated lab DNS server is planned initially.
- Static hosts-file entries will provide name resolution for the four planned
  VMs.
- Entries will need to be maintained on each guest and, if desired, the
  Windows host.
- There is no automatic registration or reverse DNS.
- Name resolution is not configured or verified.

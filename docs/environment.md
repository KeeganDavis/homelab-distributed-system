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

### Approved Pre-Provisioning Plan

| Hostname | Role | OS | CPU | RAM | Planned IP |
|---|---|---|---:|---:|---|
| drl-k8s-cp-01 | Kubernetes control plane | Ubuntu Server | 2 | 4 GB | `192.168.50.20` |
| drl-k8s-wk-01 | Kubernetes worker 1 | Ubuntu Server | 2 | 4 GB | `192.168.50.21` |
| drl-k8s-wk-02 | Kubernetes worker 2 | Ubuntu Server | 2 | 4 GB | `192.168.50.22` |
| drl-ops-01 | Operations server | Ubuntu Server | 2 | 4 GB | `192.168.50.10` |

- Total planned guest allocation: 8 vCPU and 16 GB RAM.
- Active VM configuration and virtual disks use the internal `C:` SSD.
- The USB-connected `D:` drive is reserved for future VM exports and backups.
- These are approved pre-provisioning values; no Ubuntu VMs currently exist and
  no guest IP addresses have been configured.

## Networking

### Approved Design - Not Yet Configured

- Dedicated Hyper-V Internal switch: `drl-lab`
- Lab subnet: `192.168.50.0/24`
- Planned Windows host-side adapter and NAT gateway: `192.168.50.1`
- Planned guest Internet access: outbound through host NAT only
- Direct inbound access from the physical LAN or Internet: not intended
- Existing host networks were checked for overlap:
  - Physical Ethernet: `192.168.1.0/24`
  - Default Switch: `192.168.64.0/20`
  - WSL: `172.24.96.0/20`
- The dedicated switch, host adapter, NAT, and guest network configuration are
  not implemented.

## SSH

### Approved Policy - Not Yet Configured

- Windows host to all VMs over lab-subnet SSH, TCP `22`
- `drl-ops-01` to the control-plane and worker VMs over SSH for administration
  and automation
- No SSH exposure to the physical LAN or Internet
- Guest firewalls should default-deny unsolicited inbound traffic and allow
  only approved management and later cluster traffic
- SSH and firewall configuration has not been implemented or verified.

## DNS / Name Resolution

### Approved Design - Not Yet Configured

- No dedicated lab DNS server is planned initially.
- Static hosts-file entries will provide name resolution for the four planned
  VMs.
- Entries will need to be maintained on each guest and, if desired, the
  Windows host.
- There is no automatic registration or reverse DNS.
- Name resolution is not configured or verified.

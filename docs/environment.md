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

| Hostname | Role | OS | CPU | RAM | IP |
|---|---|---|---:|---:|---|
| drl-k8s-cp-01 | Kubernetes control plane | Ubuntu Server | 2 | 4 GB | TBD |
| drl-k8s-wk-01 | Kubernetes worker 1 | Ubuntu Server | 2 | 4 GB | TBD |
| drl-k8s-wk-02 | Kubernetes worker 2 | Ubuntu Server | 2 | 4 GB | TBD |
| drl-ops-01 | Operations server | Ubuntu Server | 2 | 4 GB | TBD |

- Total planned guest allocation: 8 vCPU and 16 GB RAM.
- Active VM configuration and virtual disks use the internal `C:` SSD.
- The USB-connected `D:` drive is reserved for future VM exports and backups.

## Networking

Not yet configured.

## SSH

Not yet configured.

## DNS / Name Resolution

Not yet configured.
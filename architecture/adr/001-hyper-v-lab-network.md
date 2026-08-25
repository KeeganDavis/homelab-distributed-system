# ADR 001: Hyper-V Lab Network

## Status

Accepted

## Context

Four planned VMs on a Windows Hyper-V host

## Options Considered

- External switch
- Default switch
- Private switch
- Dedicated internal switch with host NAT

## Decision

- `drl-lab`
- `192.168.50.0/24`
- host gateway/NAT address `192.168.50.1`
- static VM addresses
- hosts-file name resolution
- restricted SSH and firewall boundaries

## Rationale

The dedicated Internal switch provides host-to-VM and VM-to-VM communication
without placing the guests directly on the physical LAN. Host NAT can later
provide controlled outbound Internet access for updates while preventing
unsolicited inbound access. Static addressing and hosts files are simple and
transparent for this four-VM lab.

## Tradeoffs

- Host-side NAT must be configured before guests can use the Internet.
- There is no automatic DHCP or DNS service.
- Hosts-file entries must be updated manually on each guest and the Windows host if names or addresses change.
- There is no automatic DNS registration or reverse DNS.
- Future Kubernetes traffic will require explicitly planned firewall rules.

## Consequences

- A dedicated `drl-lab` Internal switch and host adapter must be created later.
- The host adapter will use `192.168.50.1/24`.
- The four VMs will receive their documented static addresses.
- Host NAT, SSH access, and guest firewall rules must be configured and verified in later implementation tasks.
- This ADR describes an approved design; none of these networking controls are currently implemented.

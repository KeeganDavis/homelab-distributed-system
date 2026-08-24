# System Overview

## Purpose

The Distributed Reliability Lab is a backend-focused distributed system designed
primarily for learning infrastructure operations, DevOps, SRE, cloud concepts,
and production troubleshooting.

## Logical Application Architecture
```
Synthetic Generator / External API
                |
                v
         Ingestion API
                |
                v
              Kafka
                |
        +-------+-------+
        |               |
        v               v
     Worker           Worker
        |               |
        +-------+-------+
                |
                v
           PostgreSQL
                |
             Redis
                |
                v
            Query API
```
## Platform Architecture
```
Developer
    |
    v
Git / GitHub
    |
    v
Jenkins
    |
    +----------------------+
    |                      |
    v                      v
Build/Test/Deploy      Image Registry

Operations VM
    |
    +---- Ansible ------> Linux servers
    |
    +---- Terraform ----> Floci / AWS resources

Linux virtual machines
    |
    v
Kubernetes
    |
    v
Application workloads

Application / Infrastructure
    |
    v
OpenTelemetry
    |
    +--> Metrics
    +--> Logs
    +--> Traces
            |
            v
         Grafana
            |
            v
          Alerts
```
## Deployment Evolution

The system will deliberately evolve through:

1. manually operated Linux services
2. Docker containers
3. Docker Compose
4. Kubernetes

This progression exists for learning purposes.

## Infrastructure Model

The Windows desktop acts as the physical host.

Planned Linux VMs:

- Kubernetes control plane
- Kubernetes worker 1
- Kubernetes worker 2
- operations/management server

The operations server will eventually host or control tools such as Jenkins,
Ansible, Terraform, Git tooling, and local cloud emulation.

## Cloud Model

The project will use:

1. local infrastructure as simulated on-premises infrastructure
2. Floci for local cloud API/resource emulation
3. limited real AWS resources for final validation

Local cloud emulation must not be described as equivalent to production AWS
experience.

## Design Priority

Infrastructure behavior, observability, failures, troubleshooting, and
operational understanding take priority over application feature complexity.

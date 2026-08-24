# Distributed Reliability Lab Project Plan

## Objective

Build a locally operated, backend-focused distributed system that provides
hands-on experience with infrastructure engineering, DevOps, SRE, cloud,
production support, and troubleshooting.

The system will progressively evolve from manually managed Linux services into
a containerized and Kubernetes-orchestrated platform.

## Target System

Synthetic Generator / External API
→ Ingestion API
→ Kafka
→ Worker Consumers
→ PostgreSQL
→ Query API

Redis may provide caching where justified.

Supporting platform:

GitHub
→ Jenkins
→ build/test/deploy

Terraform
→ infrastructure/cloud resources

Ansible
→ Linux/server configuration

OpenTelemetry
→ Prometheus / logs / traces
→ Grafana
→ alerts

Floci
→ simulated cloud resources

AWS
→ limited real-cloud validation later

## Phases

### Phase 0: Repository Foundation
- repository structure
- documentation foundation
- architecture foundation
- Git workflow

### Phase 1: Virtual Infrastructure
- select/configure hypervisor
- create Ubuntu Server VMs
- virtual networking
- hostname/IP plan
- SSH
- DNS/name resolution
- firewall baseline

Target environment:
- Kubernetes control-plane VM
- Kubernetes worker VM 1
- Kubernetes worker VM 2
- operations VM

### Phase 2: Linux Administration
Manually learn and configure:
- users/groups
- permissions
- sudo
- SSH
- packages
- processes
- systemd
- journald
- storage/filesystems
- networking
- firewall
- resource monitoring
- log rotation

Begin Linux and networking failure labs.

### Phase 3: Backend Application
Build:
- synthetic event generator
- FastAPI ingestion API
- processing worker
- query API

Keep business functionality intentionally small.

### Phase 4: Data and Messaging
Add:
- PostgreSQL
- Redis where justified
- Apache Kafka using KRaft

Learn producers, consumers, topics, partitions, offsets, consumer groups,
backpressure, retries, and idempotency.

### Phase 5: Containers
Progress from:
Linux processes
→ Docker
→ Docker Compose

Containerize application services and practice container troubleshooting.

### Phase 6: Jenkins CI/CD
Build a pipeline covering:
- checkout
- lint
- test
- build
- image creation
- image publishing
- deployment
- smoke testing
- deployment verification

### Phase 7: Ansible
After manual Linux configuration is understood, automate server configuration
with Ansible.

### Phase 8: Terraform and Cloud Emulation
Use Terraform with Floci to practice cloud-style infrastructure and AWS APIs.

Introduce selected services only when the architecture needs them.

### Phase 9: Kubernetes
Build:
- one control plane
- two workers

Migrate application workloads from Compose to Kubernetes.

Practice:
- Deployments
- Services
- ConfigMaps
- Secrets
- resource limits
- probes
- storage
- ingress
- RBAC
- NetworkPolicies

### Phase 10: Observability
Implement:
- structured logs
- OpenTelemetry
- Prometheus
- Grafana
- centralized logging when needed
- distributed tracing

### Phase 11: Reliability Engineering
Define:
- SLIs
- SLOs
- error budgets
- alerting policies

### Phase 12: Load and Capacity Testing
Generate controlled load and determine:
- throughput
- bottlenecks
- latency
- saturation behavior
- scaling behavior
- recovery behavior

### Phase 13: Failure Engineering
Continuously inject failures across:
- Linux
- networking
- containers
- Kubernetes
- Kafka
- PostgreSQL
- Jenkins
- Ansible
- Terraform
- IAM/access control
- deployments

Create incident records, postmortems, and runbooks.

### Phase 14: Security and Access Control
Practice:
- least privilege
- SSH keys
- service accounts
- secrets
- Kubernetes RBAC
- IAM
- TLS
- credential rotation

### Phase 15: External Data
Replace or supplement synthetic events with a free external API.

Practice:
- rate limits
- retries
- timeouts
- schema changes
- external dependency failures

### Phase 16: Hybrid Environment
Operate local infrastructure while consuming simulated cloud resources.

### Phase 17: Real AWS Validation
Deploy a small subset against real AWS to validate:
- Terraform
- IAM
- cloud APIs
- differences between emulation and real cloud

Avoid recreating the entire environment in AWS.

## Core Learning Pattern

Understand
→ configure manually
→ verify
→ automate
→ break
→ troubleshoot
→ document

The project is complete when the user can confidently explain, operate,
troubleshoot, and defend the major architectural decisions, rather than merely
having all components deployed.

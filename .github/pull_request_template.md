## Summary

<!-- What problem does this pull request solve? Keep this concise. -->

## Change type

- [ ] New feature or capability
- [ ] Bug fix
- [ ] Reliability or performance improvement
- [ ] Infrastructure or deployment change
- [ ] Observability or alerting change
- [ ] Security change
- [ ] Documentation or configuration change
- [ ] Breaking change

## Scope and affected components

<!-- Identify services, libraries, infrastructure, data stores, and environments affected. -->

- Components:
- Environments:
- Interfaces or APIs affected:
- Data schemas, topics, queues, or storage affected:

## Architecture and design impact

<!-- Explain any change to data flow, service boundaries, dependencies, or failure behavior. -->

- Architecture impact:
- New or changed dependencies:
- ADR required or updated: <!-- Link an ADR, or write "Not applicable". -->

## Reliability and operational impact

- [ ] Failure modes and degraded behavior were considered.
- [ ] Timeouts, retries, backpressure, and idempotency behavior were reviewed where applicable.
- [ ] Resource impact was considered (CPU, memory, storage, connections, partitions, or network).
- [ ] Availability, latency, throughput, or data-loss implications are documented.
- [ ] Runbook or operational documentation is updated, or no update is needed.

Expected operational impact:

## Observability

- Metrics added or changed:
- Logs added or changed:
- Traces added or changed:
- Alerts or SLOs affected:
- Dashboard or query links:
- [ ] The change is observable in the affected environment.

## Security and data handling

- [ ] Authentication and authorization implications were reviewed.
- [ ] Secrets and credentials are not committed.
- [ ] Sensitive data handling and logging were reviewed.
- [ ] Least-privilege implications were considered.
- [ ] Security documentation or controls were updated where required.

## Testing and verification

<!-- Include commands, test results, and links to relevant evidence. -->

Tests run:

```text
# Example:
# pytest
# docker compose config
# kubectl apply --dry-run=client -f ...
```

Verification evidence:

- [ ] Unit tests
- [ ] Integration tests
- [ ] Failure or recovery testing
- [ ] Configuration or manifest validation
- [ ] Manual verification
- [ ] Not applicable, with explanation below

## Deployment, rollout, and rollback

- Rollout plan:
- Rollback or recovery plan:
- Migration or compatibility considerations:
- Required feature flags, configuration, or secrets:
- [ ] The change can be deployed incrementally, or the limitation is documented.
- [ ] Rollback has been tested, or the reason it cannot be tested is documented.

## Risk assessment

- Risk level: <!-- Low / Medium / High -->
- Main risks:
- Mitigations:
- Conditions that should block deployment:

## Reviewer notes

<!-- Call out decisions, tradeoffs, uncertainties, or areas needing special review. -->

## Author checklist

- [ ] The change is limited to the stated scope.
- [ ] Documentation is updated where behavior or operations changed.
- [ ] Tests and verification evidence are included.
- [ ] No credentials, private keys, tokens, or other secrets are committed.
- [ ] Backward compatibility was considered.
- [ ] The pull request is ready for review.

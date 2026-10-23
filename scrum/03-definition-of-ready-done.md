# Definition of Ready and Definition of Done

## Definition of Ready (team working agreement)

A backlog item is ready for Sprint Planning when:
- user/business outcome is clear;
- acceptance criteria are testable;
- dependencies and external-provider assumptions are identified;
- UX/API/data behavior is sufficiently understood;
- security/privacy implications have been considered;
- the item is small enough to complete in one Sprint (split it if not);
- the team has an estimate or agreed sizing approach;
- required credentials, test data, and environments are available or have a plan.

This is a team aid, not a gate that should block all discovery work.

## Definition of Done

A Product Backlog Item is Done only when:
- implementation meets acceptance criteria;
- code is reviewed and follows module boundaries;
- automated tests cover relevant behavior and failure cases;
- tenant isolation and authorization are tested where relevant;
- input validation and error handling are implemented;
- database migrations are reviewed and repeatable;
- logs/metrics/traces include safe correlation fields;
- sensitive values are redacted;
- documentation/API contracts are updated;
- no known critical/high-severity defect remains without explicit risk acceptance;
- deployment/rollback or feature-flag behavior is understood;
- product owner can inspect the completed behavior.

## AI-specific Done checks
- model and prompt/config version are identifiable;
- tool schemas are validated;
- tool permissions are enforced in code;
- retrieval is tenant-scoped;
- failure, empty retrieval, and uncertainty paths are tested;
- a regression example is added for important behavior;
- no secrets or hidden reasoning are persisted in logs.

## Voice-specific Done checks
- microphone permission and active state are clear;
- session cleanup works on disconnect;
- interruption/cancellation behavior is tested;
- transcript finalization and ordering are tested;
- audio/transcript retention follows policy;
- latency and failure metrics are emitted.

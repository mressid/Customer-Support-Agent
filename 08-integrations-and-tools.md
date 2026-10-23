# 08 — Integrations and Tool Contracts

## Connector architecture

Use three layers:

1. **Tool definition:** what the AI may request, with a stable name, description, input schema, output schema, and risk classification.
2. **Tool execution service:** validation, authorization, idempotency, audit, timeout, and result normalization.
3. **Connector adapter:** provider-specific authentication, endpoint calls, payload mapping, and error interpretation.

Example:
`AI engine → orders.lookup tool → tool execution service → commerce connector → commerce API`

The AI should never receive raw integration credentials or unrestricted HTTP access.

## Tool definition fields

- stable tool name, e.g. `orders.lookup`;
- human-readable description;
- version;
- JSON input schema;
- output schema;
- allowed agent/tenant scope;
- required permission;
- risk level: read-only, reversible write, sensitive write;
- confirmation/approval requirement;
- timeout and retry policy;
- idempotency behavior;
- audit and redaction policy.

## Example: read-only order lookup

```json
{
  "name": "orders.lookup",
  "version": 1,
  "risk": "read_only",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_reference": {
        "type": "string",
        "minLength": 3,
        "maxLength": 80
      }
    },
    "required": ["order_reference"],
    "additionalProperties": false
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "status": {"type": "string"},
      "estimated_delivery": {"type": ["string", "null"]}
    },
    "required": ["status", "estimated_delivery"],
    "additionalProperties": false
  }
}
```

This is a contract example, not a claim that any particular commerce provider uses this schema.

## Error mapping

Normalize connector failures into categories:
- `AUTHENTICATION_FAILED`
- `AUTHORIZATION_DENIED`
- `NOT_FOUND`
- `VALIDATION_FAILED`
- `RATE_LIMITED`
- `TIMEOUT`
- `PROVIDER_UNAVAILABLE`
- `CONFLICT`
- `UNKNOWN_OUTCOME`

Only retry failures that are safe to retry. For writes, an unknown outcome may require a status lookup or human review instead of blind retry.

## Webhook handling

1. Verify provider signature and timestamp.
2. Resolve the configured channel/integration from trusted endpoint configuration.
3. Enforce body size and schema limits.
4. Persist event ID and payload/minimal normalized data.
5. Return success only after durable acceptance.
6. Process asynchronously.
7. Deduplicate provider retries.
8. Record processing state and failure reason without leaking secrets.

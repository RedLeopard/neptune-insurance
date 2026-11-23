# Neptune Insurance lookup requests

Synthetic request fixtures for NeptuneInsuranceLookup. The Details.Parameters
envelope matches the parameters delivered by a Connect Lambda block.

| File | Expected resultCode | Expected status |
| --- | --- | --- |
| claim-owned.json | OK | IN_REVIEW |
| policy-owned.json | OK | ACTIVE |
| claim-not-found.json | NOT_FOUND | empty |
| claim-unauthorized.json | UNAUTHORIZED | empty |
| malformed-reference.json | MALFORMED | empty |
| unexpected-identity.json | MALFORMED | empty |

Fixture creation is not evidence of test execution. Record actual invocations
and request IDs separately. All non-OK responses must have empty reference,
status and product fields. All responses must contain only resultCode,
reference, status, product and requestId, with String values.

The synthetic identity is configured server-side as DEMO_CUSTOMER_ID=DEMO-1001.
The request cannot select its customer identity. This demonstrates ownership
checks; it does not implement real customer authentication.

Public conversation wording should not disclose whether another customer's
record exists. NOT_FOUND and UNAUTHORIZED use the same generic retrieval
fallback. Internal result codes remain available for operational diagnosis.

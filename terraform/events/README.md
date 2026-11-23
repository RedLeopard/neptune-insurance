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

## Verified invocation

On November 23, 2026, the supplied terminal output showed a direct invocation
of claim-owned.json returning StatusCode 200 without FunctionError, followed by
resultCode OK, reference CLM-1001, status IN_REVIEW and product AUTO.
RequestId: aeccfc07-5077-4309-a495-62d02de4ea8f.
The response contained only the five approved fields.

This proves that one direct claim lookup, not a live Connect conversation,
completed successfully. The other cases remain pending until their actual
results are recorded.

Run the remaining checks from the existing local checkout:

```bash
python3 "$HOME/NeptuneInsurance/terraform/scripts/test-lookup.py"
```

The runner uses the installed AWS CLI and Python standard library. It invokes
only the five cases not yet verified above, checks invocation errors, exact
response fields, String types, nonempty request IDs, and expected business
values, and prints each requestId. It stops on the first failure.
Responses are temporary local files; no AWS resources are created or modified.

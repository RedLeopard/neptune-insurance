# Neptune Insurance lookup verification

Observed results from terminal output supplied on November 23, 2026.
The function is NeptuneInsuranceLookup in us-west-2, using Python 3.13,
handler neptune_insurance_lookup.lambda_handler, 128 MB memory and a normal
3-second timeout. Synthetic customer context is DEMO-1001.

| Request | Observed result | Request ID |
| --- | --- | --- |
| claim-owned | OK / CLM-1001 / IN_REVIEW / AUTO | aeccfc07-5077-4309-a495-62d02de4ea8f |
| policy-owned | OK / POL-1001 / ACTIVE / AUTO | fa463928-dd5e-4eed-ab9f-910640e09faa |
| claim-not-found | NOT_FOUND; data fields empty | 1d024b3c-9d6e-4b51-b039-59b5365dbe58 |
| claim-unauthorized | UNAUTHORIZED; data fields empty | e5c72368-c137-40d0-81ab-0cec6680db16 |
| malformed-reference | MALFORMED; data fields empty | 4a29994d-09ff-421a-ae7a-9c424f33ab1e |
| unexpected-identity | MALFORMED; data fields empty | 936c43d7-0e73-4be5-a899-4d169ccac370 |

The five-case runner checked successful invocation metadata, exact approved
response fields, String values, nonempty request IDs and expected business
values. The first claim response also visibly contained only the five approved
fields. Internal notes and ownerId were not returned. This demonstrates the
service response boundary for these synthetic records and requests.

## Pending

- Connect invocation permission and Lambda association.
- Published lookup module and Agentic CX data request.
- Real conversational lookup with backend correlation.
- Previously outstanding live agent delivery and received context.

The fixed synthetic customer ID demonstrates ownership checks; real customer
authentication is not implemented. Direct Lambda tests are separate from live
Connect conversation or agent-delivery evidence.

## Timeout check

Run terraform/scripts/test-timeout.py only while this function remains isolated
from live customer traffic. It checks the verified baseline, snapshots the
current timeout and complete environment map in memory, injects a bounded delay,
and attempts restoration in a finally block even if the test fails.
It waits for configuration updates, verifies restoration and then runs one
claim lookup to prove recovery. Request fixtures and local environment.json are
not changed. AWS invocations generate normal logging and usage.

Expected output includes controlled-timeout, restored-settings and recovery
PASS messages. A STOP or FAIL result must be resolved before integration. If the
process is forcibly terminated or AWS access is lost, verify and restore the
normal timeout/environment before using the function.

## Timeout and recovery observed

The supplied terminal output confirmed the controlled timeout and subsequent
recovery on November 23, 2026:

- Fault settings: Timeout=1 second, LOOKUP_DELAY_SECONDS=2.
- Runtime error: Sandbox.Timedout, task timed out after 1.00 seconds.
- Timeout RequestId: 1e39eb65-08b5-4edc-86bf-795a19f6969b.
- Original settings restored and checked: Timeout=3, delay=0.
- Recovery claim lookup returned OK.
- Recovery RequestId: f6043775-2c91-490c-8c02-96dbe48b16ad.

This verifies the direct Lambda timeout/recovery drill. Connect routing of an
invocation error or timeout remains separate integration work.

## Connect setup source

connect/lambda-permission.json scopes lambda:InvokeFunction to the existing
Neptune Connect instance and account. connect/lambda-association.json identifies
that instance and this lookup function. These are AWS CLI request documents,
not proof that either change has been applied.

# Neptune Insurance lookup verification

Checkpoint: November 23, 2026 (America/Chicago). **Day 9 complete (9/14). Remaining live-call verification and troubleshooting start Day 10.**
The owner stopped testing for the evening. The latest phone attempt was reported
unsuccessful; no successful end-to-end voice lookup is claimed.

## Configuration saved or reported

- DynamoDB: `NeptuneInsuranceLab`, on-demand, String partition key `pk`; three synthetic records seeded and checked.
- Lambda: `NeptuneInsuranceLookup`, Python 3.13, handler `neptune_insurance_lookup.lambda_handler`, 128 MB, normal timeout 3 seconds.
- Execution role: Lambda service trust; GetItem scoped to the lab table; basic CloudWatch execution logging.
- Connect: scoped Lambda resource permission and function association confirmed through supplied terminal output. The earlier association permission failure was resolved.
- Contracts: required String inputs `recordType` and `reference`; exactly five String outputs: `resultCode`, `reference`, `status`, `product`, `requestId`.
- The selected externally invocable tool is `NeptuneInsuranceLookupModule-Copy`. The original `NeptuneInsuranceLookupModule` was published but its tool flag remained false. Capture the copy's actual ID/version in the private deployment record on return.
- Data request: `NeptuneInsuranceLookup`, Connect flow module implementation, selected tool copy, and a clearly labeled mock response.
- Claim conversation: User choice Match enters the Data request; Success enters Split; an OK result enters the Basic response and Exit application. Other result codes, Failure and Timeout use the existing NeptuneRecovery redirect. In-progress is unconnected in the last supplied export; review whether that optional edge should be disabled before final acceptance.
- Application build/deployment was owner-reported; the final build/environment identifiers were not captured. The phone flow uses a keypad menu: press 3 before speaking to the AI.

## Evidence reviewed

| Check | Evidence and outcome |
| --- | --- |
| Canonical owned claim | Direct Lambda output: OK, CLM-1001, IN_REVIEW, AUTO |
| Canonical owned policy | Direct Lambda output: OK, POL-1001, ACTIVE, AUTO |
| Missing claim | Direct runner: NOT_FOUND with empty data fields |
| Different owner | Direct runner: UNAUTHORIZED with empty data fields |
| Malformed reference | Direct runner: MALFORMED |
| Unexpected caller-supplied identity | Direct runner: MALFORMED |
| Field filtering | Response contained only the five approved fields; internal notes and ownerId were excluded |
| Timeout and recovery | Controlled 1-second timeout with a 2-second delay; timeout observed; original 3-second timeout and zero delay restored; recovery lookup returned OK |
| Mock conversation | Data request returned the mock OK/IN_REVIEW response; after correcting the Split and message variable, the pasted transcript displayed IN_REVIEW |
| Real phone routing | Caller pressed 3, reached the AI, and invoked Lambda; CloudWatch showed MALFORMED |
| Input diagnostic | Lambda received a spoken sentence in reference instead of a canonical identifier |
| Normalizer code | Commit 87f0e94 adds bounded conversion of spoken references; seven offline test groups passed |
| Post-change direct checks | Eight-case AWS CLI runner added; owner reported executing the commands, but its output was not supplied |
| Latest real phone attempt | Owner reported failure after the normalizer update; no post-fix response/log was supplied |

The fixed synthetic customer context is a demonstration, not real customer
authentication. Authorization and field filtering remain enforced in Lambda.
The model and a reference number are not authorization decisions.

## Spoken-reference change

The observed spoken form was equivalent to “It's claim one thousand and one.”
The normalizer converts supported four-digit/spoken forms to the canonical
CLM-1001 shape before strict validation. It also supports corresponding policy
references. It rejects unrecognized/ambiguous text and never searches for or
guesses a record. Offline tests cover this phrase, other numbers, wrong-owner
access, missing records, malformed/injection text and extra identity fields.

The release source omits the temporary raw-input diagnostic. Deployment of that
release was owner-reported. Verify the active code and fresh invocation timestamps
when resuming rather than inferring deployment state from an older log.

## Approved output/context boundary

| Field | Permitted use in this synthetic lab |
| --- | --- |
| resultCode | Deterministic routing; an executed request is not automatically an authorized lookup |
| reference | Canonical returned reference only after OK; a collected slot is not proof of ownership |
| status | Display/reuse only after OK and the backend ownership check |
| product | Display/reuse only after OK |
| requestId | Diagnostic correlation; not customer authentication |
| ownerId / internalNotes | Never returned to the conversation or copied to cross-channel customer context |

This table defines the reuse boundary. It does not claim lookup outputs have
already been persisted into cross-channel context variables; that mapping and
continuity validation remain separate work.

## Start Day 10 — carried-over live verification

1. Obtain fresh logs for the latest failed phone attempt and confirm the deployed Lambda package.
2. Confirm the Data request still targets the published tool copy and the phone uses the intended deployed application environment.
3. Inspect the actual captured reference and module input mapping; distinguish speech normalization, parameter binding and backend failures.
4. Resolve the failure, then obtain one real OK/IN_REVIEW response with backend correlation.
5. Capture a final corrected claim-flow export and tool-copy export. The last supplied claim export predates later successful mock corrections; do not archive it as the final live configuration.
6. Capture any remaining controlled not-found/unauthorized/error/timeout routing evidence without repeating the completed direct timeout drill unnecessarily.
7. Finish the authorization/system-of-record explanation, then revisit deferred Terraform adoption.

Earlier follow-ups remain open: live agent acceptance with received handoff
context and the full quick-connect retest. None requires additional configuration
tonight. Day 9 is marked complete per the owner's decision; Day 10 begins with the outstanding tests. This completion marker does not assert a successful live lookup.

# Neptune Insurance lookup verification

Checkpoint: November 24, 2026 (America/Chicago). **Carried-over CLM-1001 troubleshooting and testing DONE.** Day 9 remains complete (9/14); the main Day 10 syllabus is not complete. Portfolio/page updates wait until Day 10 finishes.

All eight direct checks passed. A real phone call using individual digits returned Lambda OK and the caller heard IN_REVIEW. After the follow-up question was configured, the owner confirmed the problem fixed and requested testing marked done.

## Configuration saved or reported

- DynamoDB: `NeptuneInsuranceLab`, on-demand, String partition key `pk`; three synthetic records seeded and checked.
- Lambda: `NeptuneInsuranceLookup`, Python 3.13, handler `neptune_insurance_lookup.lambda_handler`, 128 MB, normal timeout 3 seconds.
- Execution role: Lambda service trust; GetItem scoped to the lab table; basic CloudWatch execution logging.
- Connect: scoped Lambda resource permission and function association confirmed through supplied terminal output. The earlier association permission failure was resolved.
- Contracts: required String inputs `recordType` and `reference`; exactly five String outputs: `resultCode`, `reference`, `status`, `product`, `requestId`.
- The selected externally invocable tool is `NeptuneInsuranceLookupModule-Copy`. The original `NeptuneInsuranceLookupModule` was published but its tool flag remained false. Capture the copy's actual ID/version in the private deployment record on return.
- Data request: `NeptuneInsuranceLookup`, Connect flow module implementation, selected tool copy, and a clearly labeled mock response.
- Claim conversation: User choice Match enters the Data request; Success enters Split; an OK result enters the Basic status response, then a separate User choice asking whether more help is needed. Its intended Yes path redirects to NeptuneWelcome, No exits, and No match uses NeptuneRecovery. Other result codes, Failure and Timeout use the existing NeptuneRecovery redirect. In-progress is unconnected in the last supplied export; review whether that optional edge should be disabled before final acceptance.
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
| Post-change direct checks | Supplied terminal output: 8/8 passed, including the spoken-reference case and authorization/error checks |
| Latest verified live lookup | 2026-11-24T21:32:31Z: Lambda OK; owner confirmed spoken IN_REVIEW after saying individual digits |
| Continuation fix | Supplied flow (7) has status → User choice, two value paths to welcome/exit, and No match → recovery; owner confirmed problem fixed and testing done |

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

Temporary bounded synthetic-input validation diagnostics were added in commit 727cdaef. They identified the unsupported live capture "Just calling one thousand and one." The next call using "one zero zero one" succeeded. The prompt was changed to request individual digits; unsupported conversational text remains rejected. Diagnostic logging remains in source.

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

## Completed carryover and remaining scope

- [x] Active Lambda configuration inspected; eight direct checks passed.
- [x] Live failure isolated to unsupported captured reference wording.
- [x] Real voice lookup returned OK and spoken IN_REVIEW.
- [x] Individual-digit prompt and separate continuation question configured.
- [x] Corrected claim-flow export archived: [NeptuneClaimStatus.flow.json](../connect/agentic/NeptuneClaimStatus.flow.json).
- [x] Owner confirmed the problem fixed and testing done.

The graph review confirms all explicit local node targets exist. Yes/No are stored as custom value IDs; the custom NeptuneContinueChoice resource must also exist in an importing workspace. The supplied flow does not include that slot resource, the external tool module, or deployment identifiers. The optional Data request In progress edge remains enabled/unconnected in the supplied export; its behavior is not certified by the successful synchronous lookup.

No separate live transcript was supplied for every continuation/error branch. Earlier live agent acceptance/context, quick-connect retest, final module/slot export packaging and unexecuted live failure checks remain separate follow-ups. Continue the actual Day 10 material without replaying the completed lookup troubleshooting. Portfolio/page updates are deferred until Day 10 is finished.

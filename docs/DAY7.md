# Day 7 | Conversational application v0.1.0

Reported completion: November 21, 2026 (America/Chicago).

## Saved configuration

Workspace: `Neptune Insurance Lab`. Application: `NeptuneInsurance`. Deployment: **v0.1.0**, shown **Live** with a successful deployment summary.

| Flow | Behavior |
| --- | --- |
| NeptuneWelcome | Start → User input; Flow recognized → Redirect to Recognized flow; No flow recognized → Redirect to NeptuneRecovery |
| NeptuneRecovery | Start → Basic recovery message → Exit application |
| NeptuneBilling | Start → Basic billing acknowledgement → Exit application |
| NeptuneNewAutoClaim | Introduction → policy reference → loss type → loss date → drivable → recap/confirmation → bounded ending |
| NeptuneClaimStatus | Collect claim reference → repeat reference → Exit application; no live status lookup |

Application defaults: Welcome → NeptuneWelcome; Fallback, Unknown, and Incomprehension → NeptuneRecovery.

## Nodes and state

Start begins the flow; Basic displays a fixed message; User input recognizes a request; User choice resolves an answer into a slot; Redirect changes flows; Exit application returns to the calling contact flow. Canvas connections define execution order.

| Attached slot | Type |
| --- | --- |
| policyReference | NLX.Text |
| lossType | NeptuneLossType: Collision, Theft, Other |
| lossDate | NLX.Date |
| drivable | NeptuneYesNo: Yes, No |
| intakeConfirmed | NeptuneYesNo: Yes, No |
| claimReference (Claim Status) | NLX.Text |

All five claim-intake No match paths lead to shared recovery. All three loss-type outputs continue to the date question. Both drivable values continue to confirmation. Confirmation Yes ends with details confirmed; No ends with a restart instruction. Neither files a claim.

Saved confirmation message:

```text
Your policy reference is {policyReference:NLX.Text}. The loss type is {lossType:NeptuneLossType}, occurring on {lossDate:NLX.Date}. Vehicle drivable: {drivable:NeptuneYesNo}. Are these details correct? Please answer yes or no.
```

Curly braces mark a substitution; the colon separates the attached slot name from its exact type. The names and types must match the attached slots. Generic NLX.Slot references produced type-change validation errors and were replaced.

## Evidence and limits

| Evidence | Result |
| --- | --- |
| Supplied claim-flow JSON | 11 nodes reachable; required graph targets exist; four recap placeholders match attached types; five No match paths reach recovery |
| Deployment summary pasted from console | v0.1.0 successful and Live |
| Billing transcript and debugger | Billing request recognized NeptuneBilling; acknowledgement followed by Default exit |
| Unsupported-request transcript | Pizza request reached recovery and Default exit |
| Remaining intake tests | Learner reported success; full test matrix and transcripts not independently reviewed |

The NLU Billing confidence score was 90; this is a match score, not measured accuracy. Default exit is expected for these bounded flows and does not demonstrate a human-agent handoff.

The [claim flow export](../connect/agentic/NeptuneNewAutoClaim.flow.json) is one flow, not a complete application backup. It depends on NeptuneRecovery and the separately defined custom slot types and value IDs. It does not include application attachment/default settings or deployment bindings. Review dependencies before importing into another workspace.

## Next dependency

Day 8: controlled AI actions, guardrails, and explicit AI-to-human handoff. The application has not yet been connected to the phone entry or customer website. Backend lookup, claim filing, and cross-channel continuity remain future work. The separate Day 6 quick-connect retest remains open.

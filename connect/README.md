# Neptune inbound voice lab

**Demo number:** [1-800-810-5374](tel:+18008105374)  
**Flow:** `Neptune-Inbound-Voice`  
**Snapshot:** November 19, 2026, Day 5, before the four live voice tests.

The supplied AWS export has `Metadata.status: PUBLISHED` and 21 blocks. The supplied phone-number configuration associates the existing demo number with this flow. The JSON is configuration evidence; it does not prove successful calls or agent delivery.

## Flow behavior

Entry enables flow logging, checks for the VOICE channel, plays the welcome, checks the explicitly selected lab-hours schedule, then presents the menu. Non-voice contacts disconnect. Closed hours play an after-hours message and disconnect. Operational errors use the technical fallback.

| Menu selection | Saved business context | Destination |
| --- | --- | --- |
| 1 | `menuSelection=1`, `serviceLine=PolicyService` | Policy acknowledgement and disconnect; no policy agent transfer yet |
| 2 | `menuSelection=2`, `serviceLine=Billing` | Billing acknowledgement and disconnect; no billing agent transfer yet |
| 3 | `menuSelection=3`, `serviceLine=AutoClaims` | Claims context check, acknowledgement, Set working queue, Transfer to queue |

Invalid input or silence receives one retry with the same options and a five-second input timeout. A second invalid or silent attempt reaches the final goodbye and disconnect. Both menus route technical errors to the technical fallback. Queue capacity and transfer errors have connected messages and terminal handling.

Set working queue selects Auto Claims; Transfer to queue performs the enqueue. Successful inbound enqueue continues into the queue experience and agent routing, rather than an inbound Success connector to Disconnect.

The website's browser-only claims form is separate from this voice path. It does not pass claim details to an agent. The number is voice-only in this lab; SMS, live chat and email integration are not established here.

## Public template and resource bindings

[`flows/Neptune-Inbound-Voice.json`](flows/Neptune-Inbound-Voice.json) preserves the exported block graph, names, prompts and settings. The source AWS account, instance, hours and queue identifiers have been replaced consistently in action parameters and designer metadata. The original export remains private.

| Placeholder | Replace with |
| --- | --- |
| Account `000000000000` | Your destination AWS account |
| Instance `00000000-0000-0000-0000-000000000000` | Your destination Connect instance |
| Hours `11111111-1111-1111-1111-111111111111` | Your dedicated `Neptune-Lab-Hours` resource |
| Queue `22222222-2222-2222-2222-222222222222` | Your existing Auto Claims queue |

This is a sanitized template, not a directly runnable export for the source account. The copied `PUBLISHED` metadata describes the original export; importing the file does not publish it.

1. Import into an isolated lab flow in the intended Connect instance.
2. In **Check Neptune Hours**, select the dedicated `Neptune-Lab-Hours` resource explicitly. The separate schedule is not included in this JSON. The original lab schedule is America/New_York, every day 12:00 AM–11:59 PM.
3. In **Set Auto Claims Queue**, select the actual existing Auto Claims queue. Agent profiles, capacity, queue experience and user configuration are separate resources.
4. Confirm instance-level flow logging and its CloudWatch destination. This file contains the flow-level logging block only.
5. Review every connection, Save, and Publish. Associate only an authorized lab entry with the intended published flow.

## Runtime evidence still pending

| Test | Required observation | Status |
| --- | --- | --- |
| T01 | Press 3, Elena accepts, confirm two-way audio, end contact and wrap-up | Pending |
| T02 | Press 9 twice; one retry, final goodbye, disconnect | Pending |
| T03 | Remain silent twice; one retry, final goodbye, disconnect | Pending |
| T04 | Temporarily close dedicated lab hours, hear after-hours treatment, restore and reopen original hours | Pending |

Use the approved short-call scope with a one-minute manual stop for each test. Record the version, time, actual outcome and ContactId or private evidence reference. Keep customer data, actual call recordings and private trace details out of this public repository.

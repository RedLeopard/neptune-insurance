# Neptune inbound voice lab

**Demo number:** [1-800-810-5374](tel:+18008105374)  
**Flow:** `Neptune-Inbound-Voice`  
**Current source snapshot:** November 22, 2026, Day 8; sanitized from `Neptune-Inbound-Voice (27).json`.

The supplied snapshot has PUBLISHED metadata and **26 reachable blocks**. Its graph has no empty or missing targets. It configures voice entry, Billing routing and the Agentic CX / Auto Claims handoff path. A static export is not proof of successful calls or agent receipt of context.

**Provenance:** this is the latest provided export, captured before the final reported language-attribute correction and republish. It contains Joanna but no explicit language attribute. The owner subsequently reported enabling English (United States) and publishing; the final post-correction export has not been supplied. The public template intentionally preserves that distinction rather than inventing an export.

## Configured journey

Entry → flow logging → VOICE channel check → Neptune AI Voice → welcome → dedicated lab-hours check → three-choice menu. Invalid input or silence has one retry. Closed hours and technical failures have bounded exits.

| Selection | Context | Destination |
| --- | --- | --- |
| 1 | menuSelection=1; serviceLine=PolicyService | Policy acknowledgement and disconnect |
| 2 | menuSelection=2; serviceLine=Billing | Billing acknowledgement → Set Billing Queue → Transfer to Billing |
| 3 | menuSelection=3; serviceLine=AutoClaims | Check Claims Service → Neptune Agentic CX |

| Agentic CX output | Configured destination |
| --- | --- |
| Escalation | Neptune Save AI Handoff → Set Auto Claims Queue → Transfer to Auto Claims |
| Error | Claims acknowledgement → existing Auto Claims queue path |
| Default | Disconnect / hang up |
| Idle chat timeout | Technical fallback prompt; chat-only behavior, unused by this voice path |

All five returned values are dynamically copied into Current contact / User defined attributes. Set working queue chooses the destination; Transfer to queue enqueues. Agent delivery still depends on routing eligibility, state and capacity. See [Day 8 settings and evidence](../docs/DAY8.md).

The public export stores Default in the Agentic CX block's `NoMatchingCondition` transition. Its `NextAction` duplicates the Error destination; do not misread that as a Default-to-queue connection.

## Public template and resource bindings

[`flows/Neptune-Inbound-Voice.json`](flows/Neptune-Inbound-Voice.json) preserves the supplied graph, block names, prompts, dynamic mappings and voice settings. Source account, instance, hours, queue, workspace, application and deployment-alias identifiers are replaced consistently in parameters and designer metadata. The original resource bindings are not published.

| Placeholder | Replace with |
| --- | --- |
| Account 000000000000 | Destination AWS account |
| Instance 00000000-0000-0000-0000-000000000000 | Destination Connect instance |
| Hours 11111111-1111-1111-1111-111111111111 | Dedicated Neptune-Lab-Hours resource |
| Queue 22222222-2222-2222-2222-222222222222 | Existing Auto Claims queue |
| Queue 33333333-3333-3333-3333-333333333333 | Existing Neptune-Billing queue |
| Workspace 44444444-4444-4444-4444-444444444444 | Destination Agentic CX workspace |
| Application 55555555-5555-5555-5555-555555555555 | Existing NeptuneInsurance application |
| RESELECT_DEPLOYED_ALIAS | Deployment alias/key selected through the Agentic CX block's dropdowns |

This is a sanitized source snapshot, **not directly runnable** against either AWS account. Importing retained PUBLISHED metadata does not publish the destination flow. The JSON does not include the Designer application, guardrail definitions, schemas, queues, agents, routing profiles or hours schedule.

1. Import only into the intended isolated lab flow.
2. Rebind Check Neptune Hours, Set Auto Claims Queue and Set Billing Queue to the correct destination resources. The original dedicated schedule was reported as America/New_York, every day 12:00 AM–11:59 PM; verify rather than assuming it is included.
3. In Neptune Agentic CX, reselect workspace, application and the actual deployed alias, then Confirm. Ensure the Designer resources in [DAY8.md](../docs/DAY8.md) exist and the intended build is deployed.
4. In Neptune AI Voice, select the matching application language and explicitly enable Set language attribute. This is the final reported correction missing from the provided snapshot.
5. Confirm instance-level logging and appropriate queues, eligible test agents and capacity. Review, save and publish the intended destination flow, then bind the authorized test number.

## Verification still pending

| Test | Required observation | Status |
| --- | --- | --- |
| D8-01 | Press 3, request a representative, eligible agent accepts; confirm two-way audio and returned context | Pending |
| D8-02 | Validate supervisor flag and the supervisor request with downstream contact evidence | App Escalation observed; phone/agent path pending |
| D8-03 | Exercise AI failure and missing context without losing the controlled human fallback | Pending |
| T01–T04 | Archived Day 5 normal routing, bounded invalid input, silence retry, after-hours/recovery tests | Pending |
| D6-Retest | Repeat the Billing-to-Auto Claims quick connect | Pending |

Use synthetic inputs and bounded test calls. Store real ContactIds, unredacted logs and call recordings privately. Website claims remain browser-only; SMS, hosted chat and email integration are not established by this phone-flow configuration.

## November 24 — claim lookup testing complete

The live CLM-1001 lookup returned Lambda OK and the caller heard IN_REVIEW. The owner confirmed the digit-prompt/continuation fix and testing done. The corrected [claim flow export](agentic/NeptuneClaimStatus.flow.json) includes status → follow-up User choice, welcome/exit value paths and No match recovery. Reuse requires the custom NeptuneContinueChoice slot (attached as continueChoice), external lookup tool/data request, and destination flows; these resources are not bundled in this JSON. This closes lookup carryover testing, not the earlier phone-to-agent tests listed above. See [lookup evidence](../terraform/LOOKUP_VERIFICATION.md).

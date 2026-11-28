# Day 14 — Capstone and principal architect defense

**COMPLETE — 14/14 core days, November 28, 2026 (America/Chicago).** Edward Thornton completed the guided session and explicitly accepted core closeout.

## Completed session

| Work | Result / evidence basis |
| --- | --- |
| Auto Claims voice and training-agent exclusion exercise | Completed, owner-reported live test |
| Deployed chat claim lookup and Claims handoff exercise | Completed, owner-reported guided task |
| Coverage/payment guardrail exercise | Completed, owner-reported task; insurance decisions remain outside AI authority |
| New-conversation context exercise | Completed, owner-reported task; automatic authenticated cross-channel continuity is a separate design |
| Contact record and flow-log trace | Completed, owner-reported guided evidence task |
| Follow-up work-item contract | Authored simulation with Claims ownership, due rule and failure handling |
| Operational handoff | Authored; references existing resources and Day 13 runbook |
| Five architecture decisions | Routing specialization, bounded AI/data, identity/context, capacity, and operations/security/cost |
| Five risks and rollout/rollback plan | Traffic spike, lookup/AI outage, unauthorized context, SMS failure and email routing failure |
| Combined failure challenge | Authored tabletop: 10x traffic plus lookup timeout; no disruptive load or outage injected |
| Final defense | Case summary, 10-minute briefing outline and 90-second CIO explanation completed |

Day 14 attribution is the owner's completion reports during the guided session. Earlier transcripts, CLI output and source evidence retain their original provenance. This summary does not manufacture contact identifiers, exact test times or verbatim customer responses.

## Working baseline and SDK evidence

Voice, web chat, two-way SMS and email replies are working lab channels. Existing [Day 10 evidence in the build journal](../PROGRESS.md) also establishes manual Task acceptance/completion; the new Day 14 follow-up contract is a separate simulation. SES/SMS approvals are not being substituted for the actual channel tests.

The Lambda uses **AWS SDK for Python (Boto3)**: `boto3.resource("dynamodb")`, `Table.get_item()`, table-scoped IAM and Botocore connection/read timeout settings with bounded retries. Source was rechecked for this closeout: [Lambda implementation](../terraform/lambda/neptune_insurance_lookup.py). The lookup remains read-only and uses synthetic records/a fixed demonstration principal. Python scripts orchestrating AWS CLI commands are a separate automation approach.

## Architecture decisions and risks

| Requirement | Decision | Alternative / tradeoff | Production evidence |
| --- | --- | --- | --- |
| Specialist Claims service | Explicit Claims eligibility; keep Jordin excluded | Broad catch-all staffing offers flexibility but weakens specialization | Approved overflow staffing and queue behavior |
| Safe conversational service | Bounded AI plus approved read-only tools | A menu-only journey is simpler but less conversational | Unsafe-input, failure and handoff tests |
| New-channel continuity | Verify identity, then retrieve permitted context | Recollection is simpler but repeats customer effort | Authorization and explicit context-source evidence |
| Capacity | Choose concurrency by workload and role | Broad simultaneous handling can increase throughput but overload staff | Forecasts, service targets, quotas and load tests |
| Operability | Scoped access, retention decisions, monitoring ownership and staged release | Broad access/immediate rollout reduces setup work but increases risk | Access review, recovery tests, pricing and monitoring validation |

The risk plan separates traffic overload from lookup failure. Operational responses preserve Claims eligibility, avoid retry storms and use a staffed/available fallback. SMS failure and email backlog have channel owners and explicit recovery. Alert thresholds and automation in the tabletop are design proposals.

## Briefing and case summary

Neptune is a self-directed synthetic Amazon Connect architecture lab combining customer channels, specialist routing, bounded Agentic CX, a Lambda/Boto3/DynamoDB lookup and operational traceability. It demonstrates representative behavior with a small agent set while defining a 500-agent reference design.

Ten-minute briefing: business/scope (1 minute), journey/channels (2), routing/AI/data (2), identity/context/security (2), failure/capacity/cost (2), evidence/next phase (1). The CIO explanation covers the business outcome, ownership boundaries, specialization tradeoff, safe degradation and evidence.

The 500-agent target is not a load-tested production deployment. Automatic cross-contact context, production identity, capacity and regional recovery require their own validation.

## Closeout and next phase

All 14 core days are complete. The separate self-paced sequence is **B01 S3 recording proof → B02 Nova 2 Sonic → B03 cleanup/regression**. Working channels remain intact.

The existing portfolio's progress, Day 14 milestone and SDK stack/source link are updated. Hero, branding, layout, scripts and homepage/project order are retained. Publish the source through the existing Hire Edward bash described in [portfolio notes](../portfolio/README.md).

- [Build journal](../PROGRESS.md)
- [Roadmap](../ROADMAP.md)
- [Operational runbook and Day 14 handoff](day13/RUNBOOK.md)

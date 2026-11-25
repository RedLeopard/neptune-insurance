# Day 11 — Security, resilience and observability

**Status:** Complete (11/14), owner-confirmed November 25, 2026. Next: Day 12. Observations below distinguish supplied output, owner reports and proposed controls.

## Review evidence

| Area | Evidence | Boundary |
| --- | --- | --- |
| Flow logging | Enabled instance setting and voice logging block; CloudWatch menu/AI/tool events; OK / CLM-1001 / IN_REVIEW | Backend success does not establish final delivery |
| S3 | Four bucket public-access blocks true; default AES256; Connect associations specify aws/connect | No objects returned under connect/ at inspection time; search predates fresh chat test; object encryption unverified |
| Capture | No recording/analytics block in supplied inbound voice export (29) | Does not prove capture is disabled in every related flow |
| Agent access | Agent profile: analytics 0/100, recordings/transcripts 0/19; no Contact search in Jordin's reported agent navigation | Earlier admin-session observation was corrected; direct AWS readers remain unreviewed |
| Lambda access | Deployed role NeptuneInsuranceLookupRole; TABLE_NAME NeptuneInsuranceLab; GetItem-only permission on that table; matching get_item code | Synthetic DEMO_CUSTOMER_ID is not real authentication |
| Web chat | Billing bot, human handoff and two-way customer/Jordin messages passed | Elena was not retested; previous Day 10 evidence remains intact |
| CLI identity | Denied ListUsers and CloudTrail LookupEvents | Audit-read denial does not imply no audit events |

## Fault and recovery

- Baseline: unpublished $LATEST, timeout 3 seconds, LOOKUP_DELAY_SECONDS=0.
- Preparation: standard-library Python subprocess orchestrated AWS CLI and preserved existing environment variables. Boto3 import failed before any mutation in the first attempt; Boto3 was not installed as part of this drill.
- Controlled fault instructions: delay 2 seconds and timeout 1 second, followed by a fresh synthetic CLM-1001 chat lookup and timeout restoration. The owner reported completing the failure check.
- Final configuration output verified timeout 3 seconds and delay 0. A subsequent known-good claim-status lookup passed as reported by the owner.
- Supplied metric: AWS/Lambda / Errors / FunctionName=NeptuneInsuranceLookup / Sum / 60 seconds. Count 3 at 17:42 and 3 at 17:44, November 25, 2026, displayed UTC-06:00.
- Six failed invocations are not six proven contacts. No captured request-level trace or exact customer fallback wording establishes individual attribution. Keep these limits visible.

## Data protection and threat model

- [Data-protection plan (PDF)](Neptune_Day11_Data_Protection_Plan.pdf)
- [Threat model and recovery gaps (PDF)](Neptune_Day11_Threat_Model.pdf)

The PDFs are Mission 4 review snapshots prepared before the subsequent drill. Their pending-test statements describe that point in the session; this Day 11 record supplies the later results.

Proposed controls: 14-day diagnostic logs, 30-day synthetic conversation artifacts, mock-record deletion at lab close, reviewed service-specific deletion and scoped secret retrieval if required. No retention/lifecycle rule, secret-store integration or notification topic was deployed. Avoid real policyholder/payment/medical data and credentials. Temporary validation diagnostics can include reference text and must be sanitized before real data is introduced. Attachment scanning remains disabled.

## Minimum monitoring specification — documented, not deployed

| Setting | Proposed value |
| --- | --- |
| Namespace / metric | AWS/Lambda / Errors |
| Dimension | FunctionName=NeptuneInsuranceLookup |
| Statistic / period | Sum / 60 seconds |
| Threshold | At least 1 error, 1 of 1 evaluation periods |
| Missing data | notBreaching |
| Owner | Edward, lab operator |
| First action | Inspect affected-minute Lambda logs and correlate request/contact/tool evidence |

Handled business rejection, routing failure and channel delivery require separate outcome signals. A normal JSON UNAVAILABLE response need not increment the Lambda execution Errors metric.

## Failure-response runbook

1. Identify symptom, channel, contact ID and time privately.
2. Inspect Connect flow block/branch, AI/tool execution and Lambda logs.
3. Map the tool-returned requestId to the Lambda request; do not assume it equals ContactId. Use explicit mappings and timestamps where available.
4. Restore the agreed baseline (timeout 3, delay 0) and verify current configuration.
5. Use one fresh CLM-1001 lookup to verify IN_REVIEW recovery and the customer-facing outcome.
6. Record observed versus reported results and unresolved evidence.

Missing logs: inspect both logging switches, published flow, region, time window and reader access. Missing artifacts: inspect capture, destination/prefix, existence and S3/KMS permissions. Do not weaken encryption as a diagnostic step.

## Completion and limits

The final self-review covers storage, access boundaries, failure localization, an actionable proposed alarm and recovery evidence. Day 11 completion closes the learning scope; it does not certify production compliance, deployed alerting, automatic cross-contact continuity, regional failover, RTO/RPO or 500-agent capacity. Exact fault correlation, fallback wording, object encryption and CloudTrail audit visibility remain recorded gaps.

# Neptune Insurance | 14-day Architect Project Roadmap

Status: `DONE` means verified, not simply designed. Design target: 500-agent reference model, **not** 500 real provisioned agents or concurrent calls.

| Phase | Milestone | Status | Evidence or acceptance criterion |
| --- | --- | --- | --- |
| Foundation | Eight-page fictional insurance site and local UI simulation | DONE | HTML, CSS, JS under `neptune-insurance/` |
| Foundation | Private S3 + CloudFront OAC + ACM + Route 53 | DONE | Distribution `E3GSYLGJJFG7RR`, browser HTTP 200 confirmed 2026-11-17 Central |
| Portfolio | Case-study page and carousel card created | DONE (local) | `neptune-insurance.html`, `install_neptune.py` |
| Portfolio | Main portfolio case study published | TODO | Verify public case-study URL |
| Source control | Dedicated GitHub repository | DONE | RedLeopard/neptune-insurance |
| Connect | Voice contact routing, queue, routing profile, test agent | IN PROGRESS / VERIFY | Call test and flow traces |
| Connect / Day 10 | Embedded Amazon Connect web chat | DONE — OWNER-REPORTED LIVE TESTS | Claims/Elena and Billing/Jordin delivery; homepage widget greeting and Billing transcript |
| Claims | Authenticated FNOL API with sample-only data | TODO | Cloud API test + auditable event |
| Messaging / Day 10 | Inbound email and reply | DONE — OWNER-REPORTED LIVE TEST | Verified custom domain, private KMS storage, inbound flow, Elena acceptance and return reply |
| Messaging / Day 10 | Registered two-way SMS path | DONE — CONTROLLED TWO-WAY TEST | Existing registration Complete, Active originator, Connect import, Jordin reply received on test phone; broader consent automation not claimed |
| Agentic / Day 7 | Conversation, typed slots, confirmation, recovery | DEPLOYED / PARTIAL TEST EVIDENCE | v0.1.0 Live; Billing/recovery transcripts reviewed; intake success learner-reported |
| Agentic / Day 8 | Guardrails, typed handoff context, AI-to-queue wiring | CONFIGURED / PUBLICATION REPORTED | Supervisor app transcript reached Escalation; 26-block supplied snapshot reviewed; real phone-to-agent handoff and final export pending |
| Integration / Day 9 | Approved tools and synthetic policy/claim API | DONE — LOOKUP TESTING COMPLETE | 8/8 direct checks passed; live Lambda OK and spoken IN_REVIEW confirmed November 24. Digit prompt and continuation fix accepted by owner; corrected claim flow archived. |
| Tasks / Day 10 | Manual claims follow-up delivery | DONE — OWNER-REPORTED LIVE TEST | Quick connect attached; Elena accepted and completed the synthetic Task |
| Follow-up / Day 10 | Automatic after-hours task configuration | PUBLISHED | Linked-task setting and publication reported; automatic delivery is not verified. Isolated closed-hours test removed from scope. |
| Continuity / Day 10 | Re-establish identity/context across contacts | NEXT — MISSION 6 | Contract, fresh ownership checks, cross-contact test and channel matrix |
| Optional scope | Voice callback build and live test | EXCLUDED | Removed from current scope by owner |
| Optional scope | Workload-type concurrency | DEFERRED | Retain working channel-level Task/Email capacity |
| Scale | 500-agent target capacity and routing model | DESIGN ONLY | Load assumptions, quotas and design doc, not a performance claim |
| Operations | Observability, security, cost review | TODO | Metrics, alarms and budget alerts |

## Definition of done for each lab task

1. Screenshot or command evidence recorded in `PROGRESS.md`.
2. Decision + tradeoff documented in `docs/ARCHITECTURE.md`.
3. Relevant source committed to GitHub.
4. Smoke test passed; no real personal information used.


## Current resume point — Day 10, Mission 6

Nine days are complete. Day 10's web chat, website entry, two-way SMS, manual Task delivery and inbound email/reply tests passed as owner-reported observations. Day 9's carried-over CLM-1001 lookup testing remains complete. See [the latest build journal](PROGRESS.md).

Next: the continuity contract and safe identity/ownership re-establishment across separate contacts, followed by the cross-contact tests and channel matrix. Customer Profiles and automatic cross-contact context retrieval are not claimed configured. The published after-hours task branch remains configuration evidence only; its isolated test and voice callbacks are excluded from current scope, not open completion requirements. Workload-type concurrency is deferred.

Earlier voice-specific agent-context and full voice quick-connect transfer evidence remain separate from the new chat/SMS/Task/email observations. Capture final current flow/application exports before replacing archived snapshots. Terraform adoption stays separate.

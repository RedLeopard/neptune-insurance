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
| Continuity / Day 10 | Re-establish identity/context across contacts | DESIGN / NOT LIVE-VERIFIED | Evidence boundary retained; Day 10 completion does not imply automatic cross-contact continuity |
| Optional scope | Voice callback build and live test | EXCLUDED | Removed from current scope by owner |
| Optional scope | Workload-type concurrency | DEFERRED | Retain working channel-level Task/Email capacity |
| Scale | 500-agent target capacity and routing model | DESIGN ONLY | Load assumptions, quotas and design doc, not a performance claim |
| Operations / Day 11 | Security, resilience and observability review | DONE — REVIEW / REPORTED DRILL | Flow logs, storage/access review, scoped lookup permission, fault/recovery, error metrics and documented plans; alarm/retention deployment and audit visibility remain separate |
| Operations / Day 12 | Metrics, supervisor views and outcomes | NEXT | Build the agreed channel scorecard and inspect operational outcomes |

## Definition of done for each lab task

1. Screenshot or command evidence recorded in `PROGRESS.md`.
2. Decision + tradeoff documented in `docs/ARCHITECTURE.md`.
3. Relevant source committed to GitHub.
4. Smoke test passed; no real personal information used.


## Current resume point — Day 12

Day 11 is complete (11/14), confirmed by the owner November 25, 2026. See [the latest build journal](PROGRESS.md) and [Day 11 evidence](docs/DAY11.md). Logging, storage/access boundaries and Lambda least privilege were reviewed. Fresh Billing web-chat handoff and two-way messaging passed with Jordin. The fault/recovery drill passed as reported; baseline timeout 3/delay 0 was verified and six Lambda errors were observed across two periods. Monitoring, retention, threat-model and response plans are documented; no alarm or retention policy was deployed.

Next: Day 12 — metrics, supervisor views and outcomes. There are three syllabus days remaining: 12, 13 and 14.

Evidence gaps remain explicit: final fallback wording, exact failure-to-contact correlation, stored-object encryption and CloudTrail audit visibility. Day 10 remains complete with its accepted channel results; earlier evidence is not erased by a narrower Day 11 recheck. Cross-contact continuity and Customer Profiles integration are not claimed verified. Closed-hours testing and voice callbacks remain excluded; workload-type concurrency and Terraform adoption remain deferred. Earlier voice-specific transfer/context evidence and final current exports remain separate follow-ups.

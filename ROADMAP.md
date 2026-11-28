# Neptune Insurance | 14-day Architect Project Roadmap

**Core bootcamp: COMPLETE (14/14), November 28, 2026.** Completion is based on source evidence and the owner's guided-session reports. Future extensions and design validation remain separate from core completion.

Status records distinguish implemented/tested work, owner-reported exercises and authored design. Design target: 500-agent reference model, **not** 500 real provisioned agents or concurrent calls.

| Phase | Milestone | Status | Evidence or acceptance criterion |
| --- | --- | --- | --- |
| Foundation | Eight-page fictional insurance site and local UI simulation | DONE | HTML, CSS, JS under `neptune-insurance/` |
| Foundation | Private S3 + CloudFront OAC + ACM + Route 53 | DONE | Distribution `E3GSYLGJJFG7RR`, browser HTTP 200 confirmed 2026-11-17 Central |
| Portfolio | Case-study page and carousel card created | DONE (local) | `neptune-insurance.html`, `install_neptune.py` |
| Portfolio | Day 14 portfolio case-study source | COMPLETE — SOURCE UPDATED | Existing page preserved; publish the new revision using the Hire Edward bash |
| Source control | Dedicated GitHub repository | DONE | RedLeopard/neptune-insurance |
| Connect | Voice contact routing, queue, routing profile, test agent | COMPLETE — OWNER-REPORTED CAPSTONE | Day 14 live voice exercise completed; Day 12 linked transfer/audio evidence retained |
| Connect / Day 10 | Embedded Amazon Connect web chat | DONE — OWNER-REPORTED LIVE TESTS | Claims/Elena and Billing/Jordin delivery; homepage widget greeting and Billing transcript |
| Future extension | Authenticated FNOL submission API | FUTURE EXTENSION | Current lab uses bounded intake and read-only synthetic lookup; production claim submission requires its own design and evidence |
| Messaging / Day 10 | Inbound email and reply | DONE — OWNER-REPORTED LIVE TEST | Verified custom domain, private KMS storage, inbound flow, Elena acceptance and return reply |
| Messaging / Day 10 | Registered two-way SMS path | DONE — CONTROLLED TWO-WAY TEST | Existing registration Complete, Active originator, Connect import, Jordin reply received on test phone; broader consent automation not claimed |
| Agentic / Day 7 | Conversation, typed slots, confirmation, recovery | COMPLETE — CORE SESSION | Live deployment, supplied Billing/recovery transcripts and owner-reported intake/capstone exercises |
| Agentic / Day 8 | Guardrails, typed handoff context, AI-to-queue wiring | COMPLETE — CONFIGURATION / REPORTED CAPSTONE | Supervisor Escalation transcript, reviewed supplied snapshot and owner-reported Day 14 handoff exercises; export provenance remains documented |
| Integration / Day 9 | Approved tools and synthetic policy/claim API | DONE — LOOKUP TESTING COMPLETE | 8/8 direct checks passed; live Lambda OK and spoken IN_REVIEW confirmed November 24. Digit prompt and continuation fix accepted by owner; corrected claim flow archived. |
| Tasks / Day 10 | Manual claims follow-up delivery | DONE — OWNER-REPORTED LIVE TEST | Quick connect attached; Elena accepted and completed the synthetic Task |
| Follow-up / Day 10 | Automatic after-hours task configuration | PUBLISHED | Linked-task setting and publication reported; automatic delivery is not verified. Isolated closed-hours test removed from scope. |
| Continuity / Day 10 | Re-establish identity/context across contacts | DESIGN / NOT LIVE-VERIFIED | Evidence boundary retained; Day 10 completion does not imply automatic cross-contact continuity |
| Optional scope | Voice callback build and live test | EXCLUDED | Removed from current scope by owner |
| Optional scope | Workload-type concurrency | DEFERRED | Retain working channel-level Task/Email capacity |
| Scale | 500-agent target capacity and routing model | DESIGN ONLY | Load assumptions, quotas and design doc, not a performance claim |
| Operations / Day 11 | Security, resilience and observability review | DONE — REVIEW / REPORTED DRILL | Flow logs, storage/access review, scoped lookup permission, fault/recovery, error metrics and documented plans; alarm/retention deployment and audit visibility remain separate |
| Operations / Day 12 | Metrics, supervisor views and outcomes | COMPLETE — OWNER-REPORTED LAB | Reports saved, controlled transfer/abandonment and contact review completed; scorecard, dictionary and progress files created |
| Operations / Day 13 | Reliability, recovery and operational runbook | COMPLETE — OWNER-ACCEPTED SESSION | Published isolated marker/context guard; rejection and recovery observations; agent recovery confirmation; incident/rollback procedures and evidence index |

| Capstone / Day 14 | Customer journey, operations handoff and principal architect defense | COMPLETE — OWNER-ACCEPTED SESSION | Guided live exercises; design decisions, risks, failure tabletop, briefing and case summary; [closeout](docs/DAY14.md) |

## Definition of done for each lab task

1. Screenshot or command evidence recorded in `PROGRESS.md`.
2. Decision + tradeoff documented in `docs/ARCHITECTURE.md`.
3. Relevant source committed to GitHub.
4. Smoke test passed; no real personal information used.


## Current resume point — Self-paced bonus missions

**The 14-day core bootcamp is complete (14/14), November 28, 2026.**

The capstone brings together the existing voice, chat, SMS, email, manual Task, bounded lookup, routing and operations baseline with the completed architecture defense. See [Day 14](docs/DAY14.md), [runbook](docs/day13/RUNBOOK.md) and [build journal](PROGRESS.md).

| Bonus mission | Next outcome | Core completion |
| --- | --- | --- |
| B01 — Recording and storage | Prove actual S3 audio, playback, access and retention decisions | Separate from completed 14-day core |
| B02 — Nova 2 Sonic | Verify model/version and supported integration; test and document the result | Separate extension |
| B03 — Cleanup and regression | Preserve the working demo; reconcile source, inventory, tests and portfolio | Separate extension |

Working SMS, email and manual Task delivery remain implemented/tested capabilities. Automatic cross-contact identity/context and 500-agent capacity are design/validation boundaries; no new production deployment is implied by this closeout.

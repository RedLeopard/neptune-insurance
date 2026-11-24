# Neptune Insurance | 14-day Architect Lab Roadmap

Status: `DONE` means verified, not simply designed. Design target: 500-agent reference model, **not** 500 real provisioned agents or concurrent calls.

| Phase | Milestone | Status | Evidence or acceptance criterion |
| --- | --- | --- | --- |
| Foundation | Eight-page fictional insurance site and local UI simulation | DONE | HTML, CSS, JS under `neptune-insurance/` |
| Foundation | Private S3 + CloudFront OAC + ACM + Route 53 | DONE | Distribution `E3GSYLGJJFG7RR`, browser HTTP 200 confirmed 2026-11-17 Central |
| Portfolio | Case-study page and carousel card created | DONE (local) | `neptune-insurance.html`, `install_neptune.py` |
| Portfolio | Main portfolio case study published | TODO | Verify public case-study URL |
| Source control | Dedicated GitHub repository | DONE | RedLeopard/neptune-insurance |
| Connect | Voice contact routing, queue, routing profile, test agent | IN PROGRESS / VERIFY | Call test and flow traces |
| Connect | Embedded Amazon Connect web chat | TODO | End-to-end chat with test agent |
| Claims | Authenticated FNOL API with sample-only data | TODO | Cloud API test + auditable event |
| Messaging | Email channel and delivery evidence | TODO | Test email reaches controlled inbox |
| Messaging | Toll-free sender registration + compliant SMS opt-in | TODO | Sender approved, actual consent implemented, delivery confirmed |
| Agentic / Day 7 | Conversation, typed slots, confirmation, recovery | DEPLOYED / PARTIAL TEST EVIDENCE | v0.1.0 Live; Billing/recovery transcripts reviewed; intake success learner-reported |
| Agentic / Day 8 | Guardrails, typed handoff context, AI-to-queue wiring | CONFIGURED / PUBLICATION REPORTED | Supervisor app transcript reached Escalation; 26-block supplied snapshot reviewed; real phone-to-agent handoff and final export pending |
| Integration / Day 9 | Approved tools and synthetic policy/claim API | DONE — LOOKUP TESTING COMPLETE | 8/8 direct checks passed; live Lambda OK and spoken IN_REVIEW confirmed November 24. Digit prompt and continuation fix accepted by owner; corrected claim flow archived. |
| Scale | 500-agent target capacity and routing model | DESIGN ONLY | Load assumptions, quotas and design doc, not a performance claim |
| Operations | Observability, security, cost review | TODO | Metrics, alarms and budget alerts |

## Definition of done for each lab task

1. Screenshot or command evidence recorded in `PROGRESS.md`.
2. Decision + tradeoff documented in `docs/ARCHITECTURE.md`.
3. Relevant source committed to GitHub.
4. Smoke test passed; no real personal information used.


## Current resume point — Main Day 10 work

Day 9 is complete (9/14). The carried-over CLM-1001 troubleshooting and testing are DONE as of November 24, 2026: all eight direct tests passed, live lookup returned OK, the caller heard IN_REVIEW, and the owner confirmed the continuation fix. See [lookup verification](terraform/LOOKUP_VERIFICATION.md). Continue the real Day 10 syllabus; Day 10 itself is not complete. Defer portfolio/page updates until the end of Day 10.

Separate follow-ups remain: final tool-copy/custom-slot export packaging, any unexecuted live failure-branch evidence, real phone-to-agent acceptance and received context, final inbound-flow export after the language correction, and the quick-connect retest. Terraform adoption remains separate. The customer website remains a browser-only simulation. See [DAY8.md](docs/DAY8.md).

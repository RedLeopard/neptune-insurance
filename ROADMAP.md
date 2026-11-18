# Neptune Insurance | 14-day Architect Lab Roadmap

Status: `DONE` means verified, not simply designed. Design target: 500-agent reference model, **not** 500 real provisioned agents or concurrent calls.

| Phase | Milestone | Status | Evidence or acceptance criterion |
| --- | --- | --- | --- |
| Foundation | Eight-page fictional insurance site and local UI simulation | DONE | HTML, CSS, JS under `neptune-insurance/` |
| Foundation | Private S3 + CloudFront OAC + ACM + Route 53 | DONE | Distribution `E3GSYLGJJFG7RR`, browser HTTP 200 confirmed 2026-11-17 Central |
| Portfolio | Case-study page and carousel card created | DONE (local) | `neptune-insurance.html`, `install_neptune.py` |
| Portfolio | Main portfolio case study published | TODO | Verify public case-study URL |
| Source control | Dedicated GitHub repository and initial push | TODO | Repo URL / first commit |
| Connect | Voice contact routing, queue, routing profile, test agent | IN PROGRESS / VERIFY | Call test and flow traces |
| Connect | Embedded Amazon Connect web chat | TODO | End-to-end chat with test agent |
| Claims | Authenticated FNOL API with sample-only data | TODO | Cloud API test + auditable event |
| Messaging | Email channel and delivery evidence | TODO | Test email reaches controlled inbox |
| Messaging | Toll-free sender registration + compliant SMS opt-in | TODO | Sender approved, actual consent implemented, delivery confirmed |
| Agentic | AI self-service, escalation, guardrails | TODO | Test transcripts + failure fallback |
| Scale | 500-agent target capacity and routing model | DESIGN ONLY | Load assumptions, quotas and design doc, not a performance claim |
| Operations | Observability, security, cost review | TODO | Metrics, alarms and budget alerts |

## Definition of done for each lab task

1. Screenshot or command evidence recorded in `PROGRESS.md`.
2. Decision + tradeoff documented in `docs/ARCHITECTURE.md`.
3. Relevant source committed to GitHub.
4. Smoke test passed; no real personal information used.

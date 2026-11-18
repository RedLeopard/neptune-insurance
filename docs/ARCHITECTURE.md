# Neptune Insurance | Architecture record

## Website data path (deployed)

Browser → public Route 53 DNS alias → CloudFront (custom HTTPS certificate via ACM) → private S3 origin (Origin Access Control) → static HTML/CSS/JS.

**Why this choice:** low-maintenance demo delivery, low operational overhead, TLS at edge, versioned objects, and separate deployments from the personal portfolio. The bucket name need not match the domain with CloudFront OAC.

## Customer experience path (planned)

Website, voice DID/toll-free, chat, email, and SMS → Amazon Connect contact flows → routing profile/queues → test agents, tasks, agentic self-service → controlled APIs (API Gateway/Lambda) → sample insurance data in DynamoDB/S3 → CloudWatch/CloudTrail.

Voice, chat, email and SMS each have independent enablement and quota/approval requirements. Amazon Connect **channels are not made operational by this static website deployment.**

## 500-agent design target

Build a logical 500-seat operating model while using only a few test agents: Auto/Home Claims 200, Policy Services 125, Sales 100, Billing 50, Escalations 25 (hypothetical planning allocation). Size calls/chats/email by peak concurrency and actual quotas, not user count.

## Key decisions to revisit

- Source of truth for sample policies and claims: client-only demo vs authenticated backend.
- Data protection and consent for future SMS/email channels.
- Omnichannel identity correlation and contact attributes without leaking PII.
- AI handoff rules and human escalation for regulated requests.
- Budget alarms, log retention, and WAF/security monitoring.

# Neptune Insurance | Architecture record

## Website data path (deployed)

Browser → public Route 53 DNS alias → CloudFront (custom HTTPS certificate via ACM) → private S3 origin (Origin Access Control) → static HTML/CSS/JS.

**Why this choice:** low-maintenance demo delivery, low operational overhead, TLS at edge, versioned objects, and separate deployments from the personal portfolio. The bucket name need not match the domain with CloudFront OAC.

## Voice entry (configured; runtime tests pending)

The existing voice demo number, `1-800-810-5374`, is mapped to the published `Neptune-Inbound-Voice` flow. Entry runs logging, a VOICE channel check, welcome and an explicitly selected hours check before the menu. One retry bounds invalid input and silence. Selection 3 sets and checks AutoClaims context, selects the existing queue and transfers into it. Selections 1 and 2 currently acknowledge and disconnect.

See [the sanitized export and resource-binding guide](../connect/README.md). The four Day 5 live tests remain pending. Website phone links start a separate call; browser-stored claims are not transferred into Connect. Routing profiles govern agent eligibility after queue entry and are not caller-facing flow blocks.

## Conversation layer (Day 7 deployment)

`NeptuneInsurance` v0.1.0 is deployed in Agentic CX Designer. Its Welcome flow recognizes Billing, New Auto Claim, and Claim Status requests. Typed slots hold synthetic inputs; deterministic recap and Yes/No confirmation bound the intake. A shared Recovery flow handles unsupported or unresolved input.

This is a separately deployed conversation layer. The existing phone entry and static website do not invoke it yet. Exiting the application via Default is not a queue transfer, an agent connection, or an insurance backend transaction. See [configuration and observed evidence](DAY7.md).

## Broader customer experience path (planned)

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

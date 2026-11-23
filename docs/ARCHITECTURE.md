# Neptune Insurance | Architecture record

## Website data path (deployed)

Browser → public Route 53 DNS alias → CloudFront (custom HTTPS certificate via ACM) → private S3 origin (Origin Access Control) → static HTML/CSS/JS.

**Why this choice:** low-maintenance demo delivery, low operational overhead, TLS at edge, versioned objects, and separate deployments from the personal portfolio. The bucket name need not match the domain with CloudFront OAC.

## Voice and AI entry (Day 8 configuration; live handoff pending)

The existing demo number is associated with `Neptune-Inbound-Voice`. The Day 8 graph is: logging → voice-channel check → voice/language setup → welcome → lab-hours check → menu. Policy Service acknowledges and disconnects. Billing selects Neptune-Billing and transfers. Auto Claims sets/checks service context and invokes `NeptuneInsurance` through the Agentic CX block.

Escalation copies five returned context values into user-defined contact attributes, selects the existing Auto Claims queue and transfers. AI errors use the claims acknowledgement/queue fallback; Default disconnects; idle-chat timeout uses technical fallback. Agent delivery remains dependent on queue/profile/channel eligibility, agent state and capacity.

**Evidence boundary:** the latest supplied export has 26 reachable blocks and valid targets, and predates the final reported language-attribute correction/publication. A supervisor app transcript reaches Escalation, while real phone-to-agent delivery and agent receipt of context remain unverified. See [Day 8](DAY8.md) and [public snapshot bindings](../connect/README.md).

## Conversation layer and policy controls

The Day 7 application established Welcome, Recovery, Billing, New Auto Claim and Claim Status flows with typed slots, recap and confirmation. Day 8 adds explicit general-human and supervisor Escalate flows, an input guardrail and an output LLM-judge guardrail. The input paths preserve distinct request reasons and a Boolean supervisor flag.

The handoff summary/reference/intent values are currently fixed triage fallbacks, not backend results or an automatically generated transcript summary. The model and guardrail do not authorize coverage, liability, fraud or payment decisions. No live claims API or tool-backed insurance transaction is claimed. Captured values, actual tool results and authorization must be explicitly validated before future reuse.

The static website remains separate: its claims form does not feed the phone contact, and publishing the AI flow does not enable web chat or messaging. Routing profiles remain human-agent eligibility controls, not caller-facing conversational flows.

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


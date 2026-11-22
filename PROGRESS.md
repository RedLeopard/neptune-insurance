# Neptune Insurance | Build journal

## 2026-11-21 (America/Chicago) — Day 7 conversational application

- Saved `NeptuneInsurance` in `Neptune Insurance Lab`; deployment v0.1.0 displayed successful and Live.
- Built Welcome, Recovery, Billing, New Auto Claim, and Claim Status flows; added typed slots, recap placeholders, confirmation endings, and connected No match recovery paths.
- Reviewed the supplied 11-node claim-flow export for graph connectivity and matching placeholder types.
- Observed pasted test evidence: billing recognized `NeptuneBilling` and exited via Default; an unsupported pizza request reached recovery and exited via Default. Additional intake tests were reported successful by the learner, without full transcripts.
- The app collects synthetic information only. It does not file a claim, determine coverage, or retrieve live status. Phone/web invocation and human handoff remain future work.
- Updated the portfolio case study to Day 7, with 7/14 progress and the next Day 8 milestone. Publication to the personal portfolio is separate.

## 2026-11-20 (America/Chicago) — Day 6 routing configuration

- Worked through Billing and Auto Claims queues, routing-profile eligibility, agent state, and channel capacity.
- Console reported `Neptune-To-AutoClaims` saved: Queue type, Auto Claims destination, Default queue transfer flow.
- Learner requested a full quick-connect retest on return. Keep this open; AI application tests do not verify a queue transfer or agent delivery.

## 2026-11-19 (America/Chicago) — Voice entry source and public demo links

- Confirmed the existing voice demo number, `1-800-810-5374`, is associated with `Neptune-Inbound-Voice` in the supplied Connect configuration.
- Added clickable phone links to all eight website footers and to the Home, Support, Claims and My Neptune content. Replaced the pending-number card; clarified voice versus planned messaging and the separate browser-only claims form.
- Added the supplied 21-block flow as a sanitized public template under `connect/flows/`, with consistent placeholder account, instance, hours and queue identifiers. Included binding instructions and the current menu behavior.
- Configuration evidence: the supplied export reports `PUBLISHED` and includes logging, voice-channel and hours checks, one retry, Auto Claims queue selection/transfer, and connected failure paths.
- Static validation checks phone destinations, internal links, unique HTML IDs, graph references, the retry bound and identifier replacement. These checks do not execute a phone call.
- Pending: deploy these website source changes to S3/CloudFront and execute T01–T04. No live-call results or successful agent delivery are claimed.

## 2026-11-17 (America/Chicago) — Static website goes live

- Created fictional Neptune Insurance customer website with responsive coverage, claims, portal, support, and information pages.
- Requested and DNS-validated an ACM certificate for `neptune.hireedwardthornton.click`; verified `ISSUED`.
- Deployed private S3 origin behind CloudFront; distribution `E3GSYLGJJFG7RR` (`d24fdjlm9el2lj.cloudfront.net`).
- Created Route 53 A/AAAA aliases. DNS was initially cached negatively; later authoritative and public DNS resolved.
- Confirmed custom domain HTTPS and CloudFront `HTTP/2 200` with content length 19,835 for `index.html`.
- No live voice, chat, SMS, or email integration was demonstrated by these web tests.

## Next checkpoint — Portfolio + GitHub baseline

- [ ] Relocate Neptune source folder from Mac Downloads to home projects directory.
- [ ] Review case-study page and add portfolio carousel card.
- [x] Dedicated source repository: https://github.com/RedLeopard/neptune-insurance (established before this update).
- [ ] Verify public portfolio link.
- [ ] Capture architecture screenshots for an interview-ready walkthrough.

## Note for future entries

Use format: date, change made, service/component, proof/test, architectural decision, next action.

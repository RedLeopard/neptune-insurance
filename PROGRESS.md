# Neptune Insurance | Build journal

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
- [ ] Push project to a dedicated GitHub repository and record first commit SHA.
- [ ] Verify public portfolio link.
- [ ] Capture architecture screenshots for an interview-ready walkthrough.

## Note for future entries

Use format: date, change made, service/component, proof/test, architectural decision, next action.

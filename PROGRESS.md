# Neptune Insurance | Build journal

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

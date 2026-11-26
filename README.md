# Neptune Insurance | Enterprise Omnichannel CX Project

A fictional, portfolio-grade insurance website deployed to AWS with a staged Amazon Connect integration plan. **This is a demonstration, not a licensed insurer.** Do not enter real customer or sensitive insurance information.

**Live demo:** https://neptune.hireedwardthornton.click/  
**Voice demo:** [1-800-810-5374](tel:+18008105374) (synthetic demonstration; live claim lookup tested successfully)  
**Portfolio case study (after installation):** https://hireedwardthornton.click/neptune-insurance.html  

**Current milestone:** Day 12 complete (12/14), closed November 26, 2026 after owner-reported reporting and controlled voice tests. Next: Day 13 — reliability drills and runbooks. Day 12 saved supervisor, queue/channel and agent views; tested Billing-to-Claims transfer and Claims abandonment; and reviewed reporting scope/contact chains. Created a qualitative executive scorecard, data dictionary, report inventory, test ledger and mission progress. See [Day 12 closeout](docs/day12/README.md). Day 11 reviewed logging, S3/encryption boundaries, agent permissions and table-scoped Lambda access; verified two-way Billing web chat with Jordin; documented data protection, threats and response plans; and exercised a controlled timeout/recovery with the original settings restored. CloudWatch showed six Lambda errors across two one-minute periods. Exact failure-to-contact correlation, fallback wording, stored-object encryption and CloudTrail inspection remain evidence gaps; no alarm or retention policy was deployed. Day 10 remains complete with its prior scope decisions preserved. See [current journal](PROGRESS.md) and [Day 11 evidence](docs/DAY11.md).

## What's actually built

- Eight responsive pages under `neptune-insurance/`: home, coverage, claims, portal, support, about, privacy, terms.
- Interactive *simulated* claims workflow, sample policy portal, quote explorer, and scripted help preview. Browser claims stay local and are not sent to the phone flow. The homepage now embeds the real Neptune-WebChat widget; the owner published it and supplied the expected live greeting and Billing response.
- Amazon Connect voice entry: published `Neptune-Inbound-Voice` flow and existing toll-free number association, confirmed by the supplied export and number configuration. Logging, a voice/language block, channel/hours checks, a three-choice menu, one retry, Billing routing and an AI-to-Auto Claims escalation path are configured. The latest supplied 26-block export was reviewed for reachability and valid targets. The four Day 5 voice tests remain pending.
- Routing: Neptune-Claims and Neptune-Training retain Voice/Chat capacity 1 with no cross-channel concurrency. Claims also has Task/Email capacity 1. Auto Claims uses one Voice/Chat/Task/Email row at priority 1 and delay 0; duplicate queue rows with different priorities were rejected by the console. Neptune-To-AutoClaims was attached to Auto Claims and manual Task delivery to Elena passed. This does not substitute for the earlier voice-transfer retest.
- Agentic CX Designer: `NeptuneInsurance` in `Neptune Insurance Lab`, with the [Day 7 conversation foundation](docs/DAY7.md) and a new Day 8 build/deployment reported. `NeptuneHumanHandoff`, `NeptuneSupervisorHandoff`, five typed context variables, an input guardrail and an output guardrail are configured. A supplied supervisor test transcript ends via **Escalation**; the general-human test was reported successful.
- Phone integration: the inbound flow now invokes the application on the Auto Claims branch and copies five returned context values before selecting the existing claims queue. AI errors retain a human queue fallback; Default ends the contact. This is configured and publication is reported, **not yet verified through a real phone-to-agent call**. The separate website chat widget now invokes NeptuneInsurance through Neptune-Inbound-Chat; real Claims and Billing chat handoffs were owner-reported successful.
- Insurance lookup: DynamoDB synthetic records, a scoped read-only Lambda role, field filtering, direct success/error tests and controlled timeout recovery. A tool-enabled module and Data request connect claim-reference capture to the backend. All eight direct checks passed, and a real phone lookup returned OK with the caller hearing IN_REVIEW. The owner confirmed the continuation fix and testing complete. Spoken-reference normalization and its offline security checks are committed. See [current evidence and next actions](terraform/LOOKUP_VERIFICATION.md).
- AWS SDK for Python (Boto3): the Day 9 `NeptuneInsuranceLookup` Lambda uses `boto3.resource("dynamodb")` and `Table.get_item()` to retrieve synthetic policy/claim records programmatically, with Botocore timeout/retry configuration and a table-scoped IAM role. This is direct AWS SDK integration in the runtime, distinct from Python scripts that orchestrate AWS CLI commands. See [Lambda source](terraform/lambda/neptune_insurance_lookup.py).
- Export provenance: the public flow is the latest **provided** snapshot, `Neptune-Inbound-Voice (27).json`. It contains Joanna but predates the final reported language-attribute correction and republish. The final post-correction export has not been supplied; do not treat this snapshot as that final export.
- [Sanitized flow export and resource-binding guide](connect/README.md). Source-account resource identifiers are replaced with placeholders; reselect hours and queue resources before publishing an imported copy.
- Web chat and SMS: published Neptune-Inbound-Chat reuses NeptuneInsurance's Production alias, maps five handoff attributes and branches on customerIntent = Billing or AutoClaims. Segment Subtype connect:SMS selects entryChannel = SMS; other entries retain WebChat. The existing SMS originator is Active, its linked toll-free registration is Complete, and two-way Connect import plus a customer-to-Jordin-to-phone exchange were verified.
- Email: existing SES approval carried forward; AmazonConnectEmailSESAccessRole created and hireedwardthornton.click verified in Connect. Email-message and attachment storage reuse the private S3 bucket with explicit KMS configuration. Attachment CORS permits GET/PUT from the Neptune workspace origin. claims@hireedwardthornton.click uses Neptune-Inbound-Email and Auto Claims' reply address; Elena's inbound acceptance and return reply to the test inbox were owner-reported successful.
- Follow-up: Neptune-Claim-Followup is published; manual Task delivery passed. The normal messaging flow's after-hours Claims branch creates a linked Task and acknowledges only creation success; Billing has its own closed-hours message. Publication was reported after enabling Link to contact. No successful closed-branch test is claimed; that isolated test and voice callbacks were removed from current scope.
- Operations automation: Python orchestrated AWS CLI calls for resource discovery, JSON flow generation, backups, draft/published comparisons and post-write verification. These terminal scripts did not directly use Boto3 or constitute a CI/CD pipeline. IAM access was scoped through customer-managed policies after Edward's inline policy size limit was reached. Latest terminal-authored flow exports and reusable script packaging remain to be captured in source control.
- Security and operations / Day 11: both agents use the Agent security profile; historical analytics and recording/transcript permissions are disabled. The deployed lookup uses GetItem on NeptuneInsuranceLab only. Reviewed Connect storage associations versus bucket default encryption, captured flow/tool success evidence, restored the timeout to 3 seconds and LOOKUP_DELAY_SECONDS to 0 after the drill, and documented the proposed monitoring threshold and recovery runbook. See [Day 11](docs/DAY11.md), [data-protection plan](docs/Neptune_Day11_Data_Protection_Plan.pdf) and [threat model](docs/Neptune_Day11_Threat_Model.pdf).
- Dedicated AWS S3 bucket with private origin, CloudFront distribution with Origin Access Control, HTTPS certificate in ACM, and Route 53 aliases.
- Portfolio case study (`neptune-insurance.html`) and card installer (`install_neptune.py`) to keep the main portfolio's normal project format.

## Structure

```text
NeptuneInsurance/
├── neptune-insurance/         # Live website source (deployed separately)
│   ├── index.html
│   ├── coverage.html
│   ├── claims.html
│   ├── portal.html
│   ├── support.html
│   └── assets/
├── neptune-insurance.html     # Portfolio project case study
├── assets/                    # Portfolio project card artwork
├── connect/                   # Sanitized Amazon Connect flow and lab notes
├── terraform/                 # Lookup source/contracts/tests; Terraform adoption deferred
├── install_neptune.py        # Safe update to existing portfolio
├── deploy_neptune_subdomain.py # Infrastructure/bootstrap script (already deployed)
├── scripts/
│   ├── publish_site.sh       # Update live Neptune website without rebuilding infra
│   └── verify_site.sh        # Check live deployment
├── docs/                     # Architecture/security/operations notes
├── ROADMAP.md                # Backlog and checkpoints
└── PROGRESS.md               # Milestone journal
```

## Day-to-day workflow

1. Edit source locally, run `bash scripts/verify_site.sh`, and review your changes.
2. `git add . && git commit -m "Describe milestone" && git push` once your GitHub repository is configured.
3. `bash scripts/publish_site.sh` to publish *only* the Neptune customer site to the dedicated S3 bucket and invalidate CloudFront.
4. To sync the current portfolio homepage and Neptune case study locally, run `bash scripts/sync_portfolio.sh` (defaults to the existing `~/hireedward` folder). See [portfolio source notes](portfolio/README.md). This copies files only; deploy the portfolio separately when needed. Keep `install_neptune.py` for the earlier bootstrap workflow.

## Source control setup

Move `~/Downloads/NeptuneDeployment` to `~/NeptuneInsurance` from your Mac after backing up or checking that the destination does not already exist. The GitHub repository should be dedicated to Neptune; do not nest its `.git` inside another Git repository.

```bash
cd ~/NeptuneInsurance
git init -b main
git add .
git commit -m "Initial Neptune Insurance site and architecture baseline"
# If you use GitHub CLI (gh) and are logged in:
gh repo create RedLeopard/neptune-insurance --public --source=. --remote=origin --push
```

If GitHub CLI is not installed, create an **empty** GitHub repository named `neptune-insurance` under `RedLeopard` without a README, then:

```bash
git remote add origin https://github.com/RedLeopard/neptune-insurance.git
git push -u origin main
```

See `docs/SECURITY.md` before publishing publicly. Never commit AWS access keys, `.env` files, personal information, real customer data, or actual call recordings.


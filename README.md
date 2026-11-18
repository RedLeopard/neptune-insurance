# Neptune Insurance | Enterprise Omnichannel CX Lab

A fictional, portfolio-grade insurance website deployed to AWS with a staged Amazon Connect integration plan. **This is a demonstration, not a licensed insurer.** Do not enter real customer or sensitive insurance information.

**Live demo:** https://neptune.hireedwardthornton.click/  
**Portfolio case study (after installation):** https://hireedwardthornton.click/neptune-insurance.html  

## What's actually built

- Eight responsive pages under `neptune-insurance/`: home, coverage, claims, portal, support, about, privacy, terms.
- Interactive *simulated* claims workflow, sample policy portal, quote explorer, and scripted help preview. These do **not** use real insurance processing or live Amazon Connect channels.
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
4. To update the portfolio case study and carousel card, `python3 install_neptune.py ~/hireedward --dry-run`, then repeat without `--dry-run` using your **actual** portfolio folder. Deploy that portfolio separately using your existing portfolio pipeline.

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

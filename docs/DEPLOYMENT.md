# Deployment procedure

## Infrastructure (already provisioned in account 690405831841)

- DNS: `neptune.hireedwardthornton.click`
- Route 53 zone: `Z006160125GQ45NREN3EF`
- CloudFront: `E3GSYLGJJFG7RR`
- S3: `neptune-insurance-690405831841-us-east-1` (private)
- ACM: certificate in us-east-1 (issued)

The bootstrap `deploy_neptune_subdomain.py` can create/update billable resources. Do **not** run it for ordinary HTML/CSS/JS updates. Use `bash scripts/publish_site.sh` instead after reviewing changes.

## Test and deploy

```bash
cd ~/NeptuneInsurance
bash scripts/verify_site.sh
bash scripts/publish_site.sh
```

`publish_site.sh` asks for confirmation, checks the expected AWS account, syncs only the Neptune website folder, and requests CloudFront invalidation. It does **not** touch the portfolio distribution or delete S3 objects.

## Portfolio (different deployment)

```bash
python3 install_neptune.py /actual/path/to/portfolio --dry-run
python3 install_neptune.py /actual/path/to/portfolio
```

Review `index.html`, `neptune-insurance.html`, and the SVG card artwork. Use your normal portfolio deployment workflow to publish the changes.

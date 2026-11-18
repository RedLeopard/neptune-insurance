#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
account="$(aws sts get-caller-identity --query Account --output text)"
if [[ "$account" != "690405831841" ]]; then
  echo "STOP: Expected AWS account 690405831841 but found $account" >&2; exit 1
fi
site="$root/neptune-insurance"
[[ -s "$site/index.html" ]] || { echo 'Missing website index.html' >&2;exit 1; }
echo "About to upload $site to the Neptune-only S3 bucket. No deletions."
echo "This may incur S3 / CloudFront usage charges."
read -r -p 'Type PUBLISH to continue: ' answer
[[ "$answer" == 'PUBLISH' ]] || { echo 'Cancelled.';exit 1; }
aws s3 sync "$site/" s3://neptune-insurance-690405831841-us-east-1/ --region us-east-1 --exclude '.DS_Store'
echo 'Requesting CloudFront cache invalidation...'
aws cloudfront create-invalidation --distribution-id E3GSYLGJJFG7RR --paths '/*' --query 'Invalidation.Id' --output text
echo 'Published Neptune website. Portfolio untouched.'

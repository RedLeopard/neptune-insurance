#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
portfolio_dir="${1:-$HOME/hireedward}"
source_page="$repo_root/neptune-insurance.html"
target_page="$portfolio_dir/neptune-insurance.html"

[[ -s "$source_page" ]] || { echo "Missing Neptune portfolio source." >&2; exit 1; }
[[ -f "$portfolio_dir/index.html" ]] || { echo "Expected the existing portfolio at $portfolio_dir" >&2; exit 1; }

backup_dir="$HOME/Neptune-Day13-Backups/portfolio-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$backup_dir"
if [[ -f "$target_page" ]]; then
    cp "$target_page" "$backup_dir/neptune-insurance-before.html"
fi
cp "$source_page" "$target_page"
aws s3 cp "$target_page" s3://hireedwardthornton.click/neptune-insurance.html \
    --content-type text/html --cache-control no-cache --no-cli-pager
aws cloudfront create-invalidation --distribution-id E302FX62UIOL47 \
    --paths /neptune-insurance.html --query Invalidation.Id --output text --no-cli-pager
echo "Published Neptune portfolio case study: https://hireedwardthornton.click/neptune-insurance.html"

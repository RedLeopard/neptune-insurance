#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
portfolio_dir="${1:-$HOME/hireedward}"

if [[ ! -f "$portfolio_dir/index.html" || ! -d "$portfolio_dir/assets" ]]; then
  echo "Expected an existing portfolio with index.html and assets/: $portfolio_dir" >&2
  exit 1
fi

for source in "$repo_root/portfolio/index.html" "$repo_root/neptune-insurance.html" "$repo_root/assets/neptune-website-hero.jpg"; do
  [[ -s "$source" ]] || { echo "Missing source: $source" >&2; exit 1; }
done

cp "$repo_root/portfolio/index.html" "$portfolio_dir/index.html"
cp "$repo_root/neptune-insurance.html" "$portfolio_dir/neptune-insurance.html"
cp "$repo_root/assets/neptune-website-hero.jpg" "$portfolio_dir/assets/neptune-website-hero.jpg"
echo "Synced portfolio index, Neptune case study, and preview artwork to $portfolio_dir"

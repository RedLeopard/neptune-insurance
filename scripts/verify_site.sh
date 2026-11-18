#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for p in index.html coverage.html claims.html portal.html support.html about.html privacy.html terms.html; do
  test -s "$root/neptune-insurance/$p" || { echo "Missing: $p"; exit 1; }
done
echo "Local site files present."
if command -v curl >/dev/null 2>&1; then
  echo "Public endpoint:"
  curl -sSIL --max-time 15 https://neptune.hireedwardthornton.click/ | head -n 12
fi

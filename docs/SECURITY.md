# Security and public repository checklist

- Neptune is fictional. Do not claim insurance licensure, insurance coverage, or SMS approval.
- Do not store real customer names, policy numbers, claims, PHI, payment data, recordings, addresses, or insurance forms in this repository or static demo.
- AWS account IDs and CloudFront distribution IDs are not credentials, but avoid publishing additional infrastructure details if not necessary.
- Do not commit AWS access keys, `.env`, AWS CLI profiles, secret JSON, tokens, KMS key material, certificates or private keys.
- Before `git add`, review: `git status --short`, `git diff --cached --stat`, and `git diff --cached --check`.
- Private S3 access is through CloudFront OAC. Do not set S3 website objects public.
- Claims and policy interaction is browser-only and simulated until a secure authenticated backend is built.
- An SMS program needs real consent, correct legal entity and public policies. A fictional website is not proof of a real insurer.

# Day 9: adopt the insurance table with Terraform

## Verified checkpoint

Learner-reported terminal evidence on November 23, 2026:

- AWS identity: Edward in account 690405831841.
- Neptune Connect instance: neptune-insurance-lab in us-west-2.
- NeptuneInsuranceLab is ACTIVE with String partition key pk.
- The seed write returned an empty UnprocessedItems object.
- The verification scan returned POLICY#POL-1001 (DEMO-1001, ACTIVE), CLAIM#CLM-1001 (DEMO-1001, IN_REVIEW), and CLAIM#CLM-2002 (DEMO-2002, RECEIVED). All have product AUTO.

The table and three synthetic records already exist. Do not create a second table.

## Current scope

This first Terraform stage manages the existing DynamoDB table only.
Lambda, IAM, logging, Connect association and conversational integration are later
guided tasks, not completed resources. Seed records remain separate from
infrastructure state; do not use aws_dynamodb_table_item for these mutable lab records.

The provider explicitly selects Oregon, regardless of the CLI's default region,
and restricts execution to the verified account. No credentials belong in these files.
Terraform prevent_destroy guards plans while this lifecycle rule is present; it is
not AWS-side deletion protection and does not prevent deletion through other tools.

## Bring the configuration to the laptop

From the existing checkout:

```bash
git -C "$HOME/NeptuneInsurance" pull --ff-only origin main
terraform version
```

If Terraform is unavailable, resolve installation before continuing. The source
requires Terraform 1.5 or later, below 2.0. If pull reports an overwrite conflict,
stop and inspect it; do not reset or clean the working tree.

## Initialize, validate and inspect the import plan

```bash
terraform -chdir="$HOME/NeptuneInsurance/backend/day9/terraform" init
terraform -chdir="$HOME/NeptuneInsurance/backend/day9/terraform" fmt -check
terraform -chdir="$HOME/NeptuneInsurance/backend/day9/terraform" validate
terraform -chdir="$HOME/NeptuneInsurance/backend/day9/terraform" plan -out=adopt-table.tfplan
```

Run these sequentially and stop if one fails. No apply has been authorized by this
README. Review the actual plan in the lesson before applying. Expected first plan:
one table to import, zero resources to add/change/destroy. Output values may also
be added to state. If the provider detects any drift, inspect it before proceeding.
The import block records the existing table in state during apply rather than
creating a new table, and does not import or rewrite its item contents.

After the import-only plan is reviewed and applied, rerun plan and confirm no
infrastructure changes. Keep imports.tf as a record of adoption.

## Source and state

Commit .tf files, this README, synthetic fixtures and .terraform.lock.hcl.
Keep .terraform/, state files, saved plans, credentials and secret variable files
out of Git. State is local for this single-operator lab; preserve it securely.
An access-controlled remote state backend can be added as a separate task before
using multiple operators or automated applies.

The existing backend/day9/table.json and seed-records.json were created on the
learner's laptop. They are not overwritten by this commit. The former documents
the CLI bootstrap; do not use it to recreate a table now managed by Terraform.
Inspect and stage those two exact synthetic files separately when syncing them.
Never use git add . for the whole repository because unrelated website files
are currently untracked.

## References

- https://developer.hashicorp.com/terraform/language/import
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table
- https://developer.hashicorp.com/terraform/language/style

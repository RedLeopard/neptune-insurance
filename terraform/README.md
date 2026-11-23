# Neptune Insurance infrastructure

Terraform configuration for the existing Neptune Insurance lookup table in
us-west-2 (Oregon), AWS account 690405831841.

## Existing resources

- Connect instance: neptune-insurance-lab.
- DynamoDB table: NeptuneInsuranceLab, on-demand billing, String partition key pk.
- Synthetic records: POLICY#POL-1001, CLAIM#CLM-1001 and CLAIM#CLM-2002.

The table and records were created and verified through AWS CLI. Terraform has
not been initialized or applied. Adoption is deferred until the insurance lookup
and its integration are working.

## Configuration scope

The current configuration covers the existing table only. Lambda, IAM, logging
and Connect integration are implemented incrementally. Seed items are maintained
separately from Terraform infrastructure state.

The provider explicitly selects us-west-2 and restricts execution to the account
above. imports.tf identifies the existing table by name. It must be adopted
without creating a replacement or rewriting its item contents.

prevent_destroy guards Terraform plans while the lifecycle rule is present; it
is not AWS-side deletion protection.

## Project files

- main.tf: table definition.
- versions.tf: Terraform/provider requirements and AWS configuration.
- imports.tf: existing-table import declaration.
- outputs.tf: table name, ARN and region.
- iam/: Neptune Insurance role trust and permission documents.
- table.json: original AWS CLI table configuration, when present locally.
- seed-records.json: synthetic record fixtures, when present locally.

All project paths use the repository's top-level terraform/ directory.

## Adoption workflow (deferred)

Terraform 1.5 or later, below 2.0, is required. After the backend is working:

```bash
terraform -chdir="$HOME/NeptuneInsurance/terraform" init
terraform -chdir="$HOME/NeptuneInsurance/terraform" fmt -check
terraform -chdir="$HOME/NeptuneInsurance/terraform" validate
terraform -chdir="$HOME/NeptuneInsurance/terraform" plan -out=adopt-table.tfplan
```

Run commands sequentially and resolve failures before continuing. Review the
actual plan before applying. The expected initial plan imports one table with
zero resources to add, change or destroy. Inspect any drift rather than assuming
the configuration matches the account. After adoption, confirm a subsequent
plan shows no infrastructure changes.

## Version control

Commit configuration, Python source, synthetic fixtures and .terraform.lock.hcl.
Keep state files, saved plans, .terraform/, credentials and secret inputs out of
Git. Local state is appropriate only for the current single-operator workflow;
preserve it securely and configure an access-controlled remote backend before
using multiple operators or automated applies.

Stage exact project paths so unrelated website files are not accidentally
included. If a pull reports a conflict, inspect it rather than resetting or
cleaning the working tree.

## References

- https://developer.hashicorp.com/terraform/language/import
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table
- https://developer.hashicorp.com/terraform/language/style

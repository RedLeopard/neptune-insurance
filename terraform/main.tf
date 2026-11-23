# Manage the existing Neptune Insurance data table after import.
# Seed items are managed separately; this resource manages the table itself.
resource "aws_dynamodb_table" "insurance_lab" {
  name         = "NeptuneInsuranceLab"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }
}

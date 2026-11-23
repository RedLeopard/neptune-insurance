# The existing table is imported by name.
# Review the plan before applying; the expected first plan imports one table.
import {
  to = aws_dynamodb_table.insurance_lab
  id = "NeptuneInsuranceLab"
}

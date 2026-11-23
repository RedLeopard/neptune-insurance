output "table_name" {
  description = "Name of the synthetic insurance table."
  value       = aws_dynamodb_table.insurance_lab.name
}

output "table_arn" {
  description = "Exact table ARN for the later least-privilege Lambda policy."
  value       = aws_dynamodb_table.insurance_lab.arn
}

output "aws_region" {
  description = "Region of the existing Neptune Connect instance and backend."
  value       = "us-west-2"
}

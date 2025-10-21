output "bucket_id" {
  description = "The name of the bucket"
  value       = aws_s3_bucket.terraform_state.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.terraform_state.arn
}
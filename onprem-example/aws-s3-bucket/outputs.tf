output "bucket_name" {
  description = "Generated bucket name."
  value       = aws_s3_bucket.main.bucket
}

output "bucket_arn" {
  description = "Bucket ARN, for IAM policies."
  value       = aws_s3_bucket.main.arn
}

output "bucket_region" {
  description = "Region that holds the bucket."
  value       = aws_s3_bucket.main.region
}

output "s3_uri" {
  description = "URI for the AWS CLI."
  value       = "s3://${aws_s3_bucket.main.bucket}"
}

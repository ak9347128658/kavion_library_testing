variable "region" {
  description = "AWS region for the bucket."
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "Bucket name prefix. AWS appends a unique suffix, because bucket names are global."
  type        = string
  default     = "onprem-demo"
}

variable "versioning_enabled" {
  description = "Keep previous versions of overwritten and deleted objects."
  type        = bool
  default     = false
}

variable "force_destroy" {
  description = "Let terraform destroy delete the bucket even when it still holds objects."
  type        = bool
  default     = false
}

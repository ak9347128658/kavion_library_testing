variable "region" {
  description = "AWS region for the VPC and instance."
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "Short name used for the instance, network, and key file."
  type        = string
  default     = "onprem-demo-3"
}

variable "admin_username" {
  description = "Linux user for SSH. The Ubuntu 22.04 AMI logs in as ubuntu."
  type        = string
  default     = "ubuntu"
}

variable "instance_type" {
  description = "Size for function testing. t3.large is 2 vCPU and 8 GiB."
  type        = string
  default     = "t3.large"
}

variable "root_volume_size_gb" {
  description = "Root volume size in GiB."
  type        = number
  default     = 30
}

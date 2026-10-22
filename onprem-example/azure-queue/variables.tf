variable "location" {
  description = "Azure region for the resource group and storage account."
  type        = string
  default     = "eastus"
}

variable "name" {
  description = "Short name used for the resource group and as the storage account name prefix."
  type        = string
  default     = "onprem-demo"
}

variable "queue_name" {
  description = "Queue name. 3-63 chars, lowercase letters, numbers, and single hyphens."
  type        = string
  default     = "onprem-demo-jobs"
}

variable "replication_type" {
  description = "Storage redundancy. LRS is the cheapest and enough for function testing."
  type        = string
  default     = "LRS"
}

variable "grant_current_user" {
  description = "Give the identity running Terraform the Storage Queue Data Contributor role, so the portal and az CLI work with Entra ID login. Needs Owner or User Access Administrator on the subscription."
  type        = bool
  default     = false
}

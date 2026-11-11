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

variable "container_name" {
  description = "Blob container name. 3-63 chars, lowercase letters, numbers, and single hyphens."
  type        = string
  default     = "invoices"
}

variable "replication_type" {
  description = "Storage redundancy. LRS is the cheapest and enough for testing."
  type        = string
  default     = "LRS"
}

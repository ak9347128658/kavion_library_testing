variable "location" {
  description = "Azure region for this VM. Standard_F2as_v7 uses 2 of the 4 regional vCPUs. Same region as azure-4cpu-1. centralindia cannot allocate the 4 vCPU size."
  type        = string
  default     = "centralus"
}

variable "name" {
  description = "Short name used for the resource group, VM, and key file."
  type        = string
  default     = "onprem-4cpu-3"
}

variable "admin_username" {
  description = "Linux admin user for SSH. Cannot be root, admin, or administrator."
  type        = string
  default     = "azureuser"
}

variable "vm_size" {
  description = "Size for function testing. Standard_F2as_v7 is 2 vCPU and 8 GiB."
  type        = string
  default     = "Standard_F2as_v7"
}

variable "os_disk_size_gb" {
  description = "OS disk size in GiB. 30 is the Ubuntu image minimum."
  type        = number
  default     = 30
}

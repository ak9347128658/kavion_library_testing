variable "location" {
  description = "Azure region for this VM. Each Standard_F4as_v7 uses the whole 4 vCPU regional quota. centralindia cannot allocate this size."
  type        = string
  default     = "centralus"
}

variable "name" {
  description = "Short name used for the resource group, VM, and key file."
  type        = string
  default     = "onprem-4cpu-1"
}

variable "admin_username" {
  description = "Linux admin user for SSH. Cannot be root, admin, or administrator."
  type        = string
  default     = "azureuser"
}

variable "vm_size" {
  description = "Size for function testing. Standard_F4as_v7 is 4 vCPU and 16 GiB."
  type        = string
  default     = "Standard_F4as_v7"
}

variable "os_disk_size_gb" {
  description = "OS disk size in GiB. 30 is the Ubuntu image minimum."
  type        = number
  default     = 30
}

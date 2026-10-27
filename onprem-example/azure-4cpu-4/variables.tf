variable "location" {
  description = "Azure region for this VM. Standard_F2as_v7 uses 2 of the 4 regional vCPUs. centralus is full because onprem-4cpu-1 uses Standard_F4as_v7. northcentralus has unused quota and no SKU restriction for this size."
  type        = string
  default     = "northcentralus"
}

variable "name" {
  description = "Short name used for the resource group, VM, and key file."
  type        = string
  default     = "onprem-4cpu-4"
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

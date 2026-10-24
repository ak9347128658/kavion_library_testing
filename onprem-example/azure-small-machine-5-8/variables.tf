variable "location" {
  description = "Azure region for this resource group and its VMs."
  type        = string
  default     = "centralindia"
}

variable "name" {
  description = "Short name for the shared resource group, VNet, subnet, and NSG."
  type        = string
  default     = "onprem-demo-5-8"
}

variable "vm_names" {
  description = "VM names created in the one resource group. Each gets a public IP, NIC, disk, and PEM file."
  type        = list(string)
  default     = ["onprem-demo-5", "onprem-demo-6", "onprem-demo-7", "onprem-demo-8"]
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

variable "location" {
  description = "Azure region for the resource group and VM. eastus2 because this subscription can hold only 3 Standard public IPv4 addresses in eastus, and the other demo VMs already use that quota."
  type        = string
  default     = "eastus2"
}

variable "name" {
  description = "Short name used for the resource group, VM, and key file."
  type        = string
  default     = "onprem-demo-4"
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

variable "allowed_cidr" {
  description = "Source CIDR allowed to SSH (22) and reach the app (8080). Use your public IP, for example 203.0.113.10/32, when you are not testing from anywhere."
  type        = string
  default     = "*"
}

variable "os_disk_size_gb" {
  description = "OS disk size in GiB. 30 is the Ubuntu image minimum."
  type        = number
  default     = 30
}


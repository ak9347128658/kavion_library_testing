output "resource_group_name" {
  description = "Resource group that holds this VM."
  value       = azurerm_resource_group.main.name
}

output "public_ip" {
  description = "Static public IP of the VM."
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_user" {
  description = "Linux user for SSH."
  value       = var.admin_username
}

output "pem_file" {
  description = "Private key written next to this Terraform config. Keep it out of git."
  value       = local_sensitive_file.pem.filename
}

output "ssh_command" {
  description = "SSH into the VM."
  value       = "ssh -i ${var.name}.pem ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

output "app_url" {
  description = "HTTP URL for the on-prem host once it listens on 0.0.0.0:8080."
  value       = "http://${azurerm_public_ip.main.ip_address}:8080"
}

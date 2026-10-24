output "resource_group_name" {
  description = "Resource group that holds machines 5 through 8."
  value       = azurerm_resource_group.main.name
}

output "public_ip" {
  description = "Static public IP of each VM."
  value       = { for name, pip in azurerm_public_ip.main : name => pip.ip_address }
}

output "ssh_user" {
  description = "Linux user for SSH."
  value       = var.admin_username
}

output "pem_file" {
  description = "Private key for each VM, written next to this Terraform config. Keep these out of git."
  value       = { for name, key in local_sensitive_file.pem : name => key.filename }
}

output "ssh_command" {
  description = "SSH into each VM."
  value       = { for name, pip in azurerm_public_ip.main : name => "ssh -i ${name}.pem ${var.admin_username}@${pip.ip_address}" }
}

output "app_url" {
  description = "HTTP URL for each on-prem host once it listens on 0.0.0.0:8080."
  value       = { for name, pip in azurerm_public_ip.main : name => "http://${pip.ip_address}:8080" }
}

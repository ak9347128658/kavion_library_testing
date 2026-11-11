output "resource_group_name" {
  description = "Resource group that holds the storage account."
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Generated storage account name."
  value       = azurerm_storage_account.main.name
}

output "container_name" {
  description = "Name of the blob container."
  value       = azurerm_storage_container.main.name
}

output "blob_endpoint" {
  description = "Blob service endpoint of the storage account."
  value       = azurerm_storage_account.main.primary_blob_endpoint
}

output "container_url" {
  description = "Full URL of the container. Private, so requests need credentials."
  value       = "${azurerm_storage_account.main.primary_blob_endpoint}${azurerm_storage_container.main.name}"
}

output "portal_url" {
  description = "Opens the storage account in the Azure portal."
  value       = "https://portal.azure.com/#@${data.azurerm_client_config.current.tenant_id}/resource${azurerm_storage_account.main.id}"
}

output "primary_connection_string" {
  description = "Connection string for SDKs. Read with: terraform output -raw primary_connection_string"
  value       = azurerm_storage_account.main.primary_connection_string
  sensitive   = true
}

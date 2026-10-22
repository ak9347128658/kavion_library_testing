output "resource_group_name" {
  description = "Resource group that holds the storage account."
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Storage account that owns the queue."
  value       = azurerm_storage_account.main.name
}

output "queue_name" {
  description = "Name of the queue."
  value       = azurerm_storage_queue.main.name
}

output "queue_endpoint" {
  description = "Queue service endpoint of the storage account."
  value       = azurerm_storage_account.main.primary_queue_endpoint
}

output "queue_url" {
  description = "Full URL of the queue."
  value       = "${azurerm_storage_account.main.primary_queue_endpoint}${azurerm_storage_queue.main.name}"
}

output "queue_resource_id" {
  description = "Azure resource ID of the queue, for role assignments."
  value       = azurerm_storage_queue.main.id
}

output "portal_url" {
  description = "Opens the storage account in the Azure portal. Go to Data storage > Queues from there."
  value       = "https://portal.azure.com/#@${data.azurerm_client_config.current.tenant_id}/resource${azurerm_storage_account.main.id}/queueList"
}

output "primary_access_key" {
  description = "Storage account key. Read with: terraform output -raw primary_access_key"
  value       = azurerm_storage_account.main.primary_access_key
  sensitive   = true
}

output "primary_connection_string" {
  description = "Connection string for SDKs. Read with: terraform output -raw primary_connection_string"
  value       = azurerm_storage_account.main.primary_connection_string
  sensitive   = true
}

output "az_cli_send_message" {
  description = "Send a test message with the Azure CLI."
  value       = "az storage message put --account-name ${azurerm_storage_account.main.name} --queue-name ${azurerm_storage_queue.main.name} --content '{\"hello\":\"world\"}' --auth-mode key"
}

output "az_cli_peek_messages" {
  description = "Look at messages without removing them."
  value       = "az storage message peek --account-name ${azurerm_storage_account.main.name} --queue-name ${azurerm_storage_queue.main.name} --num-messages 5 --auth-mode key"
}

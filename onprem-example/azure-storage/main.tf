data "azurerm_client_config" "current" {}

# Storage account names are global: 3-24 chars, lowercase letters and numbers only.
resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

locals {
  storage_account_name = substr("${replace(lower(var.name), "/[^a-z0-9]/", "")}${random_string.suffix.result}", 0, 24)
}

resource "azurerm_resource_group" "main" {
  name     = "${var.name}-storage-rg"
  location = var.location

  tags = {
    purpose = "onprem-example-storage-test"
  }
}

resource "azurerm_storage_account" "main" {
  name                     = local.storage_account_name
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = var.replication_type
  account_kind             = "StorageV2"
  min_tls_version          = "TLS1_2"

  # Keys stay enabled so the connection string output works.
  shared_access_key_enabled       = true
  allow_nested_items_to_be_public = false

  tags = azurerm_resource_group.main.tags
}

resource "azurerm_storage_container" "main" {
  name                  = var.container_name
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}

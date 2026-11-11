# Azure storage account with a blob container

Terraform for a private Azure storage account and blob container used to test the on-prem example. The Terraform state holds the connection string and is gitignored.

## What you get

| Piece | Default |
| --- | --- |
| Region | `eastus` |
| Resource group | `onprem-demo-storage-rg` |
| Storage account | `onpremdemo<unique suffix>` |
| Redundancy | `LRS` |
| Container | `invoices` |
| Access level | Private |
| Minimum TLS | 1.2 |

Azure bills for stored data and requests while they exist. Run `terraform destroy` when you are done testing.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or newer
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), logged in:

```powershell
az login
az account set --subscription "<subscription name or id>"
```

The AzureRM provider reads the subscription from `az login`, or from the `ARM_SUBSCRIPTION_ID` environment variable.

## Create the storage

```powershell
cd onprem-example\azure-storage
terraform init
terraform apply
```

## Get the connection string

```powershell
terraform output -raw primary_connection_string
```

This is the same value as key1 Connection string under Security + networking > Access keys in the portal. It grants full access to the account, so keep it out of git.

## Use it

```powershell
$env:AZURE_STORAGE_CONNECTION_STRING = terraform output -raw primary_connection_string
az storage blob upload --container-name invoices --file .\README.md --name README.md
az storage blob list --container-name invoices --output table
```

## Remove

```powershell
terraform destroy
```

Destroy deletes the storage account and every blob in it, for good.

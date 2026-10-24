# Azure small Ubuntu VMs (Machines 9–12)

One Terraform config for four Ubuntu 22.04 VMs in a single resource group. Each VM has its own static public IP, NIC, disk, and SSH key. They share one VNet, one subnet, and one network security group.

The inbound rule on that group is `allow_all`: source Any, source port `*`, destination Any, destination port `*` (service Custom), protocol Any, action Allow.

Private keys are written to `onprem-demo-9.pem` through `onprem-demo-12.pem` in this folder when you apply. Those files and the Terraform state are gitignored.

## What you get

| Piece | Default |
| --- | --- |
| Resource group | `onprem-demo-9-12-rg` |
| Region | `centralindia` |
| VMs | `onprem-demo-9` through `onprem-demo-12` |
| Size | `Standard_F2as_v7` (2 vCPU, 8 GiB) |
| Image | Ubuntu 22.04 LTS Gen2 |
| Login | `azureuser` over SSH key only |
| Inbound | `allow_all` (any source, any port, any protocol) |
| Disk | 30 GiB Standard HDD each |

This subscription allows 3 Standard public IPv4 addresses and 4 regional vCPUs in `centralindia`. These four VMs need 4 public IPs and 8 vCPUs, which is over both quotas, so `terraform apply` cannot create every VM until the quotas are raised. Machines 5–8 use this same region, so the two groups share that quota. `centralindia` is empty today.

The VMs are billed while they exist. Run `terraform destroy` when you are done testing.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or newer
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), logged in:

```powershell
az login
az account set --subscription "<subscription name or id>"
```

The AzureRM provider reads the subscription from `az login`, or from the `ARM_SUBSCRIPTION_ID` environment variable.

## Create the VMs

`terraform init` has been run. Apply has not.

```powershell
cd onprem-example\azure-small-machine-9-12
terraform apply
```

## SSH

From this folder, after apply:

```powershell
ssh -i onprem-demo-9.pem azureuser@<public_ip>
```

`<public_ip>` is that VM's entry in the `public_ip` output. On Windows, if OpenSSH rejects the key, lock the file down:

```powershell
icacls onprem-demo-9.pem /inheritance:r /grant:r "${env:USERNAME}:(R)"
```

## Remove

```powershell
terraform destroy
```

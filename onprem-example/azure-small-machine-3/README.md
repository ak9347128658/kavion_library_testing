# Azure small Ubuntu VM (Machine 3)

Terraform for a third small Ubuntu 22.04 box used to test the on-prem example. It creates a resource group, a static public IP, SSH on port 22, and TCP 8080 for `pskit deploy`.

The private key is written to `onprem-demo-3.pem` in this folder when you apply. That file and the Terraform state are gitignored.

## What you get

| Piece | Default |
| --- | --- |
| Region | `eastus` |
| Size | `Standard_F2as_v7` (2 vCPU, 8 GiB) |
| Image | Ubuntu 22.04 LTS Gen2 |
| Login | `azureuser` over SSH key only |
| Open ports | 22 and 8080 |
| Disk | 30 GiB Standard HDD |

The VM is billed while it exists. Run `terraform destroy` when you are done testing.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or newer
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), logged in:

```powershell
az login
az account set --subscription "<subscription name or id>"
```

The AzureRM provider reads the subscription from `az login`, or from the `ARM_SUBSCRIPTION_ID` environment variable.

## Create the VM

```powershell
cd onprem-example\azure-small-machine-3
terraform init
terraform apply
```

To allow only your current IP, set `allowed_cidr` before apply:

```powershell
terraform apply -var "allowed_cidr=$(curl.exe -s https://ifconfig.me)/32"
```

## SSH

From this folder:

```powershell
ssh -i onprem-demo-3.pem azureuser@<public_ip>
```

`<public_ip>` is the `public_ip` output. On Windows, if OpenSSH rejects the key, lock the file down:

```powershell
icacls onprem-demo-3.pem /inheritance:r /grant:r "${env:USERNAME}:(R)"
```

## Deploy the example on the VM

The sample `pskit.yml` binds `127.0.0.1`, which is not reachable through the public IP. On the VM, set the host to all interfaces and keep port 8080:

```yaml
provider:
  name: onprem
  options:
    host: 0.0.0.0
    port: 8080
    advertise: http://<public_ip>:8080
```

Then install Python 3 and the kit, and start the host:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
python3 -m venv ~/pskit-venv
source ~/pskit-venv/bin/activate
pip install py-serverless-kit
# copy onprem-example onto the VM, then:
cd onprem-example
pskit deploy
```

Check from your machine:

```powershell
curl http://<public_ip>:8080/__pskit/health
```

## Remove

```powershell
terraform destroy
```


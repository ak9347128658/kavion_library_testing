# AWS small Ubuntu instance (Machine 2)

Terraform for a second small Ubuntu 22.04 box used to test the on-prem example. It creates a VPC, an Elastic IP, and an inbound `allow_all` rule.

The private key is written to `onprem-demo-2.pem` in this folder when you apply. That file and the Terraform state are gitignored.

## What you get

| Piece | Default |
| --- | --- |
| Region | `us-east-1` |
| Size | `t3.large` (2 vCPU, 8 GiB) |
| Image | Ubuntu 22.04 LTS |
| Login | `ubuntu` over SSH key only |
| Inbound | `allow_all`, all protocols, all ports, source `0.0.0.0/0` |
| Disk | 30 GiB gp3 |

The instance is billed while it exists. An unattached Elastic IP is billed too. Run `terraform destroy` when you are done testing.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or newer
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), with credentials:

```powershell
aws configure
aws sts get-caller-identity
```

The AWS provider reads the default credential chain: the AWS CLI profile, `AWS_PROFILE`, or `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

## Create the instance

```powershell
cd onprem-example\aws-small-machine-2
terraform init
terraform apply
```

## SSH

From this folder:

```powershell
ssh -i onprem-demo-2.pem ubuntu@<public_ip>
```

`<public_ip>` is the `public_ip` output. On Windows, if OpenSSH rejects the key, lock the file down:

```powershell
icacls onprem-demo-2.pem /inheritance:r /grant:r "${env:USERNAME}:(R)"
```

## Deploy the example on the instance

The sample `pskit.yml` binds `127.0.0.1`, which is not reachable through the public IP. On the instance, set the host to all interfaces and keep port 8080:

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
# copy onprem-example onto the instance, then:
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

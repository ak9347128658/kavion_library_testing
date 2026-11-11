# AWS S3 bucket

Terraform for a private S3 bucket used to test the on-prem example. The Terraform state is gitignored.

## What you get

| Piece | Default |
| --- | --- |
| Region | `us-east-1` |
| Name | `onprem-demo-<unique suffix>` |
| Public access | All blocked |
| Encryption | SSE-S3 (`AES256`) |
| Versioning | Off |

S3 bills for stored objects and requests while they exist. Run `terraform destroy` when you are done testing.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or newer
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), with credentials:

```powershell
aws configure
aws sts get-caller-identity
```

The AWS provider reads the default credential chain: the AWS CLI profile, `AWS_PROFILE`, or `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

## Create the bucket

```powershell
cd onprem-example\aws-s3-bucket
terraform init
terraform apply
```

## Use it

`<bucket_name>` is the `bucket_name` output.

```powershell
aws s3 cp .\README.md s3://<bucket_name>/README.md
aws s3 ls s3://<bucket_name>/
```

## Remove

```powershell
terraform destroy
```

Destroy fails while the bucket still holds objects. Empty it first, or set `force_destroy = true` and run `terraform apply` before destroying. With `force_destroy`, the objects are deleted for good.

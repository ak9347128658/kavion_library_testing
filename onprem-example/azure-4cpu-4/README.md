# Azure Ubuntu VM (onprem-4cpu-4)

One Terraform config for a single Ubuntu 22.04 VM. It has its own resource group, VNet, static public IP, and SSH key.

The inbound rule is `allow_all`: source Any, source port `*`, destination Any, destination port `*` (service Custom), protocol Any, action Allow.

Size is `Standard_F4as_v7` (4 vCPU, 16 GiB) in `centralindia`. This subscription allows 4 regional vCPUs in that region, so only one VM of this size can exist there at a time. The other `azure-4cpu-*` folders use the same region.

`terraform init` has been run. Apply has not.

The VM is billed while it exists. Run `terraform destroy` when you are done testing.

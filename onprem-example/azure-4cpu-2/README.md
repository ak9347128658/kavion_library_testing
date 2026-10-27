# Azure Ubuntu VM (onprem-4cpu-2)

One Terraform config for a single Ubuntu 22.04 VM. It has its own resource group, VNet, static public IP, and SSH key.

The inbound rule is `allow_all`: source Any, source port `*`, destination Any, destination port `*` (service Custom), protocol Any, action Allow.

Size is `Standard_F2as_v7` (2 vCPU, 8 GiB) in `centralus`, the same region as `azure-4cpu-1`. This subscription allows 4 regional vCPUs there, so two VMs of this size can exist in that region at a time. `onprem-4cpu-1` is `Standard_F4as_v7` and uses the whole quota while it is running. `centralindia` returned `AllocationFailed` for that 4 vCPU size. The subscription also allows only 3 Standard public IPv4 addresses per region.

`terraform init` has been run. Apply has not.

The VM is billed while it exists. Run `terraform destroy` when you are done testing.

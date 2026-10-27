# Azure Ubuntu VM (onprem-4cpu-3)

One Terraform config for a single Ubuntu 22.04 VM. It has its own resource group, VNet, static public IP, and SSH key.

The inbound rule is `allow_all`: source Any, source port `*`, destination Any, destination port `*` (service Custom), protocol Any, action Allow.

Size is `Standard_F2as_v7` (2 vCPU, 8 GiB) in `southcentralus`. This subscription allows 4 regional vCPUs and 3 Standard public IPv4 addresses per region. `centralus` is full: `onprem-4cpu-1` is `Standard_F4as_v7` and uses all 4 vCPUs, so a VM of this size there returned `OperationNotAllowed` (limit 4, usage 4, required 2). `southcentralus` has this SKU with no location restriction and unused vCPU and public IP quota. `centralindia` returned `AllocationFailed` for the 4 vCPU size.

`terraform init` has been run. The VM is applied in `southcentralus`.

The VM is billed while it exists. Run `terraform destroy` when you are done testing.

# Azure Storage Queue

Terraform for a small Azure Storage Queue to use with the on-prem example. It creates a resource group, a Standard LRS storage account, and one queue.

It sits next to `azure-small-machine` and uses the same region, naming style, and login.

## What you get

| Piece | Default |
| --- | --- |
| Resource group | `onprem-demo-queue-rg` |
| Region | `eastus` |
| Storage account | `onpremdemo<6 random chars>` (names must be unique across Azure) |
| Redundancy | `LRS` (Standard tier, StorageV2) |
| Queue | `onprem-demo-jobs` |
| Auth | Access key (on), plus optional Entra ID role for you |
| TLS | 1.2 minimum |

Storage queues cost very little when idle: you pay per GB stored and per 10,000 operations. Run `terraform destroy` when you are done.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or newer
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), logged in:

```powershell
az login
az account set --subscription "<subscription name or id>"
```

## Create the queue

```powershell
cd onprem-example\azure-queue
terraform init
terraform apply
```

To change the queue name or region, copy `terraform.tfvars.example` to `terraform.tfvars` and edit it, or pass `-var`:

```powershell
terraform apply -var "queue_name=orders" -var "location=westeurope"
```

To also give yourself the **Storage Queue Data Contributor** role (lets the portal and `az` use your Entra ID login instead of the key; you need Owner or User Access Administrator):

```powershell
terraform apply -var "grant_current_user=true"
```

Role assignments can take a few minutes to apply.

## Queue details after apply

Terraform prints these at the end of `apply`. To see them again:

```powershell
terraform output
```

| Output | What it is | Example |
| --- | --- | --- |
| `resource_group_name` | Resource group | `onprem-demo-queue-rg` |
| `storage_account_name` | Storage account | `onpremdemoa1b2c3` |
| `queue_name` | Queue | `onprem-demo-jobs` |
| `queue_endpoint` | Queue service endpoint | `https://onpremdemoa1b2c3.queue.core.windows.net/` |
| `queue_url` | Full queue URL | `https://onpremdemoa1b2c3.queue.core.windows.net/onprem-demo-jobs` |
| `queue_resource_id` | Azure resource ID, for role assignments | `/subscriptions/.../queueServices/default/queues/onprem-demo-jobs` |
| `portal_url` | Opens the queue list in the portal | `https://portal.azure.com/#@<tenant>/resource/.../queueList` |
| `az_cli_send_message` | Ready-to-run send command | |
| `az_cli_peek_messages` | Ready-to-run peek command | |
| `primary_access_key` | Account key (secret) | hidden |
| `primary_connection_string` | SDK connection string (secret) | hidden |

The key and connection string are marked sensitive. Print them only when you need them:

```powershell
terraform output -raw primary_connection_string
terraform output -raw primary_access_key
```

Treat both as passwords. Anyone with them has full access to the storage account. They are also stored in plain text in `terraform.tfstate`, which `.gitignore` in this folder keeps out of git.

## Add a message in the Azure portal

1. Open [portal.azure.com](https://portal.azure.com) and sign in. Or open the `portal_url` output and skip to step 4.
2. In the top search bar, type the `storage_account_name` output (for example `onpremdemoa1b2c3`) and select it. You can also go to **Resource groups** > `onprem-demo-queue-rg` > the storage account.
3. In the left menu, under **Data storage**, select **Queues**.
4. Select the queue, `onprem-demo-jobs`.
5. Select **+ Add message** on the toolbar.
6. Fill in the panel:
   - **Message text**: the body, for example `{"order_id": "A-100", "priority": "high"}`. Max 64 KB.
   - **Expires in**: how long the message lives. The default is 7 days. Tick **Message never expires** to keep it until it is deleted.
   - **Encode the message body in Base64**: tick it if your consumer expects Base64. The Azure Functions queue trigger and the Python SDK's `BinaryBase64DecodePolicy` expect Base64. Leave it off for consumers that read plain text.
7. Select **OK**.

The message appears in the list with its **ID**, **Message text**, **Insertion time**, **Expiration time**, and **Dequeue count**.

### Other actions on the same page

- **Refresh**: reload the list. The portal shows up to 32 messages, oldest first.
- **Dequeue message**: removes the oldest message.
- **Clear queue**: deletes every message in the queue.
- Select a message to see its full text.

### If the portal says you do not have permission

The **Authentication method** line at the top of the queue page shows **Access key** or **Microsoft Entra user account**.

- Select **Switch to Access key** if you see Entra ID and get a permission error. This needs the `Microsoft.Storage/storageAccounts/listkeys/action` permission, which Contributor and Owner have.
- To use Entra ID instead, apply with `grant_current_user=true` (above), wait a few minutes, and refresh.

### Storage browser

The same actions are under **Storage browser** > **Queues** in the left menu of the storage account. [Azure Storage Explorer](https://azure.microsoft.com/products/storage/storage-explorer/) on the desktop works the same way.

## Add a message from the command line

Copy the command from the output:

```powershell
terraform output -raw az_cli_send_message
```

Or write it out:

```powershell
$acct  = terraform output -raw storage_account_name
$queue = terraform output -raw queue_name

az storage message put --account-name $acct --queue-name $queue --content "hello" --auth-mode key
az storage message peek --account-name $acct --queue-name $queue --num-messages 5 --auth-mode key
```

Use `--auth-mode login` instead of `key` if you applied with `grant_current_user=true`.

## Use it from Python

```bash
pip install azure-storage-queue
```

```python
import os
from azure.storage.queue import QueueClient

queue = QueueClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"],
    "onprem-demo-jobs",
)

queue.send_message('{"order_id": "A-100"}')

for msg in queue.receive_messages(messages_per_page=10, visibility_timeout=30):
    print(msg.id, msg.content)
    queue.delete_message(msg)
```

Set the variable from the output:

```powershell
$env:AZURE_STORAGE_CONNECTION_STRING = terraform output -raw primary_connection_string
```

A received message is hidden for `visibility_timeout` seconds. If you do not delete it in that time, it comes back and its dequeue count goes up.

## Remove

```powershell
terraform destroy
```

This deletes the resource group, storage account, queue, and every message in it.

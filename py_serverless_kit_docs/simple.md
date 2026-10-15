```markdown
# py-serverless-kit Guide  
**GET / POST / PUT APIs + ARN function + Azure deploy**

## 1. Install
```bash
pip install py-serverless-kit
# optional for AWS invoke
pip install "py-serverless-kit[aws]"
```
Requires **Terraform ≥ 1.5** (or OpenTofu) on your PATH.

## 2. Scaffold project
```bash
pskit init my-api --provider aws --template http
cd my-api
```

## 3. Handlers (`app/handlers.py`)
```python
from py_serverless_kit import Event, Context, NotFound, BadRequest, Response

ITEMS = {}   # demo only

def list_items(event: Event, ctx: Context):
    return {"items": list(ITEMS.values())}

def get_item(event: Event, ctx: Context):
    item_id = event.http.path_params["id"]
    item = ITEMS.get(item_id)
    if not item:
        raise NotFound(f"item {item_id} not found")
    return item

def create_item(event: Event, ctx: Context):
    body = event.http.json()
    if not isinstance(body, dict) or "name" not in body:
        raise BadRequest("name is required")
    item_id = str(len(ITEMS) + 1)
    ITEMS[item_id] = {"id": item_id, **body}
    return Response.json(ITEMS[item_id], status=201,
                         headers={"location": f"/items/{item_id}"})

def update_item(event: Event, ctx: Context):
    item_id = event.http.path_params["id"]
    if item_id not in ITEMS:
        raise NotFound(f"item {item_id} not found")
    ITEMS[item_id].update(event.http.json())
    return ITEMS[item_id]

def get_arn(event: Event, ctx: Context):
    """Invoke-only function (no HTTP API). Returns ARN on AWS."""
    info = {
        "function": ctx.function,
        "service": ctx.service,
        "stage": ctx.stage,
        "region": ctx.region,
        "provider": ctx.provider,
        "request_id": ctx.request_id,
    }
    arn = None
    if ctx.provider == "aws" and ctx.raw is not None:
        arn = getattr(ctx.raw, "invoked_function_arn", None)
    if not arn:
        arn = f"arn:aws:lambda:{ctx.region}:ACCOUNT:function:{ctx.service}-{ctx.stage}-{ctx.function}"
    return {"arn": arn, **info}
```

## 4. `pskit.yml`
```yaml
service: my-api
provider:
  name: aws
  region: us-east-1

functions:
  list-items:
    handler: app.handlers.list_items
    events:
      - http: GET /items

  get-item:
    handler: app.handlers.get_item
    events:
      - http: GET /items/{id}

  create-item:
    handler: app.handlers.create_item
    events:
      - http: POST /items

  update-item:
    handler: app.handlers.update_item
    events:
      - http: PUT /items/{id}

  # Non-API function (invoke only)
  get-arn:
    handler: app.handlers.get_arn
```

## 5. Local test
```bash
pskit dev
# curl http://127.0.0.1:3000/items
# curl -X POST http://127.0.0.1:3000/items -d '{"name":"Widget"}'
# curl -X PUT  http://127.0.0.1:3000/items/1 -d '{"name":"Updated"}'

pskit invoke -f get-arn          # non-API function
```

## 6. Deploy (AWS)
```bash
pskit validate
pskit deploy --stage dev
```

### Get ARNs & endpoints
```bash
pskit info
pskit info --json
pskit dashboard --open
```

## 7. Undeploy / Remove
```bash
pskit remove
pskit remove --stage dev -y
pskit remove --provider azure -y
```

## 8. Switch to Azure

### Update `pskit.yml`
```yaml
provider:
  name: azure
  region: eastus

providers:
  azure:
    region: eastus
    options:
      subscription_id: "${env:ARM_SUBSCRIPTION_ID}"
```

### Install Azure CLI (Windows)
```powershell
winget install -e --id Microsoft.AzureCLI
# then reopen terminal
az login
```

### Get Subscription ID (Azure Portal)
1. Go to https://portal.azure.com
2. Search for **Subscriptions**
3. Copy the **Subscription ID**

### Deploy to Azure
```powershell
$env:ARM_SUBSCRIPTION_ID = "your-subscription-id"
pskit validate --provider azure
pskit deploy --provider azure --stage dev
pskit info
```

## Official example
https://github.com/ak9347128658/serverless_kit/tree/main/examples/02-rest-api

## Docs
https://github.com/ak9347128658/serverless_kit
```

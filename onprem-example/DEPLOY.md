# On-Premises Deployment Guide
# py-serverless-kit (pskit)

This example demonstrates a complete on-premises deployment with:

- **2 GET APIs**: `GET /items`, `GET /items/{id}`
- **2 POST APIs**: `POST /items`, `POST /orders`
- **1 invoke-only function**: `price-calculator` (called from `process-order`)
- **3 workflows (Step Functions style)**: `order-pipeline`, `simple-ping`, `support-escalation`

The same code and `pskit.yml` can be deployed to AWS, GCP, Azure, etc. by changing `provider.name`.

---

## Prerequisites

```bash
pip install py-serverless-kit
# Terraform ≥ 1.5 or OpenTofu must be on PATH
terraform version
```

Python ≥ 3.9 is required for the CLI. The on-prem host uses the same interpreter (or a bundled CPython for remote hosts without Python).

---

## Project structure

```
onprem-example/
├── pskit.yml              # service definition (provider: onprem)
├── requirements.txt
└── app/
    └── handlers.py        # all handlers
```

---

## 1. Local development (hot-reload HTTP)

```bash
cd onprem-example
pskit dev
# → http://127.0.0.1:3000
```

```bash
# GET APIs
curl "http://127.0.0.1:3000/items"
curl "http://127.0.0.1:3000/items/1"

# POST APIs
curl -X POST http://127.0.0.1:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"New Widget","price":12.5}'

curl -X POST http://127.0.0.1:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"items":[{"sku":"a","qty":2,"unit_price":10}],"country":"DE"}'
```

Test individual functions (including invoke-only and workflow tasks):

```bash
pskit invoke -f list-items --path /items
pskit invoke -f price-calculator -d '{"items":[{"unit_price":10,"qty":1}],"country":"US"}'
pskit invoke -f validate-order -d '{"customer_id":"c1","items":[{}]}'
```

---

## 2. Deploy on-premises (durable host)

```bash
pskit validate                 # check config
pskit deploy                   # starts the host process
# Host listens on http://127.0.0.1:8080
```

After deploy:

```bash
pskit info                     # endpoints, resource ids
pskit dashboard --open         # HTML dashboard
```

### Call the APIs

```bash
# Health
curl http://127.0.0.1:8080/__pskit/health

# GET
curl http://127.0.0.1:8080/items
curl http://127.0.0.1:8080/items/1

# POST
curl -X POST http://127.0.0.1:8080/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Gadget Pro","price":29.99}'

curl -X POST http://127.0.0.1:8080/orders \
  -H "Content-Type: application/json" \
  -d '{"items":[{"sku":"x","qty":1,"unit_price":100}],"country":"IN"}'
```

### Invoke a function directly

```bash
curl -X POST http://127.0.0.1:8080/__pskit/invoke/price-calculator \
  -H "Content-Type: application/json" \
  -d '{"items":[{"unit_price":50,"qty":2}],"country":"DE"}'
```

### Run workflows (the 3 step functions)

```bash
# order-pipeline
curl -X POST http://127.0.0.1:8080/__pskit/workflows/order-pipeline \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"cust-1","items":[{"sku":"a","qty":1}],"priority":"normal"}'

# simple-ping
curl -X POST http://127.0.0.1:8080/__pskit/workflows/simple-ping \
  -d '{"customer_id":"c2","items":[{}]}'

# support-escalation
curl -X POST http://127.0.0.1:8080/__pskit/workflows/support-escalation \
  -d '{"priority":"high","customer_id":"c3"}'
```

You can also use the CLI:

```bash
pskit workflow run order-pipeline -i '{"customer_id":"c1","items":[{}]}'
pskit workflow show order-pipeline
```

---

## 3. Admin endpoints (queues, topics, storage)

The host exposes internal endpoints under `/__pskit/*`:

| Method | Path | Purpose |
|--------|------|---------|
| GET    | `/__pskit/health` | status |
| POST   | `/__pskit/queues/<name>` | enqueue |
| POST   | `/__pskit/topics/<name>` | publish |
| PUT    | `/__pskit/storage/<bucket>/<key>` | put object |
| POST   | `/__pskit/invoke/<function>` | in-process invoke |
| POST   | `/__pskit/workflows/<name>` | run workflow |

Set `options.admin_token` in `pskit.yml` and send header `x-pskit-token` to protect them (except `/health`).

---

## 4. Remote on-premises deploy

### SSH

```yaml
provider:
  name: onprem
  options:
    host: 0.0.0.0          # bind on the remote machine
    port: 8080
    advertise: http://10.0.1.12:8080
    deploy:
      method: ssh
      host: 10.0.1.12
      user: deploy
      # python: bundle   # if the server has no Python
```

```bash
pskit deploy
```

### Docker

```yaml
deploy:
  method: docker
  image: pskit/onprem-demo:dev
  docker_host: ssh://deploy@10.0.1.12   # optional remote daemon
  restart: unless-stopped
```

See the official examples:

- [examples/16-on-premises](https://github.com/ak9347128658/serverless_kit/tree/main/examples/16-on-premises)
- [examples/17-on-premises-remote](https://github.com/ak9347128658/serverless_kit/tree/main/examples/17-on-premises-remote)

---

## 5. Stop / remove

```bash
pskit remove -y          # stops the host process (data directories are kept)
```

---

## 6. Switching to a cloud

Change one line and redeploy:

```yaml
provider:
  name: aws          # or gcp, azure, ...
  region: us-east-1
```

```bash
pskit deploy --provider aws
```

Workflows become native Step Functions on AWS and Cloud Workflows on GCP; the embedded engine is used everywhere else (including on-prem).

---

## Useful commands

| Command | Description |
|---------|-------------|
| `pskit validate` | Check config against provider capabilities |
| `pskit package` | Build the artifact without deploying |
| `pskit invoke -f <name>` | Invoke a function locally |
| `pskit workflow run <name>` | Run a workflow locally |
| `pskit info` | Show deployed endpoints |
| `pskit dashboard --open` | Open the HTML dashboard |
| `pskit providers` | List all supported clouds and features |

---

## Notes

- On-prem is marked **experimental**. Delivery is at-least-once. Handlers are not forcibly killed at timeout (but `ctx.remaining_time_ms()` still works).
- State lives under `.pskit/onprem-data/` and `.onprem/buckets/`.
- For production, point `services.queue`, `storage`, etc. at durable directories or existing infrastructure.
- Auth on HTTP is `none` — implement token checks inside handlers if needed.

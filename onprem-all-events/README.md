# On-prem all-events + 3-step workflow example

This project deploys every supported on-prem trigger (HTTP, schedule, queue, storage, topic) plus an embedded 3-step workflow to the remote host using the SSH + systemd + bundled-Python method that previously worked.

## Layout

```
onprem-all-events/
  pskit.yml
  requirements.txt
  app/
    handlers.py
```

## Deploy

```bash
pip install py-serverless-kit
cd onprem-all-events
pskit deploy
```

After a successful deploy the host listens on `http://20.106.136.236:8080`.

## Test endpoints

```bash
# Health
curl http://20.106.136.236:8080/__pskit/health

# HTTP
curl http://20.106.136.236:8080/hello?name=Ada
curl -X POST http://20.106.136.236:8080/hello -d '{"msg":"hi"}' -H 'Content-Type: application/json'

# Queue
curl -X POST http://20.106.136.236:8080/__pskit/queues/jobs -d '{"kind":"email"}'
curl -X POST http://20.106.136.236:8080/__pskit/queues/jobs -d '{"kind":"email","fail":true}'

# Topic
curl -X POST http://20.106.136.236:8080/__pskit/topics/orders \
  -d '{"message":{"id":1},"attributes":{"event_type":"order.shipped"}}'

# Storage (creates the file under the bucket directory)
curl -X PUT http://20.106.136.236:8080/__pskit/storage/uploads/in/report.csv --data-binary 'a,b,c'

# Workflow (3 steps)
curl -X POST http://20.106.136.236:8080/__pskit/workflows/three-step-pipeline \
  -d '{"amount": 42}'
```

Schedules fire automatically inside the host process.

## Notes

- `provider.name` must be exactly `onprem`.
- The `deploy` block matches the previously working remote configuration (SSH, PEM, systemd, bundled Python).
- On first apply the portable CPython is downloaded (needs network on the machine running `pskit deploy`).
- Data (queues, topics, storage files) lives under the `data_dir` on the server.

"""Handlers for all on-prem event types. Same code runs on AWS/GCP/Azure/etc."""

from __future__ import annotations

from py_serverless_kit import BatchResult, Context, Event


def hello(event: Event, ctx: Context):
    """HTTP event."""
    name = event.http.query.get("name", "world")
    ctx.logger.info("greeting", extra={"name": name})
    return {
        "message": f"Hello, {name}!",
        "provider": event.provider,
        "stage": ctx.stage,
        "path": event.http.path,
    }


def tick(event: Event, ctx: Context):
    """Schedule event. event.data contains the input from pskit.yml."""
    ctx.logger.info("tick", extra={"data": event.data, "time": str(event.time)})
    return {"ok": True, "data": event.data}


def worker(event: Event, ctx: Context):
    """Queue event with partial batch failure support."""
    result = BatchResult()
    for record in event.records:
        job = record.json()
        if isinstance(job, dict) and job.get("fail"):
            ctx.logger.error("job failed", extra={"message_id": record.id})
            result.fail(record)          # only this message is retried
            continue
        ctx.logger.info("job done", extra={"message_id": record.id, "body": job})
    return result


def audit_dlq(event: Event, ctx: Context):
    """Dead-letter queue handler."""
    for record in event.records:
        ctx.logger.error(
            "dead letter",
            extra={"message_id": record.id, "body": record.text()[:500]},
        )
    return {"seen": len(event.records)}


def on_upload(event: Event, ctx: Context):
    """Storage event (file created/deleted under the bucket directory)."""
    keys = []
    for record in event.records:
        ctx.logger.info(
            "object",
            extra={"key": record.key, "action": record.action, "size": record.size},
        )
        keys.append(record.key)
    return {"keys": keys}


def on_order(event: Event, ctx: Context):
    """Topic event."""
    ctx.logger.info("order event", extra={"count": len(event.records)})
    for record in event.records:
        ctx.logger.info("message", extra={"body": record.json(), "attrs": record.attributes})
    return {"records": len(event.records)}


def mark(event: Event, ctx: Context):
    """Workflow task (or direct invoke)."""
    data = dict(event.data or {})
    data["seen"] = True
    data["provider"] = event.provider
    ctx.logger.info("marked", extra=data)
    return data
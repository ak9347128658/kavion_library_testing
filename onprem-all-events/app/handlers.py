"""Handlers covering every on-prem event type + the 3 workflow steps.

Same code works on any cloud. On-prem the host delivers events via the
__pskit/* control endpoints or the built-in file brokers.
"""

from __future__ import annotations

from typing import Any, Dict

from py_serverless_kit import BatchResult, Context, Event, Response


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def hello(event: Event, ctx: Context) -> Dict[str, Any]:
    if event.http.method == "GET":
        name = event.http.query.get("name", "world")
        return {"message": f"Hello, {name}!", "provider": event.provider, "stage": ctx.stage}
    # POST
    body = event.http.json(default={})
    return Response.json({"echo": body, "request_id": ctx.request_id}, status=200)


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------
def tick(event: Event, ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("scheduled tick", extra={"data": event.data})
    return {"ok": True, "received": event.data}


# ---------------------------------------------------------------------------
# Queue
# ---------------------------------------------------------------------------
def worker(event: Event, ctx: Context) -> BatchResult:
    result = BatchResult()
    for record in event.records:
        job = record.json()
        if isinstance(job, dict) and job.get("fail"):
            ctx.logger.error("job failed", extra={"id": record.id})
            result.fail(record)
            continue
        ctx.logger.info("job processed", extra={"id": record.id, "payload": job})
    return result


def audit_dlq(event: Event, ctx: Context) -> Dict[str, Any]:
    for record in event.records:
        ctx.logger.error("dead-letter", extra={"id": record.id, "body": record.text()[:300]})
    return {"seen": len(event.records)}


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
def on_upload(event: Event, ctx: Context) -> Dict[str, Any]:
    keys = []
    for record in event.records:
        ctx.logger.info(
            "storage event",
            extra={"bucket": record.bucket, "key": record.key, "action": record.action, "size": record.size},
        )
        keys.append(record.key)
    return {"keys": keys}


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------
def on_order(event: Event, ctx: Context) -> Dict[str, Any]:
    for record in event.records:
        ctx.logger.info("topic message", extra={"id": record.id, "body": record.json()})
    return {"received": len(event.records)}


# ---------------------------------------------------------------------------
# Workflow steps (event.type == "workflow", input in event.data)
# ---------------------------------------------------------------------------
def validate_step(event: Event, ctx: Context) -> Dict[str, Any]:
    data = dict(event.data or {})
    amount = data.get("amount", 0)
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("amount must be a positive number")
    data["valid"] = True
    ctx.logger.info("validated", extra=data)
    return data


def process_step(event: Event, ctx: Context) -> Dict[str, Any]:
    data = dict(event.data or {})
    data["processed"] = True
    data["status"] = "processed"
    ctx.logger.info("processed", extra=data)
    return data


def notify_step(event: Event, ctx: Context) -> Dict[str, Any]:
    data = dict(event.data or {})
    data["notified"] = True
    ctx.logger.info("notified", extra=data)
    return data

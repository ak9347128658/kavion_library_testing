"""HTTP handlers. This code runs unchanged on every supported cloud."""

import base64
import os
import tempfile
from pathlib import Path

from faker import Faker
from py_serverless_kit import Context, Event, NotFound, Response
from py_serverless_kit import BatchResult

_fake = Faker()
_fake.seed_instance(42)


def _random_items(count: int = 5) -> dict:
    """Build a small catalog with Faker so item data is not hardcoded."""
    items = {}
    for number in range(1, count + 1):
        item_id = str(number)
        items[item_id] = {
            "id": item_id,
            "name": _fake.catch_phrase(),
            "category": _fake.word(),
            "price": round(_fake.pyfloat(min_value=1, max_value=100, right_digits=2), 2),
        }
    return items


_ITEMS = _random_items()


def hello(event: Event, ctx: Context):
    name = event.http.query.get("name", "world")
    ctx.logger.info("saying hello", extra={"name": name})
    return {"message": f"Hello, {name}!", "provider": event.provider, "stage": ctx.stage}


def get_item(event: Event, ctx: Context):
    item = _ITEMS.get(event.http.path_params["id"])
    if item is None:
        raise NotFound(f"item {event.http.path_params['id']} does not exist")
    return item


def create_item(event: Event, ctx: Context):
    body = event.http.json()
    item = {"id": str(len(_ITEMS) + 1), **body}
    _ITEMS[item["id"]] = item
    return Response.json(item, status=201)


def s3_fun_test(event: Event, ctx: Context):
    """Storage trigger: one record per created / deleted object."""
    for record in event.records:
        ctx.logger.info("object", extra={"bucket": record.bucket, "key": record.key, "action": record.action})


def sqs_test(event: Event, ctx: Context):
    """Storage trigger: one record per created / deleted object."""
    for record in event.records:
        ctx.logger.info("object", extra={"bucket": record.bucket, "key": record.key, "action": record.action})


def sqs_fun_test(event: Event, ctx: Context) -> BatchResult:
    """Queue consumer: failed records are retried, then dead-lettered."""
    result = BatchResult()
    for record in event.records:
        try:
            ctx.logger.info("message", extra={"id": record.id, "body": record.text()})
        except Exception:  # noqa: BLE001 - retry only this record
            result.fail(record)
    return result


def queue_test_fun(event: Event, ctx: Context) -> BatchResult:
    """Queue consumer: failed records are retried, then dead-lettered."""
    result = BatchResult()
    for record in event.records:
        try:
            ctx.logger.info("message", extra={"id": record.id, "body": record.text()})
        except Exception:  # noqa: BLE001 - retry only this record
            result.fail(record)
    return result


def mail_funtion(event: Event, ctx: Context):
    """Called with invoke("<name>", data) or from a workflow: event.data is the payload."""
    return {"ok": True, "input": event.data}


def fn_mail_test(event: Event, ctx: Context):
    """Called with invoke("<name>", data) or from a workflow: event.data is the payload."""
    return {"ok": True, "input": event.data}


def ses_fun_test(event: Event, ctx: Context):
    """SMTP trigger: saves each attachment to disk and logs the mail and the file paths."""
    mail = event.data
    # MAIL_ATTACHMENTS_DIR (environment) or the system temp folder; one folder per mail.
    folder = Path(os.environ.get("MAIL_ATTACHMENTS_DIR") or Path(tempfile.gettempdir()) / "pskit-mail") / mail["id"]
    folder.mkdir(parents=True, exist_ok=True)
    files = []
    for i, att in enumerate(mail["attachments"]):
        # The name comes from the sender: keep only the file name, never a path.
        name = Path(att["filename"] or f"attachment-{i}").name or f"attachment-{i}"
        path = folder / name
        path.write_bytes(base64.b64decode(att["content"]))
        files.append({"filename": name, "path": str(path), "content_type": att["content_type"], "size": att["size"]})
        ctx.logger.info("attachment saved", extra={"path": str(path), "content_type": att["content_type"],
                                                   "size": att["size"]})
    ctx.logger.info("mail received", extra={"from": mail["from"], "to": mail["to"], "subject": mail["subject"],
                                            "files": [f["path"] for f in files]})
    # Return a summary, not event.data: the attachments' base64 content would fill the logs and the result.
    return {"ok": True, "from": mail["from"], "to": mail["to"], "subject": mail["subject"],
            "text": mail["text"], "files": files}

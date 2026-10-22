"""HTTP handlers. This code runs unchanged on every supported cloud."""

from py_serverless_kit import Context, Event, NotFound, Response
from py_serverless_kit import BatchResult

_ITEMS = {"1": {"id": "1", "name": "first item"}}


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


def sqs_test(event: Event, ctx: Context) -> BatchResult:
    """Queue consumer: failed records are retried, then dead-lettered."""
    result = BatchResult()
    for record in event.records:
        try:
            ctx.logger.info("message", extra={"id": record.id, "body": record.text()})
        except Exception:  # noqa: BLE001 - retry only this record
            result.fail(record)
    return result


def schdule_test(event: Event, ctx: Context):
    """Scheduled job: event.data is the schedule's `input`."""
    ctx.logger.info("tick", extra={"input": event.data})


def fun_step01(event: Event, ctx: Context):
    """Called with invoke("<name>", data) or from a workflow: event.data is the payload."""
    return {"ok": True, "input": event.data}


def fun_step02(event: Event, ctx: Context):
    """Called with invoke("<name>", data) or from a workflow: event.data is the payload."""
    return {"ok": True, "input": event.data}

"""HTTP handlers. This code runs unchanged on every supported cloud."""

from py_serverless_kit import Context, Event, NotFound, Response

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

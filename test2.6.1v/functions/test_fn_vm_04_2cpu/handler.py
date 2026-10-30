"""Handlers created with pskit studio. This code runs unchanged on every supported cloud."""

from py_serverless_kit import Context, Event


def main(event: Event, ctx: Context):
    """HTTP handler: event.http has method, path, query, path_params, headers and json().

    Also called from a workflow step or invoke(): then event.http is None and event.data is the input."""
    if event.http is None:
        return {"message": "Hello, world!", "input": event.data}
    name = event.http.query.get("name", "world")
    return {"message": f"Hello, {name}!"}

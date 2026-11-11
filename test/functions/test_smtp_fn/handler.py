"""Handlers created with pskit studio. This code runs unchanged on every supported cloud."""

from py_serverless_kit import Context, Event


def main(event: Event, ctx: Context):
    """Called with invoke("<name>", data) or from a workflow: event.data is the payload."""
    return {"ok": True, "input": event.data}

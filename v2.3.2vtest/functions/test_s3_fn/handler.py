"""Handlers created with pskit studio. This code runs unchanged on every supported cloud."""

from py_serverless_kit import Context, Event


def main(event: Event, ctx: Context):
    """Storage trigger: one record per created / deleted object."""
    for record in event.records:
        ctx.logger.info("object", extra={"bucket": record.bucket, "key": record.key, "action": record.action})

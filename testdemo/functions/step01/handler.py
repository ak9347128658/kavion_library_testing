"""Handlers created with pskit studio. This code runs unchanged on every supported cloud."""

from py_serverless_kit import BatchResult, Context, Event


def main(event: Event, ctx: Context) -> BatchResult:
    """Queue consumer: failed records are retried, then dead-lettered."""
    result = BatchResult()
    for record in event.records:
        try:
            ctx.logger.info("message", extra={"id": record.id, "body": record.text()})
        except Exception:  # noqa: BLE001 - retry only this record
            result.fail(record)
    return result

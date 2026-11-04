"""HTTP handlers. This code runs unchanged on every supported cloud."""

from py_serverless_kit import Context, Event, NotFound, Response

_ITEMS = {"1": {"id": "1", "name": "first item"}}


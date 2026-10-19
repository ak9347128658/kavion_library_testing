"""On-premises handlers demonstrating GET/POST APIs, invoke, and workflows.

These handlers are cloud-agnostic and work the same on AWS, GCP, Azure, or on-prem.
"""

from __future__ import annotations

from typing import Any, Dict

from py_serverless_kit import (
    BadRequest,
    Conflict,
    Context,
    Event,
    NotFound,
    Response,
    invoke,
)


# Simple in-memory store for the demo (replace with a real DB in production)
ITEMS: Dict[str, Dict[str, Any]] = {
    "1": {"id": "1", "name": "Widget", "price": 9.99},
    "2": {"id": "2", "name": "Gadget", "price": 19.99},
}


# ---------------------------------------------------------------------------
# GET APIs
# ---------------------------------------------------------------------------

def list_items(event: Event, ctx: Context):
    """GET /items — list all items, optional ?limit= and ?name= filter."""
    limit = int(event.http.query.get("limit", "100"))
    name_filter = event.http.query.get("name")
    items = list(ITEMS.values())
    if name_filter:
        items = [i for i in items if name_filter.lower() in i["name"].lower()]
    return {"items": items[:limit], "count": len(items[:limit])}


def get_item(event: Event, ctx: Context):
    """GET /items/{id} — fetch a single item."""
    item_id = event.http.path_params["id"]
    item = ITEMS.get(item_id)
    if item is None:
        raise NotFound(f"item {item_id} not found")
    return item


# ---------------------------------------------------------------------------
# POST APIs
# ---------------------------------------------------------------------------

def create_item(event: Event, ctx: Context):
    """POST /items — create a new item from JSON body."""
    body = event.http.json()
    if not isinstance(body, dict):
        raise BadRequest("JSON object required")
    name = body.get("name")
    price = body.get("price")
    if not name or price is None:
        raise BadRequest("`name` and `price` are required")
    if any(i["name"].lower() == name.lower() for i in ITEMS.values()):
        raise Conflict(f"item named '{name}' already exists")
    item_id = str(max((int(k) for k in ITEMS), default=0) + 1)
    item = {"id": item_id, "name": name, "price": float(price)}
    ITEMS[item_id] = item
    return Response.json(item, status=201, headers={"Location": f"/items/{item_id}"})


def process_order(event: Event, ctx: Context):
    """POST /orders — accept an order and invoke an internal pricing function."""
    body = event.http.json()
    if not isinstance(body, dict) or "items" not in body:
        raise BadRequest("`items` array is required")
    # Synchronous invoke of the pricing function
    priced = invoke("price-calculator", {"items": body["items"], "country": body.get("country", "US")})
    return {
        "order_id": ctx.request_id,
        "priced": priced,
        "status": "accepted",
    }


# ---------------------------------------------------------------------------
# Invoke-only function (no HTTP events)
# ---------------------------------------------------------------------------

def price_calculator(event: Event, ctx: Context):
    """Internal function called via invoke(). Receives event.data as the payload."""
    data = event.data or {}
    items = data.get("items", [])
    country = data.get("country", "US")
    subtotal = sum(float(i.get("unit_price", 0)) * int(i.get("qty", 1)) for i in items)
    tax_rate = {"US": 0.08, "DE": 0.19, "IN": 0.18}.get(country, 0.0)
    tax = round(subtotal * tax_rate, 2)
    return {
        "subtotal": subtotal,
        "tax": tax,
        "total": round(subtotal + tax, 2),
        "tax_rate": tax_rate,
        "country": country,
    }


# ---------------------------------------------------------------------------
# Workflow task functions (used by the three step functions)
# ---------------------------------------------------------------------------

def validate_order(event: Event, ctx: Context):
    data = event.data or {}
    if not data.get("customer_id"):
        raise ValueError("customer_id is required")
    if not data.get("items"):
        raise ValueError("items are required")
    data["validated"] = True
    return data


def reserve_stock(event: Event, ctx: Context):
    data = event.data or {}
    data["reserved"] = True
    data["reservation_id"] = f"res-{ctx.request_id[:8]}"
    return data


def charge_payment(event: Event, ctx: Context):
    data = event.data or {}
    # Simulate a possible transient error for retry demo
    if data.get("simulate_timeout"):
        raise TimeoutError("payment gateway timeout")
    data["charged"] = True
    data["charge_id"] = f"ch-{ctx.request_id[:8]}"
    return data


def send_confirmation(event: Event, ctx: Context):
    data = event.data or {}
    data["confirmation_sent"] = True
    return data


def create_shipment(event: Event, ctx: Context):
    data = event.data or {}
    data["shipment_id"] = f"shp-{ctx.request_id[:8]}"
    data["shipped"] = True
    return data


def notify_support(event: Event, ctx: Context):
    data = event.data or {}
    data["support_notified"] = True
    return data

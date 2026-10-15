from py_serverless_kit import Event, Context, NotFound, BadRequest, Response
# In-memory store for demo (use DynamoDB/etc. in production)
ITEMS = {}

def list_items(event: Event, ctx: Context):
    return {"items": list(ITEMS.values())}

def get_item(event: Event, ctx: Context):
    item_id = event.http.path_params["id"]
    item = ITEMS.get(item_id)
    if not item:
        raise NotFound(f"item {item_id} not found")
    return item

def create_item(event: Event, ctx: Context):
    body = event.http.json()  # auto 400 on bad JSON
    if not isinstance(body, dict) or "name" not in body:
        raise BadRequest("name is required")
    item_id = body.get("id") or str(len(ITEMS) + 1)
    ITEMS[item_id] = {"id": item_id, **body}
    return Response.json(ITEMS[item_id], status=201, headers={"location": f"/items/{item_id}"})

def update_item(event: Event, ctx: Context):
    item_id = event.http.path_params["id"]
    if item_id not in ITEMS:
        raise NotFound(f"item {item_id} not found")
    body = event.http.json()
    ITEMS[item_id].update(body)
    return ITEMS[item_id]

def get_arn(event: Event, ctx: Context):
    """
    Invoke-only function (not an HTTP API).
    On AWS it returns the real Lambda ARN.
    On other clouds it returns the resource id / name that pskit assigned.
    """
    # Portable info always available
    info = {
        "function": ctx.function,
        "service": ctx.service,
        "stage": ctx.stage,
        "region": ctx.region,
        "provider": ctx.provider,
        "request_id": ctx.request_id,
    }

    # AWS-specific ARN (native Lambda context)
    arn = None
    if ctx.provider == "aws" and ctx.raw is not None:
        arn = getattr(ctx.raw, "invoked_function_arn", None)

    # Fallback: construct the usual AWS-style name if needed
    if not arn:
        # pskit names functions: <service>-<stage>-<function>
        arn = f"arn:aws:lambda:{ctx.region}:ACCOUNT:function:{ctx.service}-{ctx.stage}-{ctx.function}"

    return {
        "arn": arn,
        **info,
        "message": "This function has no HTTP endpoint — call it with pskit invoke or lambda invoke",
    }
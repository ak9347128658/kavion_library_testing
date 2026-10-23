import json

from py_serverless_kit.local import LocalRunner, http_event
from py_serverless_kit.core.project import Project


def test_hello():
    runner = LocalRunner(Project.load())
    resp = runner.invoke("hello", http_event("GET", "/hello?name=test"))
    assert resp.status == 200


def test_get_item_uses_faker_catalog():
    runner = LocalRunner(Project.load())
    resp = runner.invoke("get-item", http_event("GET", "/items/1"))
    assert resp.status == 200
    body = json.loads(resp.body)
    assert body["id"] == "1"
    assert body["name"]
    assert body["category"]
    assert isinstance(body["price"], (int, float))

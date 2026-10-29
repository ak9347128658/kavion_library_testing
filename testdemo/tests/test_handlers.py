from py_serverless_kit.local import LocalRunner, http_event
from py_serverless_kit.core.project import Project


def test_hello():
    runner = LocalRunner(Project.load())
    resp = runner.invoke("hello", http_event("GET", "/hello?name=test"))
    assert resp.status == 200

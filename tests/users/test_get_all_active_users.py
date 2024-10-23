import jsonschema
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_active_users(users_schema):
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()["response"]
    jsonschema.validate(instance=data, schema=users_schema)

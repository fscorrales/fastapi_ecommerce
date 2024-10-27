import jsonschema
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_active_users(public_stored_user_schema):
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()["response"]
    jsonschema.validate(instance=data, schema=public_stored_user_schema)

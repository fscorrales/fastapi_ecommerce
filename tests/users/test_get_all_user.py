import jsonschema
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_users(login_as_admin, users_schema):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/users/include_deleted", headers=headers)
    assert response.status_code == 200
    jsonschema.validate(instance=response.json(), schema=users_schema)


def test_get_all_users_without_auth():
    response = client.get("/api/users/include_deleted")
    assert response.status_code == 401

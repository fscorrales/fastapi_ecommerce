from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_deleted_users(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/users/deleted", headers=headers)
    assert response.status_code == 200


def test_get_all_deleted_users_without_auth():
    response = client.get("/api/users/deleted")
    assert response.status_code == 401

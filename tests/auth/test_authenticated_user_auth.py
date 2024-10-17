from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_authenticated_user_without_credentials():
    response = client.get("/auth/authenticated_user/")
    assert response.status_code == 401


def test_authenticated_user(login_as_admin, dict_test_user):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/authenticated_user/", headers=headers)
    assert response.status_code == 200
    keys = ["username", "email", "role"]
    dict_test_user = {key: dict_test_user[key] for key in keys}
    dict_test_user["id"] = login_as_admin.get("user_id")
    dict_test_user["role"] = "admin"
    assert response.json() == dict_test_user

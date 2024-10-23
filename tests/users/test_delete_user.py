from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_delete_user(login_as_admin, create_and_delete_customer):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = create_and_delete_customer
    response = client.delete(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json().get("deactivated_at") != None


def test_delete_user_with_incorrect_auth(login_as_customer, create_and_delete_admin):
    access_token = login_as_customer.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = create_and_delete_admin
    response = client.delete(f"/api/users/{user_id}", headers=headers)
    assert response.status_code != 200


def test_delete_user_without_auth(create_and_delete_customer):
    user_id = create_and_delete_customer
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 401


def test_delete_user_with_invalid_id(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = "12345"
    response = client.delete(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 422

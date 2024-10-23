from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_deleted_products(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/products/deleted", headers=headers)
    assert response.status_code == 200


def test_get_all_deleted_products_without_auth():
    response = client.get("/api/products/deleted")
    assert response.status_code == 401


def test_get_all_deleted_products_with_incorrect_auth(login_as_customer):
    access_token = login_as_customer.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/products/deleted", headers=headers)
    assert response.status_code == 401

import jsonschema
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_products(login_as_admin, create_product_schema):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/products/include_deleted", headers=headers)
    assert response.status_code == 200
    data = response.json()["response"]
    jsonschema.validate(instance=data, schema=create_product_schema)


def test_get_all_products_without_auth():
    response = client.get("/api/products/include_deleted")
    assert response.status_code == 401


def test_get_all_products_with_incorrect_auth(login_as_customer):
    access_token = login_as_customer.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/products/include_deleted", headers=headers)
    assert response.status_code == 401

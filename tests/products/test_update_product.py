import pytest
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_update_product_without_credentials(create_and_delete_product):
    product_id = create_and_delete_product
    response = client.put(f"/api/products/{product_id}")
    assert response.status_code == 401


def test_update_product_with_invalid_id(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    product_id = "12345"
    response = client.put(f"/api/products/{product_id}", headers=headers)
    assert response.status_code == 422


def test_update_product_without_body(login_as_admin, create_and_delete_product):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    product_id = create_and_delete_product
    response = client.put(f"/api/products/{product_id}", headers=headers)
    assert response.status_code == 422


def test_update_product(
    login_as_admin,
    create_and_delete_product,
    dict_test_product,
    test_valid_product_fields,
):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    product_id = create_and_delete_product
    response = client.put(
        f"/api/products/{product_id}", headers=headers, json=test_valid_product_fields
    )
    assert response.status_code == 200
    dict_test_product["id"] = str(product_id)
    dict_test_product.update(test_valid_product_fields)
    dict_test_product = {k: v for k, v in dict_test_product.items() if v is not None}
    dict_test_product["deactivated_at"] = None
    assert response.json() == dict_test_product


def test_update_product_with_invalid_fields(
    login_as_admin, create_and_delete_product, test_invalid_product_fields
):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    product_id = create_and_delete_product
    response = client.put(
        f"/api/products/{product_id}", headers=headers, json=test_invalid_product_fields
    )
    assert response.status_code == 422

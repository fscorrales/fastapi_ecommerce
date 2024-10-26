import pytest

from bson import ObjectId
from fastapi.testclient import TestClient

from ...src.main import app
from ...src.api.services import ProductsServiceDependency

client = TestClient(app)


def test_create_product(login_as_seller, dict_test_product):
    access_token = login_as_seller.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    dict_test_product["seller_id"] = login_as_seller.get("user_id")
    response = client.post("/api/products/", json=dict_test_product, headers=headers)
    assert response.status_code == 200
    if product_id := response.json().get("id"):
        ProductsServiceDependency().delete_one_hard(id=ObjectId(product_id))


def test_create_product_without_body(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/products/", json={}, headers=headers)
    assert response.status_code == 422


def test_create_product_without_auth():
    response = client.post("/api/products/", json={})
    assert response.status_code == 401


def test_create_product_with_incorrect_auth(login_as_customer, dict_test_product):
    access_token = login_as_customer.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    dict_test_product["seller_id"] = login_as_customer.get("user_id")
    response = client.post("/api/products/", json=dict_test_product, headers=headers)
    assert response.status_code == 401
    if product_id := response.json().get("id"):
        ProductsServiceDependency().delete_one_hard(id=ObjectId(product_id))


def test_create_product_with_invalid_fields(
    login_as_seller, test_invalid_product_fields
):
    access_token = login_as_seller.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    test_invalid_product_fields["seller_id"] = login_as_seller.get("user_id")
    response = client.post(
        "/api/products/", json=test_invalid_product_fields, headers=headers
    )
    if product_id := response.json().get("id"):
        ProductsServiceDependency().delete_one_hard(id=ObjectId(product_id))
    assert response.status_code != 200

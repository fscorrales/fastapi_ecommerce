from bson import ObjectId
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_one_product(create_and_delete_product, dict_test_product):
    product_id = create_and_delete_product
    response = client.get(f"/api/products/{product_id}")
    print(response.json())
    assert response.status_code == 200
    created_product = dict_test_product
    created_product["id"] = str(product_id)
    created_product["deactivated_at"] = None
    assert response.json() == created_product


def test_get_one_product_with_invalid_id():
    product_id = "12345"
    response = client.get(f"/api/products/{product_id}")
    print(response.json())
    assert response.status_code == 422


def test_get_one_product_with_nonexitent_id():
    product_id = ObjectId()
    response = client.get(f"/api/products/{product_id}")
    print(response.json())
    assert response.status_code == 404

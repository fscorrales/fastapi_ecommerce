from fastapi.testclient import TestClient

from ...src.main import app

from bson import ObjectId

client = TestClient(app)


def test_delete_product(login_as_admin, create_and_delete_product):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    product_id = create_and_delete_product
    response = client.delete(f"/api/products/{product_id}", headers=headers)
    assert response.status_code == 200
    assert response.json().get("deactivated_at") != None


def test_delete_product_without_credentials(create_and_delete_product):
    product_id = create_and_delete_product
    response = client.delete(f"/api/products/{product_id}")
    assert response.status_code == 401


# def test_delete_product_with_incorrect_auth(
#     login_as_customer, create_and_delete_product
# ):
#     access_token = login_as_customer.get("access_token")
#     headers = {"Authorization": f"Bearer {access_token}"}
#     product_id = create_and_delete_product
#     response = client.delete(f"/api/products/{product_id}", headers=headers)
#     assert response.status_code == 401


def test_delete_product_with_invalid_id(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    produt_id = "12345"
    response = client.delete(f"/api/products/{produt_id}", headers=headers)
    assert response.status_code == 422


def test_delete_product_with_nonexitent_id(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    product_id = ObjectId()
    response = client.delete(f"/api/products/{product_id}", headers=headers)
    print(response.json())
    assert response.status_code == 404

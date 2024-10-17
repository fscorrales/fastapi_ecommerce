from bson import ObjectId
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_one_user(create_and_delete_customer):
    user_id = create_and_delete_customer
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200


def test_get_one_user_with_invalid_id():
    user_id = "12345"
    response = client.get(f"/api/users/{user_id}")
    print(response.json())
    assert response.status_code == 422


def test_get_one_user_with_nonexitent_id():
    user_id = ObjectId()
    response = client.get(f"/api/users/{user_id}")
    print(response.json())
    assert response.status_code == 404

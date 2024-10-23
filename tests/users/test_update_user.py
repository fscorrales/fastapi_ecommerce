import pytest
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "updated_fields",
    [
        {"username": "UpdatedTest"},
        {"email": "UpdatedTest@test.com"},
        {"image": "https://picsum.photos/200/300?random=1"},
        {"username": "UpdatedTest", "email": "UpdatedTest@test.com"},
        {
            "username": "UpdatedTest",
            "email": "UpdatedTest@test.com",
            "image": "https://picsum.photos/200/300?random=1",
        },
        {"username": "UpdatedTest", "image": None},
        {"email": "UpdatedTest@test.com", "image": None},
    ],
)
def test_update_user(
    login_as_admin, create_and_delete_customer, dict_test_user_two, updated_fields
):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = create_and_delete_customer
    response = client.put(f"/api/users/{user_id}", headers=headers, json=updated_fields)
    assert response.status_code == 200
    dict_test_user_two.pop("password")
    dict_test_user_two["id"] = str(user_id)
    dict_test_user_two.update(updated_fields)
    dict_test_user_two = {k: v for k, v in dict_test_user_two.items() if v is not None}
    assert response.json() == dict_test_user_two


def test_update_user_with_incorrect_auth(
    login_as_customer, create_and_delete_admin, dict_test_user
):
    access_token = login_as_customer.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = create_and_delete_admin
    response = client.put(f"/api/users/{user_id}", headers=headers, json=dict_test_user)
    assert response.status_code != 200


def test_update_user_without_auth(create_and_delete_customer):
    user_id = create_and_delete_customer
    response = client.put(f"/api/users/{user_id}")
    assert response.status_code == 401


def test_update_user_with_invalid_id(login_as_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = "12345"
    response = client.put(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 422


def test_update_user_without_body(login_as_admin, create_and_delete_customer):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = create_and_delete_customer
    response = client.put(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "updated_fields",
    [
        {"username": 1223},
        {"username": None},
        {"username": ""},
        {"username": True},
        {"username": ["a", "b", "c"]},
        {"username": {"nombre": "Juan"}},
        {"email": None},
        {"username": "UpdatedTest", "email": None},
    ],
)  # Falta el campo image
def test_update_user_with_invalid_fields(
    login_as_admin, create_and_delete_customer, updated_fields
):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = create_and_delete_customer
    response = client.put(f"/api/users/{user_id}", headers=headers, json=updated_fields)
    assert response.status_code == 422

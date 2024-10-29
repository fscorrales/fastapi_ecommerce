import pytest

from bson import ObjectId
from fastapi.testclient import TestClient

from ...src.main import app
from ...src.api.services import UsersServiceDependency

client = TestClient(app)


def test_create_user(login_as_admin, dict_test_seller):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/users/", json=dict_test_seller, headers=headers)
    assert response.status_code == 200
    if user_id := response.json().get("id"):
        UsersServiceDependency().delete_one_hard(id=ObjectId(user_id))


def test_create_user_without_auth():
    response = client.post("/api/users/", json={})
    assert response.status_code == 401


def test_create_user_without_body(login_as_admin, dict_test_admin):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/users/", json={}, headers=headers)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "test_fields",
    [
        {
            "username": "",
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "admin",
        },
        {
            "username": 12345,
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "admin",
        },
        {
            "username": None,
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "admin",
        },
        {
            "username": ["a", "b", "c"],
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "admin",
        },
        {
            "username": {"nombre": "Juan"},
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "admin",
        },
        {
            "username": "AnotherTest",
            "email": "",
            "password": "12345",
            "role": "admin",
        },
        {
            "username": "AnotherTest",
            "email": "anothertest@anothertest.com",
            "password": "",
            "role": "admin",
        },
        {
            "username": "AnotherTest",
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "cualquiera",
        },
        {
            "username": "AnotherTest",
            "email": "anothertest@anothertest.com",
            "password": "12345",
            "role": "",
        },
        {
            "username": "AnotherTest",
            "email": "hola",
            "password": "12345",
            "role": "admin",
        },
    ],
)
def test_create_user_with_invalid_fields(login_as_admin, test_fields):
    access_token = login_as_admin.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/users/", json=test_fields, headers=headers)
    assert response.status_code != 200

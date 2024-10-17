import pytest
from fastapi.testclient import TestClient
from fastapi import Form

from typing import Annotated

from ...src.main import app
from ...src.api.models import LoginUser


client = TestClient(app)


def test_login_auth_without_body():
    response = client.post("/auth/login/", json={})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "test_fields",
    [
        {"username": 1223},
        {"username": None},
        {"username": ""},
        {"username": True},
        {"username": ["a", "b", "c"]},
        {"username": {"nombre": "Juan"}},
        {"password": 1223},
        {"password": None},
        {"password": ""},
        {"password": True},
        {"password": ["a", "b", "c"]},
        {"password": {"nombre": "Juan"}},
        {"username": "UpdatedTest", "password": None},
    ],
)
def test_login_auth_with_invalid_fields(create_and_delete_admin, test_fields):
    response = client.post("/auth/login/", data=test_fields)
    assert response.status_code != 200


def test_login_auth_with_valid_fields(create_and_delete_admin, dict_test_user):
    response = client.post("/auth/login/", data=dict_test_user)
    assert response.status_code == 200

# https://fastapi.tiangolo.com/tutorial/testing/
import pytest
from bson import ObjectId
from fastapi import Response

from ..src.api.models.users import CreateUser, LoginUser
from ..src.api.services import (
    UsersServiceDependency,
    Authentication,
    AuthenticationDependency,
)


@pytest.fixture
def dict_test_user() -> dict:
    return {
        "username": "Test",
        "email": "test@test.com",
        "role": "admin",
        "password": "12345",
    }


@pytest.fixture
def dict_test_user_two() -> dict:
    return {
        "username": "TestTwo",
        "email": "testtwo@testtwo.com",
        "role": "seller",
        "password": "12345",
    }


@pytest.fixture
def create_and_delete_admin(dict_test_user):
    user = CreateUser(**dict_test_user)
    user_id = UsersServiceDependency().create_one(user=user).model_dump()["id"]
    yield user_id
    UsersServiceDependency().delete_one_hard(id=ObjectId(user_id))


@pytest.fixture
def login_as_admin(create_and_delete_admin, dict_test_user):
    user_id = create_and_delete_admin
    user = LoginUser(**dict_test_user)
    access_token = Authentication().login_and_set_access_token(
        db_user=UsersServiceDependency().get_one(
            username=user.username, with_password=True
        ),
        user=user,
        response=Response(),
    )
    access_token = access_token.get("access_token")
    return {"access_token": access_token, "user_id": user_id}


@pytest.fixture
def login_as_customer(create_and_delete_customer, dict_test_user_two):
    user_id = create_and_delete_customer
    user = LoginUser(**dict_test_user_two)
    access_token = Authentication().login_and_set_access_token(
        db_user=UsersServiceDependency().get_one(
            username=user.username, with_password=True
        ),
        user=user,
        response=Response(),
    )
    access_token = access_token.get("access_token")
    return {"access_token": access_token, "user_id": user_id}


@pytest.fixture
def login_as_seller(create_and_delete_seller, dict_test_user_two):
    user_id = create_and_delete_seller
    user = LoginUser(**dict_test_user_two)
    access_token = Authentication().login_and_set_access_token(
        db_user=UsersServiceDependency().get_one(
            username=user.username, with_password=True
        ),
        user=user,
        response=Response(),
    )
    access_token = access_token.get("access_token")
    return {"access_token": access_token, "user_id": user_id}


@pytest.fixture
def create_and_delete_customer(dict_test_user_two):
    dict_test_user_two["role"] = "customer"
    user = CreateUser(**dict_test_user_two)
    user_id = UsersServiceDependency().create_one(user=user).model_dump()["id"]
    yield user_id
    UsersServiceDependency().delete_one_hard(id=ObjectId(user_id))


@pytest.fixture
def create_and_delete_seller(dict_test_user_two):
    dict_test_user_two["role"] = "seller"
    user = CreateUser(**dict_test_user_two)
    user_id = UsersServiceDependency().create_one(user=user).model_dump()["id"]
    yield user_id
    UsersServiceDependency().delete_one_hard(id=ObjectId(user_id))

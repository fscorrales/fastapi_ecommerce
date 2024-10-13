__all__ = [
    "BaseUser",
    "LoginUser",
    "PublicStoredUser",
    "PrivateStoredUser",
    "RegisterUser",
    "CreateUser",
    "UpdateUser",
]

from datetime import datetime
from enum import Enum

from pydantic import AliasChoices, BaseModel, Field, field_validator
from pydantic_mongo import PydanticObjectId
from ..utils import validate_not_empty


class RegisterRole(str, Enum):
    customer = "customer"
    seller = "seller"


class Role(str, Enum):
    admin = "admin"
    customer = "customer"
    seller = "seller"


class BaseUser(BaseModel):
    username: str
    email: str
    image: str | None = None


class UpdateUser(BaseUser):
    username: str | None = None
    email: str | None = None
    image: str | None = None

    @field_validator("username", "email", mode="after")
    @classmethod
    def not_empty(cls, field: str) -> str:
        return validate_not_empty(field)


class RegisterUser(BaseUser):
    role: RegisterRole = RegisterRole.customer
    password: str


class CreateUser(RegisterUser):
    role: Role = Role.customer

    @field_validator("username", "email", "password", mode="after")
    @classmethod
    def not_empty(cls, field: str) -> str:
        return validate_not_empty(field)


class LoginUser(BaseModel):
    username: str
    password: str


class PublicStoredUser(BaseUser):
    role: Role
    deactivated_at: datetime | None = Field(default=None)
    id: PydanticObjectId = Field(validation_alias=AliasChoices("_id", "id"))


class PrivateStoredUser(BaseUser):
    role: Role
    id: PydanticObjectId = Field(alias="_id")
    deactivated_at: datetime | None = Field(default=None)
    hash_password: str

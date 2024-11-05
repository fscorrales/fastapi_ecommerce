__all__ = [
    "BaseUser",
    "LoginUser",
    "PublicStoredUser",
    "PrivateStoredUser",
    "RegisterUser",
    "CreateUser",
    "UpdateUser",
    "FilterParamsUser",
]

from datetime import datetime
from enum import Enum
from typing import Optional, Literal

from pymongo.collection import Collection
from pydantic import AliasChoices, BaseModel, Field, field_validator, EmailStr
from pydantic_mongo import PydanticObjectId
from ..utils import validate_not_empty, convert_url_to_string, data_filter
from ..config import logger


class RegisterRole(str, Enum):
    customer = "customer"
    seller = "seller"


class Role(str, Enum):
    admin = "admin"
    customer = "customer"
    seller = "seller"


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    image: str | None = None


class UpdateUser(BaseUser):
    username: str | None = None
    email: EmailStr | None = None
    image: str | None = None
    _not_empty = field_validator("username", "email", mode="after")(validate_not_empty)


class RegisterUser(BaseUser):
    role: RegisterRole = RegisterRole.customer
    password: str
    _not_empty = field_validator("username", "email", "password", mode="after")(
        validate_not_empty
    )


class CreateUser(RegisterUser):
    role: Role = Role.customer
    _not_empty = field_validator("username", "email", "password", mode="after")(
        validate_not_empty
    )


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


class FilterParamsUser(BaseModel):
    query_filter: str = ""
    limit: int = Field(100, gt=0)
    offset: int = Field(0, ge=0)
    sort_by: Literal["id", "username", "email"] = "id"
    sort_dir: Literal["asc", "desc"] = "asc"
    role: Role | None = None

    def query_collection(
        self, collection: Collection, get_deleted: Optional[bool] = None
    ):

        extra_filter = {"role": {"$eq": self.role.value}} if self.role else None

        return (
            collection.find(data_filter(self.query_filter, get_deleted, extra_filter))
            .skip(self.offset)
            .limit(self.limit)
            .sort(self.sort_by, 1 if self.sort_dir == "asc" else -1)
        )

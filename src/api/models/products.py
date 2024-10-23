__all__ = ["Product", "StoredProduct", "UpdateProduct", "Type"]

from pydantic import BaseModel, Field, AliasChoices, field_validator
from datetime import datetime
from pydantic_mongo import PydanticObjectId
from enum import Enum
from ..utils import (
    validate_not_empty,
    validate_greater_than_zero,
    validate_positive_number,
)


class Type(str, Enum):
    percussion = "Percussion"
    wind = "Wind"
    string = "String"
    keyboard = "Keyboard"
    electronic = "Electronic"


class Product(BaseModel):
    name: str
    price: float
    quantity: int
    description: str | None = None
    image: str | None = None
    type: Type
    seller_id: PydanticObjectId
    _not_empty = field_validator("name", "price", "quantity", mode="after")(
        validate_not_empty
    )
    _greater_than_zero = field_validator("price", mode="after")(
        validate_greater_than_zero
    )
    _positive_number = field_validator("quantity", mode="after")(
        validate_positive_number
    )

    # @classmethod
    # def not_empty(cls, field: str) -> str:
    #     return validate_not_empty(field)


class UpdateProduct(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None
    image: str | None = None


class StoredProduct(Product):
    id: PydanticObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    deactivated_at: datetime | None = Field(default=None)

__all__ = [
    "CreateProduct",
    "StoredProduct",
    "UpdateProduct",
    "FilterParamsProduct",
]

from typing import Literal
from pydantic import (
    BaseModel,
    Field,
    AliasChoices,
    field_validator,
    PositiveFloat,
    NonNegativeInt,
)
from datetime import datetime
from pydantic_mongo import PydanticObjectId
from pymongo.collection import Collection
from enum import Enum
from ..utils import validate_not_empty


class Type(str, Enum):
    percussion = "Percussion"
    wind = "Wind"
    string = "String"
    keyboard = "Keyboard"
    electronic = "Electronic"


class CreateProduct(BaseModel):
    name: str
    price: PositiveFloat
    quantity: NonNegativeInt
    description: str | None = None
    image: str | None = None
    type: Type
    seller_id: PydanticObjectId
    _not_empty = field_validator("name", "price", "quantity", mode="after")(
        validate_not_empty
    )


class UpdateProduct(BaseModel):
    name: str | None = None
    price: PositiveFloat | None = None
    quantity: NonNegativeInt | None = None
    description: str | None = None
    image: str | None = None
    type: Type | None = None
    _not_empty = field_validator("name", "price", "quantity", mode="after")(
        validate_not_empty
    )


class StoredProduct(CreateProduct):
    id: PydanticObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    deactivated_at: datetime | None = Field(default=None)


class FilterParamsProduct(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    sort_by: Literal["price", "name"] = "price"
    sort_dir: Literal["asc", "desc"] = "asc"
    tags: list[str] = []

    @classmethod
    def query_collection(cls, collection: Collection):
        return (
            collection.find({})
            # .skip(cls.offset)
            # .limit(cls.limit)
            # .sort(cls.sort_by, 1 if cls.sort_dir == "asc" else -1)
        )

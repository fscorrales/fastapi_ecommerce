__all__ = [
    "CreateProduct",
    "StoredProduct",
    "UpdateProduct",
    "FilterParamsProduct",
]

from typing import Literal, Optional
from pydantic import (
    BaseModel,
    Field,
    AliasChoices,
    field_validator,
    PositiveFloat,
    NonNegativeInt,
)
from datetime import datetime
from pydantic import HttpUrl
from pydantic_mongo import PydanticObjectId
from pymongo.collection import Collection
from enum import Enum
from ..utils import validate_not_empty, data_filter, convert_url_to_string


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
    image: HttpUrl | None = None
    type: Type
    seller_id: PydanticObjectId
    _not_empty = field_validator("name", "price", "quantity", mode="after")(
        validate_not_empty
    )
    _convert_to_str = field_validator("image", mode="after")(convert_url_to_string)


class UpdateProduct(BaseModel):
    name: str | None = None
    price: PositiveFloat | None = None
    quantity: NonNegativeInt | None = None
    description: str | None = None
    image: HttpUrl | None = None
    type: Type | None = None
    _not_empty = field_validator("name", "price", "quantity", mode="after")(
        validate_not_empty
    )
    _convert_to_str = field_validator("image", mode="after")(convert_url_to_string)


class StoredProduct(CreateProduct):
    id: PydanticObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    deactivated_at: datetime | None = Field(default=None)


class FilterParamsProduct(BaseModel):
    query_filter: str = ""
    limit: int = Field(100, gt=0)
    offset: int = Field(0, ge=0)
    sort_by: Literal["id", "price", "name", "type"] = "id"
    sort_dir: Literal["asc", "desc"] = "asc"
    category: Type | None = None

    def query_collection(
        self, collection: Collection, get_deleted: Optional[bool] = None
    ):

        extra_filter = {"type": {"$eq": self.category.value}} if self.category else None

        return (
            collection.find(data_filter(self.query_filter, get_deleted, extra_filter))
            .skip(self.offset)
            .limit(self.limit)
            .sort(self.sort_by, 1 if self.sort_dir == "asc" else -1)
        )

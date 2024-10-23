__all__ = ["Product", "StoredProduct", "UpdationProduct", "Type"]

from pydantic import BaseModel, Field
from datetime import datetime
from pydantic_mongo import PydanticObjectId
from enum import Enum


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
    deactivated_at: datetime | None = Field(default=None)
    seller_id: PydanticObjectId


class UpdationProduct(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None
    image: str | None = None


class StoredProduct(Product):
    id: PydanticObjectId = Field(alias="_id")

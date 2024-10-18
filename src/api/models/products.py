__all__ = ["Product", "StoredProduct", "UpdationProduct","Type","Seller"]

from pydantic import BaseModel, Field
from datetime import datetime
from pydantic_mongo import PydanticObjectId
from enum import Enum

class Seller(BaseModel):
    username: str
    email: str
    image: str | None = None

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
    description: str
    image: str
    type : Type
    deactivated_at: datetime | None = Field(default=None)
    seller : Seller | None = None


class UpdationProduct(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None
    image: str | None = None
    deactivated_at: datetime | None = Field(default=None)
    seller : Seller | None = None


class StoredProduct(Product):
    id: PydanticObjectId = Field(alias="_id")
    
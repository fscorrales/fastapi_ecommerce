__all__ = [
    "OrderStatus",
    "OrderProducts",
    "UpdateOrderProduct",
    "Order",
    "StoredOrder",
    "JoinedOrder",
]

from enum import Enum

from pydantic import BaseModel, Field, NonNegativeInt, PositiveFloat
from pydantic_mongo import PydanticObjectId
from .products import CreateProduct


class OrderStatus(str, Enum):
    shopping = "shopping"
    completed = "completed"
    cancelled = "cancelled"


class OrderProducts(BaseModel):
    product_id: PydanticObjectId
    price: PositiveFloat
    quantity: NonNegativeInt


class UpdateOrderProduct(OrderProducts):
    customer_id: PydanticObjectId


class Order(BaseModel):
    customer_id: PydanticObjectId
    order_products: list[OrderProducts]
    status: OrderStatus = OrderStatus.shopping


class StoredOrder(Order):
    id: PydanticObjectId = Field(alias="_id")


class ProductWithId(CreateProduct):
    product_id: PydanticObjectId


class JoinedOrder(StoredOrder):
    order_products: list[ProductWithId]

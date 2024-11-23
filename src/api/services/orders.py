__all__ = ["OrdersServiceDependency", "OrdersService"]


from copy import deepcopy
from typing import Annotated, Literal

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId

from ..config import COLLECTIONS, db, logger
from ..models import (
    Order,
    UpdateOrderProduct,
    StoredOrder,
    StoredProduct,
    OrderStatus,
    OrderProducts,
    JoinedOrder,
)
from ..services import AuthorizationDependency
from ..utils import validate_and_extract_data


class OrdersService:
    assert (collection_name := "orders") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def create_one(cls, order: Order):
        new_order = order.model_dump()
        new_order["customer_id"] = ObjectId(new_order["customer_id"])
        for product in new_order["order_products"]:
            product["product_id"] = ObjectId(product["product_id"])
        document = cls.collection.insert_one(new_order)
        if document:
            return StoredOrder.model_validate(
                cls.collection.find_one(document.inserted_id)
            )
        return None

    @classmethod
    def get_orders_by_customer_id(
        cls, customer_id: PydanticObjectId, order_status: str = "shopping"
    ):
        if cls.collection.find_one(
            {"customer_id": customer_id, "status": order_status}
        ):
            pipeline = [
                # Filters orders by customer_id and order_status
                {
                    "$match": {
                        "customer_id": customer_id,
                        "status": order_status,
                    }
                },
                # Performs a lookup to retrieve the products associated with the orde
                {"$unwind": "$order_products"},
                {
                    "$lookup": {
                        "from": "products",
                        "localField": "order_products.product_id",
                        "foreignField": "_id",
                        "as": "product",
                    }
                },
                {"$unwind": "$product"},
                {
                    "$group": {
                        "_id": "$_id",
                        "customer_id": {"$first": "$customer_id"},
                        "status": {"$first": "$status"},
                        "order_products": {
                            "$push": {
                                "product_id": "$order_products.product_id",
                                "price": "$order_products.price",
                                "quantity": "$order_products.quantity",
                                "name": "$product.name",
                                "image": "$product.image",
                                "category": "$product.category",
                                "description": "$product.description",
                                "seller_id": "$product.seller_id",
                            }
                        },
                    }
                },
            ]
            cursor = cls.collection.aggregate(pipeline)
            return validate_and_extract_data(cursor, JoinedOrder)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=order_status + " order not found",
            )

    # Used by seed_database.py
    @classmethod
    def add_to_cart(cls, customer_id: PydanticObjectId, product: OrderProducts):
        try:
            if document := cls.collection.find_one(
                {"customer_id": customer_id, "status": "shopping"}
            ):
                return cls.update_order_product(document.get("_id"), product, opt="add")
            else:
                order = {
                    "customer_id": customer_id,
                    "order_products": [product],
                    "status": "shopping",
                }
                order = Order.model_validate(order)
                return cls.create_one(order)
        except HTTPException as e:
            raise HTTPException(detail=e.detail, status_code=e.status_code)

    @classmethod
    def remove_from_cart(cls, customer_id: PydanticObjectId, product: OrderProducts):
        try:
            if document := cls.collection.find_one(
                {"customer_id": customer_id, "status": "shopping"}
            ):
                return cls.update_order_product(
                    document.get("_id"), product, opt="remove"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Shopping cart not found",
                )
        except HTTPException as e:
            raise HTTPException(detail=e.detail, status_code=e.status_code)

    @classmethod
    def update_order_product(
        cls,
        id: PydanticObjectId,
        product: OrderProducts,
        opt: Literal["add", "remove"] = "add",
    ):
        update_product = product.model_dump()
        update_product["product_id"] = ObjectId(update_product["product_id"])
        try:
            if opt == "add":
                if cls.collection.find_one(
                    {
                        "$and": [
                            {"_id": id},
                            {"order_products.product_id": product.product_id},
                        ]
                    },
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Product already in cart",
                    )
                document = cls.collection.find_one_and_update(
                    {"_id": id},
                    {"$push": {"order_products": update_product}},
                    return_document=True,
                )
            else:
                if not cls.collection.find_one(
                    {
                        "$and": [
                            {"_id": id},
                            {"order_products.product_id": product.product_id},
                        ]
                    },
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Product not in cart",
                    )
                document = cls.collection.find_one_and_update(
                    {"_id": id},
                    {"$pull": {"order_products": {"product_id": product.product_id}}},
                    return_document=True,
                )
            if document:
                return StoredOrder.model_validate(document).model_dump()
        except HTTPException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            )

    @classmethod
    def update_shopping_cart_status(
        cls, id: PydanticObjectId, order_status: OrderStatus
    ):
        document = cls.collection.find_one_and_update(
            {"_id": id, "status": OrderStatus.shopping},
            {"$set": {"status": order_status}},
            return_document=True,
        )
        if document:
            return StoredOrder.model_validate(document).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

    @classmethod
    def get_all(cls):
        # return [
        #     StoredOrder.model_validate(order).model_dump()
        #     for order in cls.collection.find()
        # ]
        cursor = cls.collection.find()
        return validate_and_extract_data(cursor, StoredOrder)

    @classmethod
    def get_one(cls, id: PydanticObjectId):
        if db_order := cls.collection.find_one({"_id": id}):
            return StoredOrder.model_validate(db_order).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        # filter_criteria: dict = {"_id": id}

        # if security.auth_user_role == "customer":
        #     filter_criteria.update(
        #         {"customer_id": security.auth_user_id},
        #     )

        # if security.auth_user_role != "seller":
        #     if db_order := cls.collection.find_one(filter_criteria):
        #         return StoredOrder.model_validate(db_order).model_dump()
        #     else:
        #         raise HTTPException(
        #             status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        #         )

        # if security.is_seller and security.auth_user_id:

        #     aggregate_result = [
        #         StoredOrder.model_validate(order).model_dump()
        #         for order in cls.collection.aggregate(
        #             get_orders_by_seller_id_aggregate_query(
        #                 security.auth_user_id, {"_id": id}
        #             )
        #         )
        #     ]

        # if len(aggregate_result) > 0:
        #     return StoredOrder.model_validate(aggregate_result[0]).model_dump()
        # else:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        #     )


OrdersServiceDependency = Annotated[OrdersService, Depends()]

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
    def get_shopping_cart_by_customer(
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
    def create_one(cls, order: Order):
        new_order = order.model_dump()
        new_order["customer_id"] = ObjectId(new_order["customer_id"])
        for product in new_order["order_products"]:
            product["product_id"] = ObjectId(product["product_id"])
        document = cls.collection.insert_one(new_order)
        if document:
            return str(document.inserted_id)
        return None

    @classmethod
    def update_order_product(
        cls,
        id: PydanticObjectId,
        product: OrderProducts,
        opt: Literal["add", "remove"] = "add",
    ):
        if opt == "add":
            document = cls.collection.find_one_and_update(
                {"_id": id},
                {"$push": {"products": product}},
                return_document=True,
            )
        else:
            document = cls.collection.find_one_and_update(
                {"_id": id},
                {"$pull": {"products": product}},
                return_document=True,
            )
        logger.info(document)
        if document:
            return StoredOrder.model_validate(document).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
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

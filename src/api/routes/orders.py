__all__ = ["orders_router"]

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic_mongo import PydanticObjectId

from ..models import UpdateOrderProduct, OrderStatus
from ..services import (
    OrdersServiceDependency,
    AuthorizationDependency,
)

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.get("/")
async def get_all_orders(
    orders: OrdersServiceDependency,
    security: AuthorizationDependency,
):
    security.is_admin_or_raise()
    return orders.get_all()


@orders_router.get("/{id}")
def get_order_by_id(
    id: PydanticObjectId,
    security: AuthorizationDependency,
    orders: OrdersServiceDependency,
):
    security.is_admin_or_raise()
    return orders.get_one(id, security)


# @orders_router.get("/get_by_seller/{id}")
# def get_orders_by_seller_id(
#     id: PydanticObjectId, security: SecurityDependency, orders: OrdersServiceDependency
# ):
#     if security.auth_user_role != "admin" and security.auth_user_id != id:
#         return JSONResponse(
#             {"error": "User does not have access to this orders"},
#             status_code=status.HTTP_401_UNAUTHORIZED,
#         )
#     return orders.get_all(QueryParams(filter=f"seller_id={id}"), security)


# @orders_router.get("/get_by_customer/{id}")
# def get_orders_by_customer_id(
#     id: PydanticObjectId, security: SecurityDependency, orders: OrdersServiceDependency
# ):
#     if security.auth_user_id != id and security.auth_user_role != "admin":
#         return (
#             JSONResponse(
#                 {"error": "User does not have access to this orders"},
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#             ),
#         )

#     return orders.get_all(QueryParams(filter=f"customer_id={id}"), security)


# @orders_router.get("/get_by_product/{id}")
# def get_orders_by_product_id(
#     id: PydanticObjectId, security: SecurityDependency, orders: OrdersServiceDependency
# ):
#     params = QueryParams(filter=f"order_products.product_id={id}")
#     return orders.get_all(params, security)


# @orders_router.patch("/buy/{id}")
# async def buy_shopping_cart(
#     id: PydanticObjectId,
#     orders: OrdersServiceDependency,
#     security: SecurityDependency
# ):
#     auth_user_id = security.auth_user_id
#     order = orders.get_one(id, None)
#     assert (
#         auth_user_id == order.get("customer_id", None) or security.auth_user_role == "admin"
#     ), "User does not have access to this order"
#     return orders.update_shopping_cart_status(id, OrderStatus.complete)


# @orders_router.patch("/cancel/{id}")
# async def cancel_shopping_cart(
#     id: PydanticObjectId,
#     orders: OrdersServiceDependency,
#     security: SecurityDependency
# ):
#     auth_user_id = security.auth_user_id
#     order = orders.get_one(id, None)
#     assert (
#         auth_user_id == order.get("customer_id", None) or security.auth_user_role == "admin"
#     ), "User does not have access to this order"
#     return orders.update_shopping_cart_status(id, OrderStatus.canceled)

__all__ = ["products_router"]

from typing import Annotated
from fastapi import APIRouter

from fastapi import HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse
from pydantic_mongo import PydanticObjectId

from ..models import CreateProduct, UpdateProduct, FilterParamsProduct
from ..services import (
    ProductsService,
    ProductsServiceDependency,
    AuthorizationDependency,
)

from typing import List

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/")
async def list_products(
    products: ProductsServiceDependency,
    query: Annotated[FilterParamsProduct, Query()],
):
    return products.get_all_active(query)


@products_router.get("/deleted")
async def list_deleted_products(
    products: ProductsServiceDependency,
    security: AuthorizationDependency,
    query: Annotated[FilterParamsProduct, Query()],
):
    security.is_admin_or_raise()
    return products.get_all_deleted(query)


@products_router.get("/include_deleted")
async def list_products(
    products: ProductsServiceDependency,
    security: AuthorizationDependency,
    query: Annotated[FilterParamsProduct, Query()],
):
    security.is_admin_or_raise()
    return products.get_all(query)


@products_router.get("/{id}")
async def get_product(id: PydanticObjectId):
    product = ProductsService.get_one(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.get("/product_by_seller/{id}")
async def get_by_seller(id: PydanticObjectId):
    product = ProductsService.get_one(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.post("/")
async def create_product(
    product: CreateProduct,
    products: ProductsServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_same_seller(product.model_dump()["seller_id"])
        return products.create_one(product)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@products_router.put("/{id}")
async def update_product(
    id: PydanticObjectId,
    product: UpdateProduct,
    products: ProductsServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_same_user(id)
        return products.update_one(id=id, product=product)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@products_router.delete("/{id}")
async def delete_product(
    id: PydanticObjectId,
    products: ProductsServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_same_seller(id)
        return products.delete_one(id)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@products_router.delete("/delete_hard/{id}")
async def delete_product_hard(
    id: PydanticObjectId,
    products: ProductsServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_raise()
        return products.delete_one_hard(id)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)

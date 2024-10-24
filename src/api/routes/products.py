__all__ = ["products_router"]

from fastapi import APIRouter

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic_mongo import PydanticObjectId

from ..models import Product, UpdationProduct,StoredProduct
from ..services import ProductsService, ProductsServiceDependency 

from typing import List

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/" )
async def list_products():
    return ProductsService.get_all_active()


@products_router.get("/deleted")
async def list_deleted_products():
    return ProductsService.get_all_deleted()


@products_router.get("/include_deleted")
async def list_products():
    return ProductsService.get_all()


@products_router.get("/{id}")
async def get_product(id: PydanticObjectId):
    product = ProductsService.get_one(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.get("/product_by_sellet/{id}")
async def get_by_seller(id: PydanticObjectId):
    product = ProductsService.get_one(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.post("/")
async def create_product( product: Product):
    return ProductsService.create_one(product)


@products_router.put("/{id}")
async def update_product(id : PydanticObjectId, product: UpdationProduct):
    return ProductsService.update_one(id=id, product=product)


@products_router.delete("/{id}")
async def delete_product(id : PydanticObjectId):
    return ProductsService.delete_one(id)


@products_router.delete("/delete_hard/{id}")
async def delete_product_hard(id : PydanticObjectId):
    return ProductsService.delete_product_hard(id)

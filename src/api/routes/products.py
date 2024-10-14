from fastapi import APIRouter

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/")
async def list_products():
    pass


@products_router.get("/deleted")
async def list_deleted_products():
    pass


@products_router.get("/include_deleted")
async def list_products():
    pass


@products_router.get("/{id}")
async def get_product():
    pass


@products_router.post("/")
async def create_product():
    pass


@products_router.put("/{id}")
async def update_product():
    pass


@products_router.delete("/{id}")
async def delete_product():
    pass


@products_router.get("/get_by_seller/{id}")
async def get_products_by_seller_id():
    pass

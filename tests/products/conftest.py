import pytest
from ...src.api.models import CreateProduct
from ...src.api.services import ProductsServiceDependency

from bson import ObjectId


@pytest.fixture
def products_schema():
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "price": {"type": "number"},
                "quantity": {"type": "integer"},
                "description": {"type": ["string", "null"]},
                "image": {"type": ["string", "null"]},
                "type": {"type": "string"},
                "deactivated_at": {"type": ["string", "null"]},
                "seller_id": {"type": "string"},
            },
            "required": ["id", "seller_id", "price", "quantity", "type", "name"],
        },
    }


@pytest.fixture
def dict_test_product() -> dict:
    return {
        "name": "Test Product",
        "price": 10985.75,
        "quantity": 10,
        "description": "Test Product Description",
        "image": "https://picsum.photos/200/300?random=1",
        "type": "Keyboard",
    }


@pytest.fixture
def create_and_delete_product(dict_test_product, create_and_delete_seller):
    dict_test_product["seller_id"] = create_and_delete_seller
    product = CreateProduct(**dict_test_product)
    product_id = (
        ProductsServiceDependency().create_one(product=product).model_dump()["id"]
    )
    yield product_id
    ProductsServiceDependency().delete_one_hard(id=ObjectId(product_id))

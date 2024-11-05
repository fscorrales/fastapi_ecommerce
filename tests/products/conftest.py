import pytest
from ...src.api.models import CreateProduct
from ...src.api.services import ProductsServiceDependency

from bson import ObjectId


@pytest.fixture
def create_product_schema():
    # pprint(products.CreateProduct.model_json_schema())
    return {
        "$defs": {
            "Type": {
                "enum": ["Percussion", "Wind", "String", "Keyboard", "Electronic"],
                "title": "Type",
                "type": "string",
            }
        },
        "type": "array",
        "items": {
            "properties": {
                "description": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "default": None,
                    "title": "Description",
                },
                "image": {
                    "anyOf": [
                        {
                            "format": "uri",
                            "maxLength": 2083,
                            "minLength": 1,
                            "type": "string",
                        },
                        {"type": "null"},
                    ],
                    "default": None,
                    "title": "Image",
                },
                "name": {"title": "Name", "type": "string"},
                "price": {"exclusiveMinimum": 0.0, "title": "Price", "type": "number"},
                "quantity": {"minimum": 0, "title": "Quantity", "type": "integer"},
                "seller_id": {"title": "Seller Id", "type": "string"},
                "type": {"$ref": "#/$defs/Type"},
            },
            "required": ["name", "price", "quantity", "type", "seller_id"],
            "title": "CreateProduct",
            "type": "object",
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


@pytest.fixture(
    params=[
        {"name": "Test Product"},
        {"price": 10985.75},
        {"quantity": 10},
        {"type": "Keyboard"},
        {
            "name": "Test Product",
            "price": 10985.75,
            "quantity": 10,
            "type": "Keyboard",
        },
    ]
)
def test_valid_product_fields(request):
    return request.param


@pytest.fixture(
    params=[
        {"name": "", "price": 10985.75, "quantity": 10, "type": "Keyboard"},
        {"name": "Test Product", "price": 0, "quantity": 10, "type": "Keyboard"},
        {"name": "Test Product", "price": 100, "quantity": -1, "type": "Keyboard"},
        {"name": "Test Product", "price": 100, "quantity": 100, "type": "otro"},
        {
            "name": "Test Product",
            "price": 10985.75,
            "quantity": 10,
            "type": "Keyboard",
            "description": 12345,
        },
        {
            "name": "Test Product",
            "price": 10985.75,
            "quantity": 10,
            "type": "Keyboard",
            "image": 123,
        },
    ]
)
def test_invalid_product_fields(request):
    return request.param

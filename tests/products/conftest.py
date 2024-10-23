import pytest


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
def create_and_delete_product():
    pass

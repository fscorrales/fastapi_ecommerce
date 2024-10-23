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
            "required": ["id", "seller_id", "price", "quantity", "type"],
        },
    }


#   "response": [
#     {
#       "name": "Product 1",
#       "price": 100,
#       "quantity": 10,
#       "description": "Product 1 description",
#       "image": "https://picsum.photos/200/300?random=1",
#       "type": "Keyboard",
#       "deactivated_at": null,
#       "seller_id": "671423902a2ab1f93c3fda7e",
#       "id": "671423992a2ab1f93c3fda82"
#     },

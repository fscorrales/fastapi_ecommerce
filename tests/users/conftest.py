import pytest


@pytest.fixture
def public_stored_user_schema():
    # pprint(users.PublicStoredUser.model_json_schema())
    return {
        "$defs": {
            "Role": {
                "enum": ["admin", "customer", "seller"],
                "title": "Role",
                "type": "string",
            }
        },
        "type": "array",
        "items": {
            "properties": {
                "id": {"title": " Id", "type": "string"},
                "deactivated_at": {
                    "anyOf": [
                        {"format": "date-time", "type": "string"},
                        {"type": "null"},
                    ],
                    "default": None,
                    "title": "Deactivated At",
                },
                "email": {"title": "Email", "type": "string"},
                "image": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "default": None,
                    "title": "Image",
                },
                "role": {"$ref": "#/$defs/Role"},
                "username": {"title": "Username", "type": "string"},
            },
            "required": ["username", "email", "role", "id"],
            "title": "PublicStoredUser",
            "type": "object",
        },
    }

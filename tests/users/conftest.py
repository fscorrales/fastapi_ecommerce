import pytest


@pytest.fixture
def active_users_schema():
    return {
        "response": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "username": {"type": "string"},
                    "email": {"type": ["string", "null"]},
                    "image": {"type": ["string", "null"]},
                    "role": {"type": "string"},
                    "deactivated_at": {"type": ["string", "null"]},
                },
                "required": ["id", "username", "role"],
            },
        },
        "error": {},
    }

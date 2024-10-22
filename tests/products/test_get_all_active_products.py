import jsonschema
from fastapi.testclient import TestClient

from ...src.main import app

client = TestClient(app)


def test_get_all_active_products(products_schema):
    response = client.get("/api/products/")
    assert response.status_code == 200
    jsonschema.validate(instance=response.json(), schema=products_schema)

from src.api.models import CreateUser, Order, CreateProduct
from src.api.services import OrdersService, ProductsService, UsersService
import json
import os
import random

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "sample_data")

# Read JSON from randomuser.me api
data_file = os.path.join(data_dir, "users.json")
with open(data_file) as f:
    users = json.load(f)

results = users["results"]

# Creating users
print("Creating users...")
customer_ids = []
seller_ids = []
user = {}
for result in results:
    user["username"] = result["login"]["username"]
    user["email"] = result["email"]
    user["password"] = result["login"]["password"]
    user["image"] = result["picture"]["large"]
    user["role"] = random.choice(["customer", "seller"])
    insertion_user = CreateUser.model_validate(user)
    result_id = UsersService.create_one(insertion_user).model_dump()["id"]
    (customer_ids if user["role"] == "customer" else seller_ids).append(result_id)


# Definición de tipos de productos
percussion = "Percussion"
wind = "Wind"
string = "String"
keyboard = "Keyboard"
electronic = "Electronic"

# Read JSON from mockaroo api
data_file = os.path.join(data_dir, "products.json")
with open(data_file) as f:
    results = json.load(f)

# Create some products
print("Creating products...")
product_ids = []
product = {}
for result in results:
    product["name"] = result["name"]
    product["category"] = result["category"]
    product["price"] = result["price"]
    product["quantity"] = result["quantity"]
    product["description"] = result["description"]
    product["image"] = result["image"]
    product["seller_id"] = random.choice(seller_ids)
    insertion_product = CreateProduct.model_validate(product)
    result_id = ProductsService.create_one(insertion_product).model_dump()["id"]
    product_ids.append(result_id)

# Create some orders

orders = [
    {
        "customer_id": random.choice(customer_ids),
        "status": "completed",
        "order_products": [
            {
                "product_id": random.choice(product_ids),
                "price": 400,
                "quantity": 3,
            },
            {
                "product_id": random.choice(product_ids),
                "price": 500,
                "quantity": 2,
            },
        ],
    },
    {
        "customer_id": random.choice(customer_ids),
        "status": "shopping",
        "order_products": [
            {
                "product_id": random.choice(product_ids),
                "price": 600,
                "quantity": 2,
            },
            {
                "product_id": random.choice(product_ids),
                "price": 700,
                "quantity": 5,
            },
        ],
    },
    {
        "customer_id": random.choice(customer_ids),
        "status": "cancelled",
        "order_products": [
            {
                "product_id": random.choice(product_ids),
                "price": 400,
                "quantity": 2,
            },
            {
                "product_id": random.choice(product_ids),
                "price": 600,
                "quantity": 3,
            },
        ],
    },
    {
        "customer_id": random.choice(customer_ids),
        "status": "completed",
        "order_products": [
            {
                "product_id": random.choice(product_ids),
                "price": 800,
                "quantity": 1,
            },
            {
                "product_id": random.choice(product_ids),
                "price": 900,
                "quantity": 2,
            },
        ],
    },
]

print("Creating orders...")
for order in orders:
    insertion_order = Order.model_validate(order)
    OrdersService.create_one(insertion_order)

print("Done!")

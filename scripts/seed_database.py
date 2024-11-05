from src.api.models import CreateUser, Order, CreateProduct
from src.api.services import OrdersService, ProductsService, UsersService
import json
import os
import random

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "sample_data")
data_file = os.path.join(data_dir, "users.json")

# Read JSON from randomuser.me api
with open(data_file) as f:
    users = json.load(f)

results = users["results"]

# Creating users
print("Creating users...")
customers_ids = []
sellers_ids = []
user = {}
for result in results:
    user["username"] = result["login"]["username"]
    user["email"] = result["email"]
    user["password"] = result["login"]["password"]
    user["image"] = result["picture"]["large"]
    user["role"] = random.choice(["customer", "seller"])
    insertion_user = CreateUser.model_validate(user)
    result_id = UsersService.create_one(insertion_user).model_dump()["id"]
    (customers_ids if user["role"] == "customer" else sellers_ids).append(result_id)

# Create some products

# Definición de tipos de productos
percussion = "Percussion"
wind = "Wind"
string = "String"
keyboard = "Keyboard"
electronic = "Electronic"

# Lista de productos
products = [
    {
        "name": "Product 1",
        "price": 100,
        "quantity": 100,
        "description": "Product 1 description",
        "image": "https://picsum.photos/200/300?random=1",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 2",
        "price": 200,
        "quantity": 200,
        "description": "Product 2 description",
        "image": "https://picsum.photos/200/300?random=2",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 3",
        "price": 300,
        "quantity": 300,
        "description": "Product 3 description",
        "image": "https://picsum.photos/200/300?random=3",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 4",
        "price": 400,
        "quantity": 400,
        "description": "Product 4 description",
        "image": "https://picsum.photos/200/300?random=4",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 5",
        "price": 500,
        "quantity": 500,
        "description": "Product 5 description",
        "image": "https://picsum.photos/200/300?random=5",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 6",
        "price": 600,
        "quantity": 600,
        "description": "Product 6 description",
        "image": "https://picsum.photos/200/300?random=6",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 7",
        "price": 700,
        "quantity": 700,
        "description": "Product 7 description",
        "image": "https://picsum.photos/200/300?random=7",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 8",
        "price": 800,
        "quantity": 800,
        "description": "Product 8 description",
        "image": "https://picsum.photos/200/300?random=8",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 9",
        "price": 900,
        "quantity": 900,
        "description": "Product 9 description",
        "image": "https://picsum.photos/200/300?random=9",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Product 10",
        "price": 1000,
        "quantity": 100,
        "description": "Product 10 description",
        "image": "https://picsum.photos/200/300?random=10",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Electric Drum Set",
        "price": 1200,
        "quantity": 500,
        "description": "An electric drum set for versatile playing.",
        "image": "https://picsum.photos/200/300?random=11",
        "type": percussion,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Saxophone",
        "price": 1500,
        "quantity": 300,
        "description": "A classic saxophone for jazz and more.",
        "image": "https://picsum.photos/200/300?random=12",
        "type": wind,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Electric Guitar",
        "price": 200,
        "quantity": 100,
        "description": "An electric guitar for rock and blues.",
        "image": "https://picsum.photos/200/300?random=13",
        "type": string,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Digital Piano",
        "price": 600,
        "quantity": 150,
        "description": "A digital piano with realistic sound.",
        "image": "https://picsum.photos/200/300?random=14",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Violin",
        "price": 450,
        "quantity": 800,
        "description": "A beautiful violin for classical music.",
        "image": "https://picsum.photos/200/300?random=15",
        "type": string,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Flute",
        "price": 300,
        "quantity": 120,
        "description": "A simple flute for beginners.",
        "image": "https://picsum.photos/200/300?random=16",
        "type": wind,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
    {
        "name": "Synthesizer",
        "price": 800,
        "quantity": 400,
        "description": "A powerful synthesizer for electronic music.",
        "image": "https://picsum.photos/200/300?random=17",
        "type": electronic,
        "deactivated_at": None,
        "seller_id": random.choice(sellers_ids),
    },
]


print("Creating products...")
product_ids = []
for product in products:
    insertion_product = CreateProduct.model_validate(product)
    result_id = ProductsService.create_one(insertion_product).model_dump()["id"]
    product_ids.append(result_id)

# Create some orders

orders = [
    {
        "customer_id": random.choice(customers_ids),
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
        "customer_id": random.choice(customers_ids),
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
        "customer_id": random.choice(customers_ids),
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
        "customer_id": random.choice(customers_ids),
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

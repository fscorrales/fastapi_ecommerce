from src.api.models import CreateUser, Order, CreateProduct
from src.api.services import OrdersService, ProductsService, UsersService

# Create two basic users

users = [
    {
        "username": "Vendedor1",
        "email": "a@a.com",
        "password": "123",
        "role": "seller",
    },
    {
        "username": "Vendedor2",
        "email": "c@c.com",
        "password": "123",
        "role": "seller",
    },
    {
        "username": "Comprador1",
        "email": "b@b.com",
        "password": "123",
        "role": "customer",
    },
    {
        "username": "Comprador2",
        "email": "d@d.com",
        "password": "123",
        "role": "customer",
    },
]

print("Creating users...")
users_ids = []
for user in users:
    insertion_user = CreateUser.model_validate(user)
    result_id = UsersService.create_one(insertion_user).model_dump()["id"]
    users_ids.append(result_id)

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
        "quantity": 10,
        "description": "Product 1 description",
        "image": "https://picsum.photos/200/300?random=1",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Product 2",
        "price": 200,
        "quantity": 20,
        "description": "Product 2 description",
        "image": "https://picsum.photos/200/300?random=2",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Product 3",
        "price": 300,
        "quantity": 30,
        "description": "Product 3 description",
        "image": "https://picsum.photos/200/300?random=3",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Product 4",
        "price": 400,
        "quantity": 40,
        "description": "Product 4 description",
        "image": "https://picsum.photos/200/300?random=4",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Product 5",
        "price": 500,
        "quantity": 50,
        "description": "Product 5 description",
        "image": "https://picsum.photos/200/300?random=5",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Product 6",
        "price": 600,
        "quantity": 60,
        "description": "Product 6 description",
        "image": "https://picsum.photos/200/300?random=6",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Product 7",
        "price": 700,
        "quantity": 70,
        "description": "Product 7 description",
        "image": "https://picsum.photos/200/300?random=7",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Product 8",
        "price": 800,
        "quantity": 80,
        "description": "Product 8 description",
        "image": "https://picsum.photos/200/300?random=8",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Product 9",
        "price": 900,
        "quantity": 90,
        "description": "Product 9 description",
        "image": "https://picsum.photos/200/300?random=9",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Product 10",
        "price": 1000,
        "quantity": 100,
        "description": "Product 10 description",
        "image": "https://picsum.photos/200/300?random=10",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Electric Drum Set",
        "price": 1200,
        "quantity": 5,
        "description": "An electric drum set for versatile playing.",
        "image": "https://picsum.photos/200/300?random=11",
        "type": percussion,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Saxophone",
        "price": 1500,
        "quantity": 3,
        "description": "A classic saxophone for jazz and more.",
        "image": "https://picsum.photos/200/300?random=12",
        "type": wind,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Electric Guitar",
        "price": 200,
        "quantity": 10,
        "description": "An electric guitar for rock and blues.",
        "image": "https://picsum.photos/200/300?random=13",
        "type": string,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Digital Piano",
        "price": 600,
        "quantity": 15,
        "description": "A digital piano with realistic sound.",
        "image": "https://picsum.photos/200/300?random=14",
        "type": keyboard,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Violin",
        "price": 450,
        "quantity": 8,
        "description": "A beautiful violin for classical music.",
        "image": "https://picsum.photos/200/300?random=15",
        "type": string,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
    {
        "name": "Flute",
        "price": 300,
        "quantity": 12,
        "description": "A simple flute for beginners.",
        "image": "https://picsum.photos/200/300?random=16",
        "type": wind,
        "deactivated_at": None,
        "seller_id": users_ids[1],
    },
    {
        "name": "Synthesizer",
        "price": 800,
        "quantity": 4,
        "description": "A powerful synthesizer for electronic music.",
        "image": "https://picsum.photos/200/300?random=17",
        "type": electronic,
        "deactivated_at": None,
        "seller_id": users_ids[0],
    },
]


print("Creating products...")
product_ids = []
for product in products:
    insertion_product = CreateProduct.model_validate(product)
    result_id = ProductsService.create_one(insertion_product)["_id"]
    product_ids.append(result_id)

# Create some orders

orders = [
    {
        "customer_id": users_ids[2],
        "status": "completed",
        "order_products": [
            {
                "product_id": product_ids[3],
                "price": 400,
                "quantity": 3,
            },
            {
                "product_id": product_ids[4],
                "price": 500,
                "quantity": 2,
            },
        ],
    },
    {
        "customer_id": users_ids[2],
        "status": "shopping",
        "order_products": [
            {
                "product_id": product_ids[5],
                "price": 600,
                "quantity": 2,
            },
            {
                "product_id": product_ids[6],
                "price": 700,
                "quantity": 5,
            },
        ],
    },
    {
        "customer_id": users_ids[2],
        "status": "cancelled",
        "order_products": [
            {
                "product_id": product_ids[3],
                "price": 400,
                "quantity": 2,
            },
            {
                "product_id": product_ids[5],
                "price": 600,
                "quantity": 3,
            },
        ],
    },
    {
        "customer_id": users_ids[3],
        "status": "completed",
        "order_products": [
            {
                "product_id": product_ids[7],
                "price": 800,
                "quantity": 1,
            },
            {
                "product_id": product_ids[8],
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

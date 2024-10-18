from src.api.models import CreationUser, Order, Product
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
    insertion_user = CreationUser.model_validate(user)
    result_id = UsersService.create_one(insertion_user)
    users_ids.append(result_id)

# Create some products

products = [
    {
        "seller_id": users_ids[0],
        "name": "Product 1",
        "description": "Product 1 description",
        "type": "Keyboard",
        "price": 100,
        "quantity": 10,
        "image": "https://picsum.photos/200/300?random=1",
    },
    {
        "seller_id": users_ids[0],
        "name": "Product 2",
        "description": "Product 2 description",
        "type": "Keyboard",
        "price": 200,
        "quantity": 20,
        "image": "https://picsum.photos/200/300?random=2",
    },
    {
        "seller_id": users_ids[0],
        "name": "Product 3",
        "description": "Product 3 description",
        "type": "Keyboard",
        "price": 300,
        "quantity": 30,
        "image": "https://picsum.photos/200/300?random=3",
    },
    {
        "seller_id": users_ids[0],
        "name": "Product 4",
        "description": "Product 4 description",
        "type": "Keyboard",
        "price": 400,
        "quantity": 40,
        "image": "https://picsum.photos/200/300?random=4",
    },
    {
        "seller_id": users_ids[0],
        "name": "Product 5",
        "description": "Product 5 description",
        "price": 500,
        "quantity": 50,
        "image": "https://picsum.photos/200/300?random=5",
    },
    {
        "seller_id": users_ids[0],
        "name": "Product 6",
        "description": "Product 6 description",
        "type": "Keyboard",
        "price": 600,
        "quantity": 60,
        "image": "https://picsum.photos/200/300?random=6",
    },
    {
        "seller_id": users_ids[1],
        "name": "Product 7",
        "description": "Product 7 description",
        "type": "Keyboard",
        "price": 700,
        "quantity": 70,
        "image": "https://picsum.photos/200/300?random=7",
    },
    {
        "seller_id": users_ids[1],
        "name": "Product 8",
        "description": "Product 8 description",
        "type": "Keyboard",
        "price": 800,
        "quantity": 80,
        "image": "https://picsum.photos/200/300?random=8",
    },
    {
        "seller_id": users_ids[1],
        "name": "Product 9",
        "description": "Product 9 description",
        "type": "Keyboard",
        "price": 900,
        "quantity": 90,
        "image": "https://picsum.photos/200/300?random=9",
    },
    {
        "seller_id": users_ids[1],
        "name": "Product 10",
        "description": "Product 10 description",
        "price": 1000,
        "quantity": 100,
        "image": "https://picsum.photos/200/300?random=10",
    },
]


print("Creating products...")
product_ids = []
for product in products:
    insertion_product = Product.model_validate(product)
    result_id = ProductsService.create_one(insertion_product)
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

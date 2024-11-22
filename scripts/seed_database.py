from src.api.models import CreateUser, Order, CreateProduct, Category, OrderStatus
from src.api.services import OrdersService, ProductsService, UsersService
from src.api.config import UNSPLASH_ACCESS_KEY
from .get_img_unsplash import get_img_unsplash
import json
import os
import random

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "sample_data")

# Read JSON from randomuser.me api
data_file = os.path.join(data_dir, "users.json")
with open(data_file, encoding="utf-8") as f:
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

# Read JSON from mockaroo api
data_file = os.path.join(data_dir, "products.json")
with open(data_file, encoding="utf-8") as f:
    results = json.load(f)

# Create some products
print("Creating products...")
if UNSPLASH_ACCESS_KEY:
    unsplash_img = {}
    categories = [category.value for category in Category]
    for category in categories:
        unsplash_img[category] = get_img_unsplash(
            UNSPLASH_ACCESS_KEY, category + " musical instrument", 50
        )

product_ids = []
product = {}
for result in results:
    product["name"] = result["name"]
    product["category"] = result["category"]
    product["price"] = result["price"]
    product["quantity"] = result["quantity"]
    product["description"] = result["description"]
    product["image"] = (
        random.choice(unsplash_img[product["category"]])
        if UNSPLASH_ACCESS_KEY
        else result["image"]
    )
    product["seller_id"] = random.choice(seller_ids)
    insertion_product = CreateProduct.model_validate(product)
    result_id = ProductsService.create_one(insertion_product).model_dump()["id"]
    product_ids.append(result_id)

# Create some orders
order_status = [order.value for order in OrderStatus]

orders = []

for _ in range(1000):
    order = {
        "customer_id": random.choice(customer_ids),
        "status": random.choice(order_status),
        "order_products": [],
    }

    num_products = random.randint(1, 5)
    for _ in range(num_products):
        product_id = random.choice(product_ids)
        price = round(random.uniform(0.1, 1000000), 2)
        quantity = random.randint(1, 3)
        order["order_products"].append(
            {
                "product_id": product_id,
                "price": price,
                "quantity": quantity,
            }
        )

    orders.append(order)

# Remove orders that do not meet the constraint
filtered_orders = []
shopping_orders = {}

for order in orders:
    customer_id = order["customer_id"]
    if order["status"] == "shopping":
        if customer_id not in shopping_orders:
            shopping_orders[customer_id] = True
            filtered_orders.append(order)
        else:
            continue
    else:
        filtered_orders.append(order)

# Update the list of orders with the filtered list
orders = filtered_orders

print("Creating orders...")
for order in orders:
    insertion_order = Order.model_validate(order)
    OrdersService.create_one(insertion_order)

print("Done!")

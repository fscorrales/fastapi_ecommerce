# Music Products eCommerce Backend (No Payment Gateway)

**Objective**: The goal of this project is to develop a backend API using Python and FastAPI to power an eCommerce platform for selling music-related products. The platform will not include a payment gateway, but it will simulate the purchase process and handle core eCommerce functionalities.

## Core Features:
1. **Model Creation**:
   - **Product**: Represents the music-related products available for sale.
   - **User**: Handles customer and seller profiles.
   - **Purchase**: Tracks purchases made by users.

2. **Basic Architecture**:
   - **config**: Application configuration settings.
   - **routes**: API routes for handling different requests.
   - **models**: Data models representing entities (e.g., Product, User, Purchase).
   - **database**: Database connection and query management.

3. **User Authentication**:
   - **Login**: Enables user authentication.
   - **User Registration**: Allows users to create accounts on the platform.

4. **Product Listings**:
   - **Pagination**: Ensures the product list is manageable with multiple pages.
   - **Filters**: Users can filter products by specific criteria (e.g., category).
   - **Search**: Provides a search functionality to find specific products.
   - **Sorting**: Sort products by price, popularity, etc.
   - **Seller's Product List**: Allows viewing products listed by a specific seller.

5. **Product Details**:
   - Provides detailed information about each product.

6. **Seller Information**:
   - Displays information about the seller for each product.

7. **Shopping Cart**:
   - Allows users to add products to a cart and simulate purchases.

## Buyer-Specific Features:
1. **Purchase Simulation**:
   - Simulates the payment process when a user buys products from the cart.

2. **Purchase History**:
   - Displays a buyer's past purchases for reference.

3. **Profile Management**:
   - Allows buyers to edit their profiles and upload a profile image.

---

This project will emphasize creating a robust and secure backend with FastAPI, handling user management, product catalogs, and purchase simulations efficiently.

## Instructions (lazy version, for VSCode users)
1. Open the preview of this file to continue:

   `[CTRL] + [SHIFT] + [V]` (Windows/Linux) or `[CMD] + [SHIFT] + [V]` (Mac)
1. [Install Python 3.12]((https://www.python.org/downloads/))
1. Install poetry (globally):
    - For windows
   ```bash
   pip install poetry
   ```
    - For Linux/Max
   ```bash
   pipx install poetry
   ```

1. Configure poetry:
   ```bash
   poetry config virtualenvs.in-project true
   ```
1. Create the venv and install dependencies:
   ```bash
   poetry install
   ```
1. Open the project directory in VSCode.
1. Set up the environment variables by copying the values from .env.example to a new file named .env.
1. In VSCode, select the appropriate interpreter:

   `[CTRL] + [SHIFT] + [P]` (Windows/Linux) or `[CMD] + [SHIFT] + [P]` (Mac) 
   Type: _Python: Select Interpreter_ and select the one corresponding to the environment created by `poetry`.
   >Alternative: Check the status bar (at the bottom of the VSCode window); if you open a Python file (e.g., main.py), you should see the selected interpreter in this bar, and you can change it by clicking there.
1. Now, if we open an integrated terminal in VSCode, the virtual environment should activate automatically. But just in case, you can manually activate it with:
   ```bash
   poetry shell
   ```
1. Run our server:
   ```bash
   fastapi dev src/main.py
   ```
1. As the console should say, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## For testing
We use pytest for automated testing of the API. You can run the tests by executing:
```bash
pytest -rA
```
The `-rA` argument is recommended as it provides a detailed report of the test results. The tests are organized into separate modules, each corresponding to a MongoDB collection (e.g., auth, users, products, orders). This modular structure ensures clear, targeted testing for each set of endpoints. Therefore, if you only want to run tests related to the user endpoints, you can do so by executing:
```bash
pytest -rA tests/users
```


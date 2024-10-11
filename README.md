### Music Products eCommerce Backend (No Payment Gateway)

**Objective**: The goal of this project is to develop a backend API using Python and FastAPI to power an eCommerce platform for selling music-related products. The platform will not include a payment gateway, but it will simulate the purchase process and handle core eCommerce functionalities.

### Core Features:
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

### Buyer-Specific Features:
1. **Purchase Simulation**:
   - Simulates the payment process when a user buys products from the cart.

2. **Purchase History**:
   - Displays a buyer's past purchases for reference.

3. **Profile Management**:
   - Allows buyers to edit their profiles and upload a profile image.

---

This project will emphasize creating a robust and secure backend with FastAPI, handling user management, product catalogs, and purchase simulations efficiently.

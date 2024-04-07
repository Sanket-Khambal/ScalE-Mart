# Shopping_Cart_System(OOP)
Shopping Cart System
This repository contains a Django-based shopping cart project that enables users to browse products, add items to their cart, apply discounts, and proceed to checkout. The project incorporates various features, including user authentication, product categorization, and a flexible discount system.

Features
User Authentication:

Users can register, log in, and log out.
Authenticated users have access to personalized features such as setting budgets and viewing their order history.
Product Management:

Products are categorized, allowing users to easily navigate through different product types.
Each product includes details such as name, category, and price.
Shopping Cart:

Users can add products to their shopping cart and view the cart at any time.
Quantity adjustments and product removal are supported.
Discount Strategies:

The project supports multiple discount strategies, including quantity-based discounts and coupon-based discounts.
Discounts are dynamically applied based on the user's cart content.
Budget Control:

Users can set budgets, and the system notifies them if their cart total exceeds the set budget during checkout.
Observers:

Observers, such as the BudgetExceededObserver and PriceDecreasedObserver, provide real-time notifications to users based on certain conditions.
Checkout Process:

Users can proceed to checkout, where various discounts are applied based on the cart's content.
The system supports payment methods like credit cards and PayPal.

Getting Started
Follow these steps to set up and run the project locally:

1. Clone the repository
2. Make sure you have python, and postgresql alongwith pgadmin installed (Can be downloaded from official website)
3. Install django:
    ```
    pip install django
    ```
4. Install psycopg2 module:
    ```
    pip install psycopg2
    ```

5. Enter database details in settings like this: 
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Shopping_cart_system',
        'USER': 'postgres',
        'PASSWORD':'your_password',
        'HOST':'localhost',
        'PORT': '5432',
        }
    }
    ```


6. Make migrations: 
    ```
    python manage.py makemigrations
    ```
7. Run Migrations:
    ```
    python manage.py migrate
    ```
8. Run sync db :
    ```
    python manage.py migrate --run-syncdb
    ```

9. With this query enter products in the products table:
    INSERT INTO public."Shopping_cart_system_product" (name, price, category) VALUES
    ('Laptop', 1000, 'Electronics'),
    ('Smartphone', 500, 'Electronics'),
    ('Headphones', 80, 'Electronics'),
    ('T-Shirt', 20, 'Clothing'),
    ('Jeans', 40, 'Clothing'),
    ('Sneakers', 60, 'Clothing'),
    ('Pain Reliever', 10, 'Pharmacy'),
    ('Vitamins', 15, 'Pharmacy'),
    ('Allergy Medication', 13, 'Pharmacy'),
    ('Milk', 8, 'Groceries'),
    ('Bread', 10, 'Groceries'),
    ('Fresh Vegetables', 15,'Groceries');

10. Run the server:
    ```
    python manage.py runserver
    ```
11. You can now access the website through the link you get in the cmd after running the runserver command.

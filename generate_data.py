from faker import Faker
import random
import mysql.connector
from datetime import datetime, timedelta

fake = Faker('en_IN')

# -------------------------
# MySQL Connection
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vivek@1008",
    database="blinkit_db"
)

cursor = conn.cursor()

# -------------------------
# Categories
# -------------------------
categories = [
    "Fruits & Vegetables",
    "Dairy & Breakfast",
    "Snacks",
    "Beverages",
    "Personal Care",
    "Household",
    "Bakery",
    "Frozen Food"
]

for category in categories:
    cursor.execute("""
    INSERT INTO categories(category_name)
    VALUES (%s)
    """, (category,))

conn.commit()

# -------------------------
# Products
# -------------------------
brands = ["Amul", "Nestle", "Britannia",
          "Parle", "Haldiram", "Tata", "Dabur"]

products = []

for i in range(1000):
    product_name = fake.word().capitalize() + " Product"
    category_id = random.randint(1, 8)
    price = round(random.uniform(20, 1000), 2)
    brand = random.choice(brands)

    cursor.execute("""
    INSERT INTO products
    (product_name, category_id, price, brand)
    VALUES (%s,%s,%s,%s)
    """, (product_name, category_id,
          price, brand))

conn.commit()

# -------------------------
# Customers
# -------------------------
cities = ["Delhi", "Mumbai", "Bangalore",
          "Hyderabad", "Pune",
          "Jaipur", "Lucknow"]

for i in range(10000):

    customer_name = fake.name()
    age = random.randint(18, 65)
    gender = random.choice(["Male", "Female"])
    city = random.choice(cities)
    pincode = fake.postcode()
    signup_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    cursor.execute("""
    INSERT INTO customers
    (customer_name, age,
    gender, city,
    pincode, signup_date)

    VALUES (%s,%s,%s,%s,%s,%s)
    """,

    (
        customer_name,
        age,
        gender,
        city,
        pincode,
        signup_date
    ))

conn.commit()

# -------------------------
# Orders + Payments +
# Delivery + Order Items
# -------------------------
payment_methods = [
    "UPI", "Cash",
    "Credit Card",
    "Debit Card"
]

for i in range(100000):

    customer_id = random.randint(1, 10000)

    order_date = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    total_amount = round(
        random.uniform(100, 3000),
        2
    )

    cursor.execute("""
    INSERT INTO orders
    (customer_id,
    order_date,
    total_amount)

    VALUES (%s,%s,%s)
    """,

    (
        customer_id,
        order_date,
        total_amount
    ))

    order_id = cursor.lastrowid

    # payment
    cursor.execute("""
    INSERT INTO payments
    (order_id,
    payment_method,
    payment_status)

    VALUES (%s,%s,%s)
    """,

    (
        order_id,
        random.choice(payment_methods),
        random.choice([
            "Success",
            "Pending"
        ])
    ))

    # delivery
    cursor.execute("""
    INSERT INTO delivery
    (order_id,
    delivery_time_minutes,
    delivery_status)

    VALUES (%s,%s,%s)
    """,

    (
        order_id,
        random.randint(10, 60),
        random.choice([
            "Delivered",
            "Cancelled"
        ])
    ))

    # order items
    for j in range(random.randint(1, 5)):

        product_id = random.randint(1, 1000)
        quantity = random.randint(1, 5)
        total_price = round(
            quantity *
            random.uniform(20, 1000),
            2
        )

        cursor.execute("""
        INSERT INTO order_items
        (order_id,
        product_id,
        quantity,
        total_price)

        VALUES (%s,%s,%s,%s)
        """,

        (
            order_id,
            product_id,
            quantity,
            total_price
        ))

    # batch commit
    if i % 1000 == 0:
        conn.commit()
        print(f"{i} orders inserted")

conn.commit()

# -------------------------
# Inventory
# -------------------------
warehouse_cities = [
    "Delhi",
    "Mumbai",
    "Bangalore"
]

for product_id in range(1, 1001):

    cursor.execute("""
    INSERT INTO inventory
    (product_id,
    stock_quantity,
    warehouse_city)

    VALUES (%s,%s,%s)
    """,

    (
        product_id,
        random.randint(10, 500),
        random.choice(
            warehouse_cities
        )
    ))

conn.commit()

print("Data Inserted Successfully!")

cursor.close()
conn.close()
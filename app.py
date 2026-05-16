import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# -------------------------
# MySQL Connection
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="blinkit_user",
    password="blinkit123",
    database="blinkit_db"
)

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Blinkit Dashboard",
    layout="wide"
)

st.title("🛒 Blinkit SQL Analytics Dashboard")

# -------------------------
# KPI Queries
# -------------------------
total_orders = pd.read_sql(
    "SELECT COUNT(*) AS total FROM orders",
    conn
)

total_customers = pd.read_sql(
    "SELECT COUNT(*) AS total FROM customers",
    conn
)

revenue = pd.read_sql(
    """
    SELECT ROUND(SUM(total_amount),2)
    AS revenue
    FROM orders
    """,
    conn
)

# -------------------------
# KPI Cards
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Orders",
    f"{total_orders['total'][0]:,}"
)

col2.metric(
    "Customers",
    f"{total_customers['total'][0]:,}"
)

col3.metric(
    "Revenue ₹",
    f"{revenue['revenue'][0]:,.2f}"
)

# -------------------------
# Top Revenue Cities
# -------------------------
city_query = """
SELECT
c.city,
ROUND(SUM(o.total_amount),2)
AS revenue
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC
"""

city_df = pd.read_sql(
    city_query,
    conn
)

fig_city = px.bar(
    city_df,
    x="city",
    y="revenue",
    title="Revenue by City"
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)

# -------------------------
# Payment Method
# -------------------------
payment_query = """
SELECT
payment_method,
COUNT(*) AS total_usage
FROM payments
GROUP BY payment_method
"""

payment_df = pd.read_sql(
    payment_query,
    conn
)

fig_payment = px.pie(
    payment_df,
    names="payment_method",
    values="total_usage",
    title="Payment Methods"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)

# -------------------------
# Top Products
# -------------------------
top_products_query = """
SELECT
p.product_name,
SUM(oi.quantity)
AS total_sold
FROM order_items oi
JOIN products p
ON oi.product_id =
p.product_id
GROUP BY p.product_name
ORDER BY total_sold DESC
LIMIT 10
"""

top_products = pd.read_sql(
    top_products_query,
    conn
)

st.subheader(
    "Top Selling Products"
)

st.table(
    top_products
)

conn.close()
import streamlit as st
import pandas as pd
from db_connection import connect_db
import queries

conn = connect_db()

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ------------------ TITLE ------------------
st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown("Analyze sales, customers, and revenue insights")

st.markdown("---")

# ------------------ KPIs ------------------
col1, col2, col3 = st.columns(3)

total_customers_df = pd.read_sql("SELECT COUNT(*) AS count FROM Customers", conn)
total_revenue_df = pd.read_sql("SELECT SUM(amount) AS total FROM Payments", conn)
total_orders_df = pd.read_sql("SELECT COUNT(*) AS count FROM Orders", conn)

total_customers = total_customers_df.iloc[0]['count']
total_revenue = total_revenue_df.iloc[0]['total'] or 0
total_orders = total_orders_df.iloc[0]['count']

col1.metric("Total Customers", total_customers)
col2.metric("Total Revenue", f"₹{int(total_revenue):,}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("🔍 Filter Data")

city = st.sidebar.selectbox("Select City", ["All", "Hyderabad", "Delhi", "Mumbai"])

if city == "All":
    query = "SELECT * FROM Customers"
else:
    query = f"SELECT * FROM Customers WHERE city = '{city}'"

df_customers = pd.read_sql(query, conn)

# ------------------ SEARCH ------------------
search = st.text_input("🔎 Search Customer Name")

if search:
    df_customers = df_customers[df_customers['name'].str.contains(search, case=False)]

# ------------------ CUSTOMER TABLE ------------------
st.subheader("Filtered Customers")
st.dataframe(df_customers)

# ------------------ DOWNLOAD ------------------
st.download_button(
    label="⬇ Download Customer Data",
    data=df_customers.to_csv(index=False),
    file_name="customers.csv",
    mime="text/csv"
)

st.markdown("---")

# ------------------ CHARTS ------------------
df2 = pd.read_sql(queries.sales_query, conn)
df3 = pd.read_sql(queries.revenue_query, conn)
df4 = pd.read_sql(queries.order_status_query, conn)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product")
    if not df2.empty:
        st.bar_chart(df2.set_index('product_name'))

with col2:
    st.subheader("Monthly Revenue")
    if not df3.empty:
        st.line_chart(df3.set_index('month'))

# Trend Insight
if not df3.empty and len(df3) > 1:
    if df3['revenue'].iloc[-1] > df3['revenue'].iloc[0]:
        st.success("📈 Revenue is increasing over time")
    else:
        st.warning("📉 Revenue is decreasing over time")

# Order Status
st.subheader("Order Status")
if not df4.empty:
    st.bar_chart(df4.set_index('order_status'))

st.markdown("---")

# ------------------ TOP CUSTOMERS ------------------
st.subheader("🏆 Top 5 Customers")

top_customers = pd.read_sql("""
SELECT c.name, SUM(p.amount) as total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Payments p ON o.order_id = p.order_id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 5
""", conn)

st.dataframe(top_customers)
st.info("Top customers contribute the highest revenue.")

st.markdown("---")

# ------------------ BUSINESS INSIGHTS ------------------
st.header("📊 Business Insights")

# Top Product
top_product = pd.read_sql("""
SELECT pr.product_name, SUM(p.amount) AS revenue
FROM Products pr
JOIN Order_Items oi ON pr.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN Payments p ON o.order_id = p.order_id
GROUP BY pr.product_name
ORDER BY revenue DESC
LIMIT 1
""", conn)

st.subheader("Top Revenue Product")
st.dataframe(top_product)
st.info("This product generates the highest revenue.")

# Top 3 Customers
top3_customers = pd.read_sql("""
SELECT c.name, SUM(p.amount) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Payments p ON o.order_id = p.order_id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 3
""", conn)

st.subheader("Top 3 Customers")
st.dataframe(top3_customers)
st.info("These customers contribute the most revenue.")

# Least Selling Product
least_product = pd.read_sql("""
SELECT pr.product_name, SUM(oi.quantity) AS total_sold
FROM Products pr
JOIN Order_Items oi ON pr.product_id = oi.product_id
GROUP BY pr.product_name
ORDER BY total_sold ASC
LIMIT 1
""", conn)

st.subheader("Least Selling Product")
st.dataframe(least_product)
st.warning("This product has low sales and needs attention.")

# Top City
top_city = pd.read_sql("""
SELECT city, COUNT(*) AS total_customers
FROM Customers
GROUP BY city
ORDER BY total_customers DESC
LIMIT 1
""", conn)

st.subheader("Top Customer City")
st.dataframe(top_city)
st.info("This city has the highest number of customers.")

# Payment Method
payment_method = pd.read_sql("""
SELECT payment_method, COUNT(*) AS usage_count
FROM Payments
GROUP BY payment_method
ORDER BY usage_count DESC
LIMIT 1
""", conn)

st.subheader("Most Used Payment Method")
st.dataframe(payment_method)
st.info("This is the most preferred payment method.")

st.markdown("---")

# ------------------ FOOTER ------------------
st.markdown("Built with Streamlit | SQL | Python")
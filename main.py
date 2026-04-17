import pandas as pd
import matplotlib.pyplot as plt
from db_connection import connect_db
import queries

conn = connect_db()

# Customers
df1 = pd.read_sql(queries.customers_query, conn)
print(df1)

# Sales
df2 = pd.read_sql(queries.sales_query, conn)
df2.plot(kind='bar', x='product_name', y='total_sold')
plt.title("Sales by Product")
plt.show()

# Revenue
df3 = pd.read_sql(queries.revenue_query, conn)
df3.plot(kind='line', x='month', y='revenue')
plt.title("Monthly Revenue")
plt.show()

# Top Customers
df_top = pd.read_sql(queries.top_customers_query, conn)
print("\nTop Customers:")
print(df_top)

# Order Status Analysis
df_status = pd.read_sql(queries.order_status_query, conn)
print("\nOrder Status:")
print(df_status)

# Order Status Chart
df_status.plot(kind='bar', x='order_status', y='total_orders')
plt.title("Order Status Distribution")
plt.show()
# Customers
customers_query = "SELECT * FROM Customers"

# Sales by Product
sales_query = """
SELECT p.product_name, SUM(oi.quantity) AS total_sold
FROM Products p
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY p.product_name
"""

# Monthly Revenue
revenue_query = """
SELECT MONTH(order_date) AS month, SUM(p.amount) AS revenue
FROM Orders o
JOIN Payments p ON o.order_id = p.order_id
GROUP BY MONTH(order_date)
"""

top_customers_query = """
SELECT c.name,
       SUM(p.amount) AS total_spent,
       RANK() OVER (ORDER BY SUM(p.amount) DESC) AS rank_position
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Payments p ON o.order_id = p.order_id
GROUP BY c.name
"""

monthly_trend_query = """
SELECT MONTH(order_date) AS month,
       SUM(p.amount) AS revenue
FROM Orders o
JOIN Payments p ON o.order_id = p.order_id
GROUP BY MONTH(order_date)
"""

order_status_query = """
SELECT order_status, COUNT(*) AS total_orders
FROM Orders
GROUP BY order_status
"""
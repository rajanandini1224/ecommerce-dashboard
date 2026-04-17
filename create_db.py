import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE Order_Items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
)
""")

cursor.execute("""
CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    payment_method TEXT,
    amount REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
)
""")

# Insert Sample Data
cursor.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?)", [
    (1, 'Amit', 'amit@gmail.com', 'Hyderabad'),
    (2, 'Sneha', 'sneha@gmail.com', 'Delhi'),
    (3, 'Rahul', 'rahul@gmail.com', 'Mumbai'),
    (4, 'Priya', 'priya@gmail.com', 'Hyderabad')
])

cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?)", [
    (1, 'Laptop', 'Electronics', 50000),
    (2, 'Phone', 'Electronics', 20000),
    (3, 'Shoes', 'Fashion', 3000),
    (4, 'Watch', 'Accessories', 5000)
])

cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?)", [
    (1, 1, '2024-01-01'),
    (2, 2, '2024-02-01'),
    (3, 3, '2024-03-01'),
    (4, 1, '2024-04-01')
])

cursor.executemany("INSERT INTO Order_Items VALUES (?, ?, ?, ?)", [
    (1, 1, 1, 1),
    (2, 2, 2, 2),
    (3, 3, 3, 3),
    (4, 4, 1, 1)
])

cursor.executemany("INSERT INTO Payments VALUES (?, ?, ?, ?)", [
    (1, 1, 'Credit Card', 50000),
    (2, 2, 'UPI', 40000),
    (3, 3, 'Debit Card', 9000),
    (4, 4, 'Credit Card', 50000)
])

conn.commit()
conn.close()

print("Database created successfully!")